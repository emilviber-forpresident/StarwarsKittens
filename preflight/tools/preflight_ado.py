"""Padawan Pre-Flight <-> Azure DevOps glue (local demo version of the pipeline).

  python -I preflight_ado.py prepare <feature-id> <run-folder>
      Writes <run-folder>/input/feature.md (current state) and prints the repo tags (repo:<name>).
  python -I preflight_ado.py publish <feature-id> <run-folder> [--field Custom.PreFlight] [--attach] [--attach-html] [--comment]
      Publishes <run-folder>/output/preflight.md to the feature: HTML into a rich-text field (the tab),
      and/or as an attachment, and/or as a comment with the Top 3. Then swaps tag preflight -> preflight-done.

Auth: the Azure CLI login (az account get-access-token). In a pipeline, use System.AccessToken instead.
"""
import sys, os, json, re, html, subprocess, urllib.request, datetime

ORG, PROJECT = "https://dev.azure.com/tunstallgroup", "IHCP"
WIT = f"{ORG}/{PROJECT}/_apis/wit"
_tok = None


def token():
    global _tok
    if not _tok:
        _tok = os.environ.get("ADO_TOKEN") or subprocess.run(
            "az account get-access-token --resource 499b84ac-1321-427f-aa17-267ca6975798 --query accessToken -o tsv",
            shell=True, capture_output=True, text=True).stdout.strip()
    return _tok


def call(method, url, body=None, ctype="application/json"):
    data = None if body is None else (body if isinstance(body, bytes) else json.dumps(body).encode())
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Authorization": "Bearer " + token(), "Content-Type": ctype})
    with urllib.request.urlopen(req) as r:
        t = r.read().decode("utf-8")
        return json.loads(t) if t else {}


def strip_html(s):
    s = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</h\d>", "\n", s or "")
    s = re.sub(r"(?i)<li[^>]*>", "\n- ", s)
    s = html.unescape(re.sub(r"<[^>]+>", "", s)).replace("\xa0", " ")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n\n", s)
    return "\n".join(l.strip() for l in s.splitlines()).strip()


FIELDS = [("Description", "System.Description"), ("Success criteria", "Custom.SuccesCriteria"),
          ("Acceptance criteria", "Microsoft.VSTS.Common.AcceptanceCriteria")]


def item_md(d, lvl):
    f = d["fields"]
    pts = f.get("Microsoft.VSTS.Scheduling.StoryPoints")
    out = [f"{'#' * lvl} {d['id']} [{f['System.WorkItemType']}] {f['System.Title']}",
           f"State: {f['System.State']} · Story points: {pts if pts is not None else 'none'}", ""]
    for label, k in FIELDS:
        if f.get(k):
            out += [f"**{label}:**", strip_html(f[k]), ""]
    return out


