# 003: Run Pre-Flight from Azure DevOps (demo slice)

Date: 5 Nov 2026 · Status: **Accepted** (team) · Design: [docs/ado-integration.md](../docs/ado-integration.md)

## Context
The team wants Pre-Flight to run on features in Azure DevOps, pick up repos from tags, and show its output on the feature, ideally as its own tab.

## Decision
- **Trigger:** manual for now. The tag `preflight` is added to the feature, and later a service hook will fire the pipeline. We don't trigger on "created", because new features are often empty.
- **Repo context:** feature tags `repo:<repo-name>`. Live runs read the default branch, shallow-cloned, with no git history.
- **First live case:** 431577 TSP Client Integration, tagged `preflight; repo:ihcp; repo:tes` on 5 Nov.
- **Output:** a **Pre-Flight tab**, which is a custom page plus the rich-text field `Custom.PreFlight` in the process "Nordic Agile - v2" (used only by IHCP). The team approved it, but **we lacked process permission (VS402356)**. For the demo, the output is a **comment with the Top 3 plus a `.md` attachment**. The tab setup is ready for a process admin: `preflight/tools/setup_tab.py`.
- **Runtime:** headless `claude -p` with Read, Grep, Glob and Write tools only (no shell or web). The same prompts work with `codex exec`.

- **Demo of the tab (5 Nov):** `preflight_ado.py preview <id> <run>` renders a local page shaped like the feature form, with a Pre-Flight tab holding exactly the HTML that `publish --field Custom.PreFlight` would write. This is honest about the gap: it's the real content, but not yet in Azure DevOps.
- **Repo context is now automatic:** `prepare` clones every `repo:<name>` tag (shallow, `.git` removed). In the pilot, the repos were cloned by hand from the team's input file, and the tags only confirmed them.

## Learnings (Beyond the happy path)
- Field names in Azure DevOps can't contain `-` ("Pre-Flight" was rejected, so we use "PreFlight").
- Changing a process needs org-level rights the dev team doesn't have. The tab is an admin request, not a dev task.
- No predecessor feature is linked to 431577. If the "nearly completed" earlier feature should give context, it needs a link (Related), and the snapshot must follow it.
