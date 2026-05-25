"""
Auto-wykrywanie podsieci LAN do skanowania.

Kontener siedzi w izolowanej sieci 172.17.0.0/24 za bridgem na routerze.
Brama domyslna (172.17.0.1) to interfejs routera na bridge - ale to nie jest
adres LAN, ktory chcemy skanowac.

Rozwiazanie: pytamy router przez jego REST API o liste wszystkich adresow IP.
Wybieramy adres, ktory NIE jest naszej sieci kontenera - to jest IP routera w LAN.
Z tego adresu wyciagamy podsiec.
"""

import json
import socket
import struct
import sys
import urllib.error
import urllib.request
import base64


def _get_default_gateway():
    """Czyta /proc/net/route i zwraca IP bramy domyslnej (czyli routera)."""
    try:
        with open("/proc/net/route") as f:
            for line in f.readlines()[1:]:
                fields = line.strip().split()
                if fields[1] == "00000000":  # destination 0.0.0.0
                    gw_hex = fields[2]
                    gw_bytes = bytes.fromhex(gw_hex)
                    return socket.inet_ntoa(gw_bytes[::-1])
    except Exception as e:
        print(f"ERROR: nie moge przeczytac /proc/net/route: {e}", file=sys.stderr)
    return None


def _get_own_ip(gateway):
    """Zwraca IP kontenera w sieci, w ktorej jest gateway."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect((gateway, 1))
        return s.getsockname()[0]
    finally:
        s.close()


def _network_from_ip_prefix(ip, prefix):
    """Z IP + prefiksu (np. '192.168.40.2' + 24) zwraca '192.168.40.0/24'."""
    ip_int = struct.unpack(">I", socket.inet_aton(ip))[0]
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    network_int = ip_int & mask
    network = socket.inet_ntoa(struct.pack(">I", network_int))
    return f"{network}/{prefix}"


def _query_mikrotik_api(gateway, user, password, timeout=10):
    """
    Pyta MikroTik REST API o liste adresow IP routera.
    Zwraca liste slownikow z polami 'address' (np. '192.168.40.2/24') i 'interface'.

    Wymaga RouterOS 7.1+ z wlaczonym serwisem www albo www-ssl.
    """
    url = f"http://{gateway}/rest/ip/address"
    auth = base64.b64encode(f"{user}:{password}".encode()).decode()
    req = urllib.request.Request(url, headers={"Authorization": f"Basic {auth}"})

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"ERROR: MikroTik API zwrocilo HTTP {e.code}", file=sys.stderr)
    except urllib.error.URLError as e:
        print(f"ERROR: nie moge polaczyc sie z MikroTik API: {e.reason}", file=sys.stderr)
    except Exception as e:
        print(f"ERROR: blad MikroTik API: {e}", file=sys.stderr)
    return None


def discover_lan_subnet(mikrotik_user, mikrotik_pass):
    """
    Glowna funkcja: wykrywa podsiec LAN do skanowania.

    Zwraca string typu '192.168.40.0/24' albo None jesli sie nie udalo.
    """
    gateway = _get_default_gateway()
    if not gateway:
        print("ERROR: nie moge ustalic bramy domyslnej", file=sys.stderr)
        return None
    print(f"Brama domyslna (router): {gateway}")

    own_ip = _get_own_ip(gateway)
    print(f"Moj IP w sieci kontenera: {own_ip}")

    addresses = _query_mikrotik_api(gateway, mikrotik_user, mikrotik_pass)
    if not addresses:
        return None

    # Szukamy adresu routera ktory NIE jest w sieci kontenera.
    # Sprawdzamy tez czy interfejs nie jest naszym bridge.
    own_network_prefix = ".".join(own_ip.split(".")[:3])

    for entry in addresses:
        addr = entry.get("address", "")
        disabled = entry.get("disabled", "false") == "true"
        if disabled or "/" not in addr:
            continue

        ip_part = addr.split("/")[0]
        # pomijamy adres routera w sieci kontenera
        if ip_part.startswith(own_network_prefix + "."):
            continue
        # pomijamy adresy loopback i link-local
        if ip_part.startswith("127.") or ip_part.startswith("169.254."):
            continue

        prefix = int(addr.split("/")[1])
        # za szeroka maska = pewnie WAN, pomijamy
        if prefix < 16:
            continue

        subnet = _network_from_ip_prefix(ip_part, prefix)
        print(f"Wykryto LAN routera: {addr} (interfejs: {entry.get('interface', '?')})")
        print(f"Podsiec do skanowania: {subnet}")
        return subnet

    print("ERROR: nie znalazlem zadnego adresu LAN na routerze", file=sys.stderr)
    return None
