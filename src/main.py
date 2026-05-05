import sys
from config import load_config
from scanner import run_scan
from parser import parse_nmap_xml
from analyzer import analyze
from diff import compare_scans
from reporter import generate_report
from mailer import send_report

def main():
    print("=" * 50)
    print("BSO N02 - Skaner sieci")
    print("=" * 50)

    cfg = load_config()
    if cfg is None:
        sys.exit(1)

    xml_path = run_scan(cfg)
    if xml_path is None:
        sys.exit(1)

    hosts = parse_nmap_xml(xml_path)
    print(f"Wykryto {len(hosts)} aktywnych hostow")

    findings = analyze(hosts)
    print(f"Znaleziono {len(findings)} problemow")

    diff = compare_scans(findings)

    report, fmt = generate_report(findings, diff, cfg)
    send_report(report, fmt, cfg)

    print("Gotowe!")

if __name__ == "__main__":
    main()