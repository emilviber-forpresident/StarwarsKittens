# Padawan Pre-Flight: how to run it

The example is Feature **404917, TES App staff security step 2**, ticket only (no code).

## Folder layout
Run folders live **next to** the team repo, not inside it, so the tool can't see our notes or answers:
```
C:\source\TunstallHackathonAI\
  StarwarsKittens\                 ← team repo (prompts, snapshots, notes)
  preflight-runs\
    404917-run-01\
      prompts\                     ← copy of StarwarsKittens\preflight\prompts
      input\feature.md             ← copy of StarwarsKittens\runs\404917\input\feature.md
      output\                      ← the tool writes here
```
`404917-run-01` is already set up.

## Run 1: just see what it does
1. Open a **new** terminal in the run folder and start the tool there:
   ```
   cd C:\source\TunstallHackathonAI\preflight-runs\404917-run-01
   claude
   ```
   (Codex: `codex` in the same folder.)
2. Type:
   `Read prompts/00-runner.md and run Pre-Flight.`
3. When it's done, type `/cost` (or `/usage`) and copy the token numbers. In Codex, use `/status`.
4. Copy `output\preflight.md` to `StarwarsKittens\runs\404917\run-01-output.md`.
5. Read it together and talk it through (about 20 min). Write a few lines in `runs\404917\run-01-notes.md`.

## Run 2 and later
1. Agree on **one** thing to change, based on the conversation. Usually it's a prompt file in `StarwarsKittens\preflight\prompts`.
2. Write one line about it in `docs\prompt-log.md`: what you changed and why.
3. Make a fresh run folder (PowerShell):
   ```powershell
   $n = "02"; $f = "404917"
   $r = "C:\source\TunstallHackathonAI\preflight-runs\$f-run-$n"
   New-Item -ItemType Directory -Force "$r\input", "$r\output" | Out-Null
   Copy-Item -Recurse C:\source\TunstallHackathonAI\StarwarsKittens\preflight\prompts $r
   Copy-Item C:\source\TunstallHackathonAI\StarwarsKittens\runs\$f\input\feature.md "$r\input"
   ```
4. Repeat steps 1–5 of run 1, using `run-02` in the file names.

## With code (step 2)
Pre-Flight **doesn't read git URLs**. Step 2 runs only when the run folder has local code in `repos\`. The code must be at a commit from **before development** (4 Mar 2026 for 404917), with **no `.git` folder**, so the tool can't see later fixes in the history. To set this up (Git Bash):
```bash
bash StarwarsKittens/preflight/tools/add-repos.sh preflight-runs/404917-run-02 2026-03-04 \
  https://dev.azure.com/tunstallgroup/IHCP/_git/AlarmServer.Swamp \
  https://dev.azure.com/tunstallgroup/IHCP/_git/AlarmServer.Database \
  https://dev.azure.com/tunstallgroup/IHCP/_git/AlarmServer.Koala \
  https://dev.azure.com/tunstallgroup/IHCP/_git/AlarmServer.Web
```
The colleague using Codex does the same with the TES app repo URLs added.

## Two rules worth keeping, even when it's informal
- **Same input every run.** Never edit `input\feature.md`, so runs stay comparable.
- **One change per run**, written down. Otherwise we can't tell what helped.
