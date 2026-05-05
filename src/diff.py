import os
import json

LAST_SCAN_FILE = "/tmp/last_scan.json"

def save_current(findings):
    snapshot = [
        {"ip": f["ip"], "port": f["port"], "service": f["service"]}
        for f in findings
    ]
    with open(LAST_SCAN_FILE, "w") as f:
        json.dump(snapshot, f)

def compare_scans(findings):
    if not os.path.exists(LAST_SCAN_FILE):
        save_current(findings)
        return {"new": [], "first_run": True}

    with open(LAST_SCAN_FILE) as f:
        previous = json.load(f)

    prev_set = {(p["ip"], p["port"]) for p in previous}
    curr_set = {(f["ip"], f["port"]) for f in findings}

    new_entries = curr_set - prev_set
    new_findings = [
        f for f in findings
        if (f["ip"], f["port"]) in new_entries
    ]

    save_current(findings)

    return {"new": new_findings, "first_run": False}