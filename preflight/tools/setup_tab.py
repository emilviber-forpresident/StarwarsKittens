"""One-time setup for a PROCESS ADMIN: adds a 'Pre-Flight' tab with a rich-text field to the
Feature form of the inherited process 'Nordic Agile - v2' (used only by project IHCP).
Run:  python -I setup_tab.py      (needs 'Edit process' permission; idempotent; undo by removing the page/field)
"""
import sys
from preflight_ado import call
O = "https://dev.azure.com/tunstallgroup"
P, W = "1bf81e2e-2801-48b9-bbf7-97bf12f45fd1", "NordicAgile-v2.Feature"
B = f"{O}/_apis/work/processes/{P}/workItemTypes/{W}"

def main():
    try:
        call("GET", f"{O}/_apis/wit/fields/Custom.PreFlight?api-version=7.1")
    except Exception:
        call("POST", f"{O}/_apis/wit/fields?api-version=7.1",
             {"name": "PreFlight", "referenceName": "Custom.PreFlight", "type": "html", "usage": "workItem",
              "description": "Padawan Pre-Flight: AI pre-refinement analysis"})
    call("POST", f"{B}/fields?api-version=7.1", {"referenceName": "Custom.PreFlight"})
    pages = call("GET", f"{B}/layout?api-version=7.1")["pages"]
    page = next((p for p in pages if p["label"] == "Pre-Flight"), None) or \
        call("POST", f"{B}/layout/pages?api-version=7.1", {"label": "Pre-Flight", "pageType": "custom", "visible": True})
    if not any(c["id"] == "Custom.PreFlight" for s in page["sections"] for g in s.get("groups") or [] for c in g.get("controls") or []):
        call("POST", f"{B}/layout/pages/{page['id']}/sections/{page['sections'][0]['id']}/groups?api-version=7.1",
             {"label": "Pre-Flight", "visible": True,
              "controls": [{"id": "Custom.PreFlight", "label": "Pre-Flight", "visible": True}]})
    print("Pre-Flight tab ready. Publish with: preflight_ado.py publish <id> <run> --field Custom.PreFlight --comment")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
