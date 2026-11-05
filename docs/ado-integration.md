# Pre-Flight in Azure DevOps: design sketch (5 Nov 2026, draft)

Goal: Pre-Flight runs automatically on features in ADO, picks up the right repos, and shows its output on the feature.

## Flow
```
Feature gets tag "preflight"  ──(Service hook: work item updated, tag filter)──▶  Incoming WebHook
   └▶ Azure Pipeline (webhook trigger)
        1. Fetch the feature + children over REST  → input/feature.md      (preflight/tools/snapshot.py, as of "now")
        2. Read repo list from the feature's tags   → shallow-clone into repos/ (System.AccessToken, read-only)
        3. Run the agent headless                   → output/preflight.md
              claude -p "Read prompts/00-runner.md and run Pre-Flight."   (or: codex exec "...")
        4. Publish the result to the feature        → tab field and/or attachment, plus a short comment
        5. Swap tag "preflight" → "preflight-done"
```

## Decisions and recommendations
| Topic | Options | Recommendation |
|---|---|---|
| **Trigger** | (a) on "work item created" (b) a tag `preflight` added (c) state changed to "Ready for refinement" | **(b) the tag.** New features are often empty: 404917 had no stories until 4 Mar, four months after it was created. A tag lets the team re-run on demand. (c) is a good later step. |
| **Repo context** | ADO repos can't be tagged per feature. (a) work item tags `repo:AlarmServer.Swamp` (b) a custom field "Pre-Flight repos" (c) a mapping from area path to repos in a config file | **(a) for now**, because it needs no process change. **(b) later**, placed on the Pre-Flight tab itself (input and output in one place). (c) is a good fallback default. |
| **Output: tab** | (a) inherited process: a **new page** on the Feature form with a rich-text custom field "Pre-Flight", which the pipeline writes as HTML (b) an ADO extension with a work-item-form page contribution | **(a).** It's a real tab with no code to ship, but it needs **process admin** rights and applies to every feature in that process. (b) is only worth it for interactive features (re-run button, comparing versions). |
| **Output: first draft** | Attach `preflight-<date>.md` to the feature, and add a comment with the Top 3 and a link | **Do this first.** It's only REST calls and needs no admin. Keep it even with the tab, as a version history. |
| **Agent runtime** | Claude Code `claude -p` / Claude Agent SDK / `codex exec` | Same prompts for each (tool-neutral). Needs an API key as a **secret pipeline variable**. |

## Risks and guardrails
- **Prompt injection:** feature text is untrusted input to an agent with tools. Run it read-only: allow only file read and search tools, no shell or network, and use an ephemeral build agent.
- **Data:** ticket text and code are sent to the model API. That's OK for the hackathon, but production needs an approved API account and data agreement.
- **Permissions:** the build service needs repo read access, and work item write access on the target project only.
- **Cost and noise:** running only on tags keeps the number of runs small. Log tokens per run (from the CLI output) to the pipeline summary.
- **Live code, no cutoff:** the as-of-date cutoff was only for the hindsight test. In live use, the pipeline reads the default branch.

## Hackathon slice vs next steps
1. **Today (demo):** run the local script on one **test feature**: snapshot → repos from tags → headless run → attach the .md and add a comment. This proves steps 1–4 end to end.
2. **Next:** pipeline YAML + service hook + secret, so the same script runs in ADO.
3. **Then:** the "Pre-Flight" page (tab) in the process, once a process admin agrees. The pipeline writes HTML to that field.

## Finding, 5 Nov
- `setup_tab.py` returned **403 VS402356** (no "Edit process" permission on Nordic Agile - v2). Nothing was created. The tab needs a process admin.
- Interim output: `publish --attach-html` attaches a standalone HTML page of the same v0.3 view (summary, by role, collapsible details). It was published to 431577 as `preflight-431577-2026-11-05.html` (live-02 run).
