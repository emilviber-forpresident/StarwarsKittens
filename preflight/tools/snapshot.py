# Usage: python -I snapshot.py <feature_id> <asof YYYY-MM-DD> <outfile>
import sys, json, re, html, subprocess, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
fid, asof, out = sys.argv[1], sys.argv[2], sys.argv[3]
ORG = "https://dev.azure.com/tunstallgroup/IHCP/_apis/wit/workitems"
tok = subprocess.run("az account get-access-token --resource 499b84ac-1321-427f-aa17-267ca6975798 --query accessToken -o tsv",
                     shell=True, capture_output=True, text=True).stdout.strip()
def get(i):
    url = f"{ORG}/{i}?asOf={asof}T23:59:59Z&$expand=relations&api-version=7.1"
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + tok})
    try:
        with urllib.request.urlopen(req) as r: return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e: return None   # did not exist at asOf
def md(s):
    s = s or ""
    s = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</h\d>", "\n", s)
    s = re.sub(r"(?i)<li[^>]*>", "\n- ", s)
    s = html.unescape(re.sub(r"<[^>]+>", "", s)).replace("\xa0", " ")
    s = re.sub(r"[ \t]+", " ", s); s = re.sub(r"\n\s*\n+", "\n\n", s)
    return "\n".join(l.strip() for l in s.splitlines()).strip()
FIELDS = [("Description", "System.Description"), ("Success criteria", "Custom.SuccesCriteria"),
          ("Acceptance criteria", "Microsoft.VSTS.Common.AcceptanceCriteria")]
def block(d, lvl):
    f = d["fields"]; pts = f.get("Microsoft.VSTS.Scheduling.StoryPoints")
    lines = [f"{'#'*lvl} {d['id']} [{f['System.WorkItemType']}] {f['System.Title']}",
             f"State: {f['System.State']} · Story points: {pts if pts is not None else 'none'}", ""]
    for label, k in FIELDS:
        if f.get(k): lines += [f"**{label}:**", md(f[k]), ""]
    return lines
feat = get(fid)
kids = [r["url"].rsplit("/",1)[1] for r in feat.get("relations") or [] if r["rel"].endswith("Hierarchy-Forward")]
lines = [f"# Feature snapshot: {fid} (as of {asof})", "",
         "Source: Azure DevOps work item fields at the snapshot date. Comments, history, people and links outside the hierarchy are excluded.", ""]
lines += block(feat, 2); log = []
for k in sorted(kids, key=int):
    d = get(k)
    if d: lines += block(d, 3); log.append(f"{k} included")
    else: log.append(f"{k} did not exist at as-of date")
open(out, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print(fid, asof, "children:", "; ".join(log))
