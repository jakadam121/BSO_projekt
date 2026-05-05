import xml.etree.ElementTree as ET

def parse_nmap_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    hosts = []
    for host in root.findall("host"):
        status = host.find("status")
        if status is None or status.get("state") != "up":
            continue

        ip = ""
        for addr in host.findall("address"):
            if addr.get("addrtype") == "ipv4":
                ip = addr.get("addr")
                break

        hostname = ""
        hostnames = host.find("hostnames")
        if hostnames is not None:
            hn = hostnames.find("hostname")
            if hn is not None:
                hostname = hn.get("name", "")

        ports = []
        ports_elem = host.find("ports")
        if ports_elem is not None:
            for port in ports_elem.findall("port"):
                state = port.find("state")
                if state is None or state.get("state") != "open":
                    continue

                port_id = port.get("portid")
                protocol = port.get("protocol")
                service_elem = port.find("service")
                service = ""
                product = ""
                version = ""
                if service_elem is not None:
                    service = service_elem.get("name", "")
                    product = service_elem.get("product", "")
                    version = service_elem.get("version", "")

                nse_results = []
                for script in port.findall("script"):
                    nse_results.append({
                        "id": script.get("id", ""),
                        "output": script.get("output", "")
                    })

                ports.append({
                    "port": port_id,
                    "protocol": protocol,
                    "service": service,
                    "product": product,
                    "version": version,
                    "nse": nse_results,
                })

        hosts.append({
            "ip": ip,
            "hostname": hostname,
            "ports": ports,
        })

    return hosts