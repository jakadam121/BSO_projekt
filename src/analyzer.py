DANGEROUS_SERVICES = {"ftp", "telnet", "http", "rsh", "rlogin"}
SENSITIVE_PORTS = {"3306", "5432", "6379", "27017", "1433", "5984"}

def analyze(hosts):
    findings = []

    for host in hosts:
        for port in host["ports"]:
            severity = "LOW"
            reason = ""

            nse_vulnerable = any(
                "VULNERABLE" in nse["output"].upper()
                for nse in port["nse"]
            )

            if nse_vulnerable:
                severity = "CRITICAL"
                reason = "NSE wykryl podatnosc"
            elif port["service"].lower() in DANGEROUS_SERVICES:
                severity = "HIGH"
                reason = f"Nieszyfrowany protokol: {port['service']}"
            elif port["port"] in SENSITIVE_PORTS:
                severity = "MEDIUM"
                reason = f"Wrazliwa usluga (baza danych): port {port['port']}"
            else:
                reason = "Otwarty port"

            findings.append({
                "ip": host["ip"],
                "hostname": host["hostname"],
                "port": port["port"],
                "protocol": port["protocol"],
                "service": port["service"],
                "product": port["product"],
                "version": port["version"],
                "severity": severity,
                "reason": reason,
                "nse": port["nse"],
            })

    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    findings.sort(key=lambda f: (severity_order[f["severity"]], f["ip"], int(f["port"])))

    return findings