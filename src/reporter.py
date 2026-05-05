from datetime import datetime

SEVERITY_COLORS = {
    "CRITICAL": "#d32f2f",
    "HIGH":     "#f57c00",
    "MEDIUM":   "#fbc02d",
    "LOW":      "#388e3c",
}

def generate_txt(findings, diff, cfg):
    lines = []
    lines.append("=" * 60)
    lines.append("RAPORT SKANOWANIA SIECI - BSO N02")
    lines.append("=" * 60)
    lines.append(f"Data:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Sieć:        {cfg['subnet']}")
    lines.append(f"Profil:      {cfg['scan_type']}")
    lines.append(f"NSE:         {cfg['nse_scripts']}")
    lines.append("")

    if diff["first_run"]:
        lines.append("[i] Pierwsze uruchomienie - brak porownania.")
    else:
        lines.append(f"[i] Nowe znaleziska od ostatniego skanu: {len(diff['new'])}")
    lines.append("")

    by_severity = {}
    for f in findings:
        by_severity.setdefault(f["severity"], []).append(f)

    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        items = by_severity.get(sev, [])
        if not items:
            continue
        lines.append(f"--- {sev} ({len(items)}) ---")
        for f in items:
            host = f"{f['ip']}" + (f" ({f['hostname']})" if f['hostname'] else "")
            svc = f"{f['service']} {f['product']} {f['version']}".strip()
            lines.append(f"  [{f['severity']}] {host} :{f['port']}/{f['protocol']} {svc}")
            lines.append(f"           Powod: {f['reason']}")
            for nse in f["nse"]:
                lines.append(f"           NSE [{nse['id']}]: {nse['output'][:100]}")
        lines.append("")

    return "\n".join(lines)

def generate_html(findings, diff, cfg):
    html = []
    html.append("<!DOCTYPE html><html><head><meta charset='utf-8'>")
    html.append("<style>")
    html.append("body{font-family:Arial,sans-serif;max-width:900px;margin:20px auto;padding:20px;}")
    html.append("h1{border-bottom:3px solid #333;padding-bottom:10px;}")
    html.append(".meta{background:#f5f5f5;padding:15px;border-radius:5px;margin:15px 0;}")
    html.append(".finding{padding:10px;margin:8px 0;border-left:5px solid;border-radius:3px;}")
    html.append(".CRITICAL{background:#ffebee;border-color:#d32f2f;}")
    html.append(".HIGH{background:#fff3e0;border-color:#f57c00;}")
    html.append(".MEDIUM{background:#fffde7;border-color:#fbc02d;}")
    html.append(".LOW{background:#e8f5e9;border-color:#388e3c;}")
    html.append(".badge{display:inline-block;padding:2px 8px;color:white;border-radius:3px;font-weight:bold;font-size:11px;}")
    html.append("</style></head><body>")
    html.append("<h1>Raport skanowania sieci - BSO N02</h1>")

    html.append("<div class='meta'>")
    html.append(f"<b>Data:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>")
    html.append(f"<b>Sieć:</b> {cfg['subnet']}<br>")
    html.append(f"<b>Profil:</b> {cfg['scan_type']}<br>")
    html.append(f"<b>NSE:</b> {cfg['nse_scripts']}<br>")
    if diff["first_run"]:
        html.append("<b>Status:</b> Pierwsze uruchomienie")
    else:
        html.append(f"<b>Nowe znaleziska:</b> {len(diff['new'])}")
    html.append("</div>")

    for f in findings:
        color = SEVERITY_COLORS[f["severity"]]
        host = f"{f['ip']}" + (f" ({f['hostname']})" if f['hostname'] else "")
        svc = f"{f['service']} {f['product']} {f['version']}".strip()

        html.append(f"<div class='finding {f['severity']}'>")
        html.append(f"<span class='badge' style='background:{color}'>{f['severity']}</span> ")
        html.append(f"<b>{host}</b> :{f['port']}/{f['protocol']} - {svc}<br>")
        html.append(f"<small>{f['reason']}</small>")
        for nse in f["nse"]:
            html.append(f"<br><small><code>NSE [{nse['id']}]: {nse['output'][:200]}</code></small>")
        html.append("</div>")

    html.append("</body></html>")
    return "\n".join(html)

def generate_report(findings, diff, cfg):
    if cfg["report_format"] == "html":
        return generate_html(findings, diff, cfg), "html"
    return generate_txt(findings, diff, cfg), "txt"