def prepare(fid, run):
    feat = call("GET", f"{WIT}/workitems/{fid}?$expand=relations&api-version=7.1")
    kids = sorted((r["url"].rsplit("/", 1)[1] for r in feat.get("relations") or []
                   if r["rel"].endswith("Hierarchy-Forward")), key=int)
    lines = [f"# Feature snapshot: {fid} (as of {datetime.date.today()})", "",
             "Source: Azure DevOps work item fields. Comments, history and people are excluded.", ""]
    lines += item_md(feat, 2)
    for k in kids:
        lines += item_md(call("GET", f"{WIT}/workitems/{k}?api-version=7.1"), 3)
    os.makedirs(f"{run}/input", exist_ok=True)
    open(f"{run}/input/feature.md", "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    tags = [t.strip() for t in (feat["fields"].get("System.Tags") or "").split(";")]
    repos = [t[5:] for t in tags if t.lower().startswith("repo:")]
    print(f"feature {fid}: {len(kids)} children -> {run}/input/feature.md")
    print("repos:", " ".join(repos) or "(none tagged)")
    # Clone the tagged repos (default branch, shallow, no git history) unless already present.
    os.makedirs(f"{run}/repos", exist_ok=True)
    for name in repos:
        dest = f"{run}/repos/{name}"
        if os.path.isdir(dest):
            print(f"  {name}: already present")
            continue
        subprocess.run(["git", "clone", "-q", "--depth", "1", f"{ORG}/{PROJECT}/_git/{name}", dest], check=True)
        subprocess.run(["rm", "-rf", f"{dest}/.git"], check=False) if os.name != "nt" else \
            subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", os.path.normpath(f"{dest}/.git")], check=False)
        print(f"  {name}: cloned")


# --- Markdown -> HTML for the ADO rich-text field --------------------------------------------------
# ADO sanitises the field: no <style>, no classes, so everything is inline-styled. Sections become
# <details>/<summary>; if a sanitiser strips those, the summary text still reads as a bold line.
ACCENT = "#773b93"
# Translucent greys and tints read well on both the light and the dark ADO theme.
LINE, HEAD_BG, TINT = "rgba(128,128,128,.30)", "rgba(128,128,128,.10)", "rgba(119,59,147,.07)"
MUTED = "opacity:.72"
PILL = {"now": ("#a4262c", "#fde7e9"), "before sprint": ("#8a5300", "#fff4ce"),
        "in sprint": ("#3b3a39", "#edebe9"), "high": ("#0b6a0b", "#dff6dd"),
        "medium": ("#8a5300", "#fff4ce"), "low": ("#3b3a39", "#edebe9")}
ROLE_COLOR = {"po": "#0f6cbd", "architect": "#773b93", "developer": "#0b6a0b", "dev": "#0b6a0b",
              "tester": "#ca5010", "ux": "#038387"}
READINESS = ["Idea", "Shaped", "Refined, open decisions", "Ready for dev", "Ready, decisions recorded"]
LABEL = "font-size:11px;text-transform:uppercase;letter-spacing:.06em;font-weight:600;" + MUTED


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", rf'<code style="font-size:12px;background:{HEAD_BG};padding:0 4px;'
                             r'border-radius:3px">\1</code>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    return re.sub(r"(?<![\w>-])([DSPA]-\d\d)\b", r'<b style="white-space:nowrap">\1</b>', s)


def pill(text, fg=None, bg=None):
    fg, bg = (fg, bg) if fg else PILL.get(text.strip().lower(), (None, None))
    if not fg:
        return inline(text)
    return (f'<span style="color:{fg};background:{bg};border-radius:10px;padding:1px 8px;'
            f'white-space:nowrap;font-size:12px;font-weight:600">{html.escape(text.strip())}</span>')


def table(hdr, body):
    pills = {i for i, h in enumerate(hdr) if h.lower() in ("urgency", "conf.", "confidence")}
    narrow = {i for i, h in enumerate(hdr) if h.lower() in ("#", "id", "min", "timebox", "conf.")}
    th = (f"text-align:left;padding:6px 10px;background:{HEAD_BG};border-bottom:1px solid {LINE};"
          "font-size:11px;text-transform:uppercase;letter-spacing:.04em")
    td = f"vertical-align:top;padding:6px 10px;border-bottom:1px solid {LINE}"
    cell = lambda i, c: pill(c) if i in pills else (
        f'<span style="{MUTED}">{inline(c)}</span>' if hdr[i] == "#" else inline(c))
    t = [f'<table style="border-collapse:collapse;width:100%;margin:6px 0 12px;font-size:13px">',
         "<tr>" + "".join(f'<th style="{th}">{inline(c)}</th>' for c in hdr) + "</tr>"]
    t += ["<tr>" + "".join(f'<td style="{td}{";white-space:nowrap" if i in narrow else ""}">{cell(i, c)}</td>'
                           for i, c in enumerate(r)) + "</tr>" for r in body]
    return "".join(t) + "</table>"


def blocks(lines):
    """Tables, lists, paragraphs and ###-headings, all inline-styled."""
    out, rows, lst = [], [], None

    def flush():
        nonlocal rows, lst
        if rows:
            cells = lambda r: [c.strip() for c in r.strip().strip("|").split("|")]
            out.append(table(cells(rows[0]), [cells(r) for r in rows[1:] if not re.fullmatch(r"[\s|:-]+", r)]))
            rows = []
        if lst:
            out.append(f"</{lst}>")
            lst = None

    for line in lines:
        if line.lstrip().startswith("|"):
            rows.append(line)
            continue
        m_ul, m_ol = re.match(r"\s*[-*] (.*)", line), re.match(r"\s*\d+\. (.*)", line)
        if m_ul or m_ol:
            kind = "ul" if m_ul else "ol"
            if rows or (lst and lst != kind):
                flush()
            if not lst:
                out.append(f'<{kind} style="margin:4px 0 8px;padding-left:20px">')
                lst = kind
            out.append(f'<li style="margin:3px 0">{inline((m_ul or m_ol).group(1))}</li>')
            continue
        flush()
        h = re.match(r"(#{3,6}) (.*)", line)
        if h:
            out.append(f'<p style="{LABEL};margin:14px 0 2px">{inline(h.group(2))}</p>')
        elif line.strip():
            out.append(f'<p style="margin:6px 0">{inline(line)}</p>')
    flush()
    return "\n".join(out)


def split(lines, marker):
    """[(heading, blurb, body_lines)] per `marker ` heading; text before the first heading comes first."""
    parts, cur = [], ["", []]
    for l in lines:
        if l.startswith(marker + " "):
            parts.append(cur)
            cur = [l[len(marker) + 1:].strip(), []]
        else:
            cur[1].append(l)
    parts.append(cur)
    res = []
    for head, body in parts:
        blurb = next((b[2:].strip() for b in body if b.startswith("> ")), "")
        res.append((head, blurb, [b for b in body if not b.startswith("> ")]))
    return res


def fold(title_html, blurb, inner, stripe=LINE):
    b = f'<div style="{MUTED};font-size:13px;margin:2px 0 0 18px">{inline(blurb)}</div>' if blurb else ""
    return (f'<details style="border:1px solid {LINE};border-left:4px solid {stripe};border-radius:6px;'
            f'margin:8px 0;padding:8px 12px">'
            f'<summary style="cursor:pointer;font-size:14px">{title_html}{b}</summary>'
            f'<div style="padding:8px 0 0 18px">{inner}</div></details>')


def role_fold(head, blurb, body):
    m = re.match(r"(.*?)\s*·\s*(\d+)\s*items?", head)
    name, n = (m.group(1), m.group(2)) if m else (head, "")
    color = ROLE_COLOR.get(name.strip().lower(), ACCENT)
    count = f' {pill(n + (" item" if n == "1" else " items"), color, HEAD_BG)}' if n else ""
    return fold(f'<b style="color:{color}">{inline(name)}</b>{count}', blurb, blocks(body), stripe=color)


def readiness_meter(level):
    cells = "".join(f'<td title="{i}: {READINESS[i]}" style="width:36px;height:8px;padding:0;border-radius:4px;'
                    f'background:{ACCENT if i <= level else LINE}"></td>' for i in range(5))
    return (f'<table style="border-collapse:separate;border-spacing:3px 0;display:inline-table;'
            f'vertical-align:middle;margin-right:10px"><tr>{cells}</tr></table>')


def stat_chips(text):
    """'**Maturity:** 6/9 stories with ... · 0/9 estimated · 7 decisions open' -> a row of number tiles."""
    tiles = []
    for part in [p.strip() for p in re.sub(r"\*\*Maturity:\*\*", "", text).split("·") if p.strip()]:
        m = re.match(r"([\d/]+)\s+(.*)", part)
        num, lab = (m.group(1), m.group(2)) if m else ("", part)
        tiles.append(f'<td style="padding:6px 12px;border:1px solid {LINE};border-radius:6px;min-width:70px;'
                     f'vertical-align:top"><div style="font-size:18px;font-weight:600">{html.escape(num)}</div>'
                     f'<div style="font-size:12px;{MUTED}">{html.escape(lab)}</div></td>')
    return (f'<table style="border-collapse:separate;border-spacing:6px 0;margin:8px -6px">'
            f'<tr>{"".join(tiles)}</tr></table>')


def summary_card(body):
    out, para, mode, blockers = [], [], None, []
    kv = []
    for line in body + [""]:
        s = line.strip()
        m = re.match(r"\*\*Readiness:\s*(\d)\s*([^*]*)\*\*\s*·?\s*(.*)", s)
        if m:
            lvl = min(int(m.group(1)), 4)
            label = (m.group(2).strip(" ()·-") or READINESS[lvl])
            out.append(f'<div style="margin:2px 0 4px">{readiness_meter(lvl)}<b style="font-size:16px">'
                       f'Readiness {lvl}/4 · {html.escape(label[:1].upper() + label[1:])}</b></div>'
                       + (f'<div style="{MUTED};font-size:13px">{inline(m.group(3))}</div>' if m.group(3) else ""))
        elif s.startswith("**Maturity:**"):
            out.append(stat_chips(s))
        elif re.fullmatch(r"\*\*Blockers\*\*:?", s):
            mode = "blockers"
        elif mode == "blockers" and re.match(r"\d+\. ", s):
            blockers.append(re.sub(r"^\d+\.\s*", "", s))
        elif re.match(r"\*\*(Next step|Who is needed):\*\*", s):
            k, v = re.match(r"\*\*([^*]+):\*\*\s*(.*)", s).groups()
            kv.append((k, v))
        elif s:
            para.append(s)
        elif para:
            out.append(f'<p style="margin:10px 0;font-size:14px;line-height:1.5">{inline(" ".join(para))}</p>')
            para = []
    if blockers:
        rows = "".join(
            f'<tr><td style="vertical-align:top;padding:5px 8px;width:22px"><span style="display:inline-block;'
            f'width:20px;height:20px;line-height:20px;text-align:center;border-radius:10px;background:#c50f1f;'
            f'color:#fff;font-size:12px;font-weight:600">{i}</span></td>'
            f'<td style="padding:5px 8px">{inline(b)}</td></tr>' for i, b in enumerate(blockers, 1))
        out.append(f'<p style="{LABEL};margin:12px 0 2px">Blockers</p>'
                   f'<table style="border-collapse:collapse;font-size:13px">{rows}</table>')
    if kv:
        rows = "".join(f'<tr><td style="{LABEL};padding:5px 12px 5px 0;white-space:nowrap;vertical-align:top">'
                       f'{html.escape(k)}</td><td style="padding:5px 0;font-size:13px">{inline(v)}</td></tr>'
                       for k, v in kv)
        out.append(f'<table style="border-collapse:collapse;margin-top:10px;border-top:1px solid {LINE};'
                   f'width:100%">{rows}</table>')
    return (f'<div style="background:{TINT};border:1px solid {LINE};border-left:4px solid {ACCENT};'
            f'border-radius:6px;padding:12px 16px;margin:6px 0 16px">{"".join(out)}</div>')


def section_label(title, blurb):
    b = f' <span style="{MUTED};font-size:13px">· {inline(blurb)}</span>' if blurb else ""
    return f'<p style="margin:18px 0 4px"><span style="{LABEL}">{inline(title)}</span>{b}</p>'


def md_to_html(md):
    out, details = [], []
    for i, (head, blurb, body) in enumerate(split(md.splitlines(), "##")):
        if i == 0:  # title + meta line: the work item already shows the title, so keep only the meta
            meta = [l for l in body if l.strip() and not l.startswith("# ")]
            if meta:
                out.append(f'<p style="{MUTED};font-size:12px;margin:0 0 6px">{inline(meta[0])}</p>')
        elif head.lower() == "summary":
            out.append(summary_card(body))
        elif head.lower() == "by role":
            subs = split(body, "###")
            out.append(section_label("By role", blurb) + blocks(subs[0][2])
                       + "".join(role_fold(h, bl, bd) for h, bl, bd in subs[1:]))
        else:
            details.append(fold(f"<b>{inline(head)}</b>", blurb, blocks(body)))
    if details:
        out.append(section_label("Details", "") + "".join(details))
    return "\n".join(out)


def summary_md(md):
    for pat in (r"## Summary[^\n]*\n(.*?)(\n## |\Z)", r"## Top 3[^\n]*\n(.*?)(\n## |\Z)"):  # v0.3, v0.2
        m = re.search(pat, md, re.S)
        if m:
            return m.group(1).strip()
    return ""


def standalone_page(fid, title, body_html):
    """The Pre-Flight view as a self-contained HTML file (for an attachment, when there is no tab)."""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Pre-Flight {fid}</title>
<style>:root{{color-scheme:light dark}}body{{margin:0;background:#fff;color:#201f1e;
font:14px/1.45 "Segoe UI",system-ui,sans-serif}}@media (prefers-color-scheme:dark){{body{{background:#1b1a19;color:#f3f2f1}}}}
.wrap{{max-width:1100px;margin:0 auto;padding:20px 16px}}h1{{font-size:20px;margin:0 0 4px}}
.wrap>div,.wrap details{{overflow-x:auto}}</style></head><body><div class="wrap">
<h1>Pre-Flight · {fid} {html.escape(title)}</h1>{body_html}</div></body></html>"""


def publish(fid, run, field=None, attach=False, comment=False, attach_html=False):
    md = open(f"{run}/output/preflight.md", encoding="utf-8").read()
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    ops = []
    banner = (f'<p style="font-size:12px;{MUTED}"><i>Generated by Padawan Pre-Flight · {stamp} · '
              'AI draft: verify before acting.</i></p>')
    if field:
        ops.append({"op": "add", "path": f"/fields/{field}", "value": banner + md_to_html(md)})
    feat = call("GET", f"{WIT}/workitems/{fid}?fields=System.Tags,System.Title&api-version=7.1")
    files = []
    if attach:
        files.append((f"preflight-{fid}-{stamp[:10]}.md", md))
    if attach_html:
        files.append((f"preflight-{fid}-{stamp[:10]}.html",
                      standalone_page(fid, feat["fields"]["System.Title"], banner + md_to_html(md))))
    for name, text in files:
        a = call("POST", f"{WIT}/attachments?fileName={name}&api-version=7.1", text.encode("utf-8"),
                 ctype="application/octet-stream")
        ops.append({"op": "add", "path": "/relations/-",
                    "value": {"rel": "AttachedFile", "url": a["url"], "attributes": {"comment": "Padawan Pre-Flight"}}})
    tags = [t.strip() for t in (feat["fields"].get("System.Tags") or "").split(";") if t.strip()]
    tags = [("preflight-done" if t == "preflight" else t) for t in tags]
    # "replace", not "add": ADO merges tags on "add", so the old "preflight" tag would stay.
    ops.append({"op": "replace", "path": "/fields/System.Tags", "value": "; ".join(dict.fromkeys(tags))})
    call("PATCH", f"{WIT}/workitems/{fid}?api-version=7.1", ops, ctype="application/json-patch+json")
    if comment:
        body = (f"<p><b>Padawan Pre-Flight</b> ran {stamp}.</p>" + summary_card(summary_md(md).splitlines())
                + f"<p>Full result: {'the Pre-Flight tab' if field else 'the attached ' + ('HTML page' if attach_html else 'preflight.md')}.</p>")
        call("POST", f"{WIT}/workItems/{fid}/comments?api-version=7.1-preview.4", {"text": body})
    print("published:", ", ".join(x for x, on in [(f"field {field}", field), ("md attachment", attach), ("html attachment", attach_html),
                                                  ("comment", comment)] if on), "+ tag preflight-done")


PREVIEW_CSS = """
:root{--bg:#f8f8f8;--card:#fff;--ink:#201f1e;--muted:#605e5c;--line:#e1dfdd;--accent:#0f6cbd;--tag:#eef3fb}
@media (prefers-color-scheme: dark){:root{--bg:#1b1a19;--card:#252423;--ink:#f3f2f1;--muted:#c8c6c4;--line:#3b3a39;--accent:#6cb8f6;--tag:#2b3a4a}}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 "Segoe UI",system-ui,sans-serif}
.wrap{max-width:1200px;margin:0 auto;padding:16px}
.head{background:var(--card);border:1px solid var(--line);border-left:4px solid #773b93;padding:12px 16px}
.type{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.04em}
h1{font-size:20px;margin:4px 0 8px}.meta{color:var(--muted);font-size:13px}
.tag{display:inline-block;background:var(--tag);border-radius:3px;padding:1px 8px;margin:2px 4px 0 0;font-size:12px}
.tabs{display:flex;gap:4px;border-bottom:1px solid var(--line);margin-top:12px;overflow-x:auto}
.tabs button{background:none;border:0;border-bottom:2px solid transparent;padding:8px 12px;color:var(--muted);font:inherit;cursor:pointer;white-space:nowrap}
.tabs button.on{color:var(--ink);border-bottom-color:var(--accent);font-weight:600}
.pane{display:none;background:var(--card);border:1px solid var(--line);border-top:0;padding:12px 16px;overflow-x:auto}.pane.on{display:block}
code{font-size:12px;background:var(--bg);padding:0 3px;border-radius:3px}
.note{color:var(--muted);font-style:italic}.empty{color:var(--muted)}
"""


def preview(fid, run):
    """Local stand-in for the Pre-Flight tab: renders exactly the HTML publish --field would write."""
    f = call("GET", f"{WIT}/workitems/{fid}?api-version=7.1")["fields"]
    md = open(f"{run}/output/preflight.md", encoding="utf-8").read()
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    tab_html = (f"<p class='note'>Generated by Padawan Pre-Flight · {stamp} · AI draft: verify before acting. "
                f"This is the content of field Custom.PreFlight.</p>" + md_to_html(md))
    tags = "".join(f"<span class='tag'>{html.escape(t.strip())}</span>"
                   for t in (f.get("System.Tags") or "").split(";") if t.strip())
    details = (f.get("System.Description") or "") + (
        f"<h3>Success criteria</h3>{f['Custom.SuccesCriteria']}" if f.get("Custom.SuccesCriteria") else "")
    tabs = [("Details", details), ("Definition of Done", "<p class='empty'>(not shown in preview)</p>"),
            ("Related Work items", "<p class='empty'>(not shown in preview)</p>"), ("Pre-Flight", tab_html)]
    btns = "".join(f"<button data-t='{i}' class='{'on' if n == 'Pre-Flight' else ''}'>{n}</button>"
                   for i, (n, _) in enumerate(tabs))
    panes = "".join(f"<div class='pane {'on' if n == 'Pre-Flight' else ''}' id='p{i}'>{c}</div>"
                    for i, (n, c) in enumerate(tabs))
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Pre-Flight tab preview</title>
<style>{PREVIEW_CSS}</style></head><body><div class="wrap">
<div class="head"><div class="type">Feature {fid} · local preview of the Pre-Flight tab</div>
<h1>{html.escape(f['System.Title'])}</h1>
<div class="meta">State: {html.escape(f['System.State'])} · Area: {html.escape(f.get('System.AreaPath', ''))}</div>
<div>{tags}</div></div>
<div class="tabs">{btns}</div>{panes}</div>
<script>document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{{
document.querySelectorAll('.tabs button,.pane').forEach(e=>e.classList.remove('on'));
b.classList.add('on');document.getElementById('p'+b.dataset.t).classList.add('on');}});</script>
</body></html>"""
    out = f"{run}/output/preview.html"
    open(out, "w", encoding="utf-8").write(page)
    print("preview:", os.path.abspath(out))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cmd, fid, run = sys.argv[1], sys.argv[2], sys.argv[3]
    if cmd == "prepare":
        prepare(fid, run)
    elif cmd == "preview":
        preview(fid, run)
    elif cmd == "publish":
        a = sys.argv[4:]
        publish(fid, run, field=a[a.index("--field") + 1] if "--field" in a else None,
                attach="--attach" in a, comment="--comment" in a,
                attach_html="--attach-html" in a)
