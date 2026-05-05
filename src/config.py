import os
import sys

SCAN_PROFILES = {
    "quick":    "-F -sV",
    "standard": "-sV -sC",
    "full":     "-p- -sV --script vuln",
    "stealth":  "-sS -sV",
}

def load_config():
    cfg = {}

    cfg["subnet"] = os.environ.get("SCAN_SUBNET")
    if not cfg["subnet"]:
        print("ERROR: SCAN_SUBNET nie ustawiona", file=sys.stderr)
        return None

    cfg["email_to"] = os.environ.get("EMAIL_TO")
    if not cfg["email_to"]:
        print("ERROR: EMAIL_TO nie ustawiona", file=sys.stderr)
        return None

    scan_type = os.environ.get("SCAN_TYPE", "standard")
    if scan_type not in SCAN_PROFILES:
        print(f"ERROR: Nieznany SCAN_TYPE: {scan_type}", file=sys.stderr)
        return None
    cfg["scan_flags"] = SCAN_PROFILES[scan_type]
    cfg["scan_type"] = scan_type

    cfg["nse_scripts"] = os.environ.get("NSE_SCRIPTS", "vuln,safe")
    cfg["nmap_extra"]  = os.environ.get("NMAP_EXTRA_ARGS", "")

    cfg["smtp_server"] = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    cfg["smtp_port"]   = int(os.environ.get("SMTP_PORT", "587"))
    cfg["smtp_user"]   = os.environ.get("SMTP_USER")
    cfg["smtp_pass"]   = os.environ.get("SMTP_PASS")

    if not cfg["smtp_user"] or not cfg["smtp_pass"]:
        print("ERROR: SMTP_USER lub SMTP_PASS nie ustawione", file=sys.stderr)
        return None

    cfg["report_format"] = os.environ.get("REPORT_FORMAT", "txt")
    cfg["results_dir"]   = "/tmp"

    return cfg