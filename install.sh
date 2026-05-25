#!/bin/sh
# install.sh - automatyczna instalacja BSO Scanner na MikroTik RouterOS
# Uruchamiane przez SSH na routerze MikroTik

set -e

# === KONFIGURACJA - uzytkownik moze zmienic przed uruchomieniem ===
DOCKER_IMAGE="${DOCKER_IMAGE:-jakubm3/bso-scanner:latest}"
# SCAN_SUBNET jest opcjonalny - jesli nie podany, kontener wykryje podsiec
# automatycznie pytajac MikroTik REST API o adresy IP routera.
SCAN_SUBNET="${SCAN_SUBNET:-}"
MIKROTIK_USER="${MIKROTIK_USER:-admin}"
MIKROTIK_PASS="${MIKROTIK_PASS:-}"
SCAN_TYPE="${SCAN_TYPE:-quick}"
EMAIL_TO="${EMAIL_TO:-}"
SMTP_USER="${SMTP_USER:-}"
SMTP_PASS="${SMTP_PASS:-}"
SMTP_SERVER="${SMTP_SERVER:-smtp.gmail.com}"
SMTP_PORT="${SMTP_PORT:-587}"
REPORT_FORMAT="${REPORT_FORMAT:-html}"
SCAN_INTERVAL="${SCAN_INTERVAL:-24h}"

if [ -z "$EMAIL_TO" ] || [ -z "$SMTP_USER" ] || [ -z "$SMTP_PASS" ]; then
    echo "BLAD: Ustaw zmienne EMAIL_TO, SMTP_USER, SMTP_PASS przed uruchomieniem"
    echo "Przyklad: EMAIL_TO=ja@gmail.com SMTP_USER=ja@gmail.com SMTP_PASS=apppass MIKROTIK_PASS=routerpass sh install.sh"
    exit 1
fi

if [ -z "$SCAN_SUBNET" ] && [ -z "$MIKROTIK_PASS" ]; then
    echo "BLAD: Ustaw MIKROTIK_PASS (do auto-detekcji podsieci) albo recznie SCAN_SUBNET"
    exit 1
fi

echo "================================================"
echo "BSO Scanner - automatyczna instalacja"
echo "================================================"
echo "Docker image:  $DOCKER_IMAGE"
if [ -n "$SCAN_SUBNET" ]; then
    echo "Skanowana siec: $SCAN_SUBNET (recznie)"
else
    echo "Skanowana siec: AUTO-DETECT (przez MikroTik REST API)"
fi
echo "Email:         $EMAIL_TO"
echo "Interwal:      $SCAN_INTERVAL"
echo "================================================"

CMD="/container/add remote-image=$DOCKER_IMAGE interface=veth1 root-dir=/tmp/scanner start-on-boot=no logging=yes"

ENV_VARS="MIKROTIK_USER=$MIKROTIK_USER,MIKROTIK_PASS=$MIKROTIK_PASS,SCAN_TYPE=$SCAN_TYPE,EMAIL_TO=$EMAIL_TO,SMTP_USER=$SMTP_USER,SMTP_PASS=$SMTP_PASS,SMTP_SERVER=$SMTP_SERVER,SMTP_PORT=$SMTP_PORT,REPORT_FORMAT=$REPORT_FORMAT"
if [ -n "$SCAN_SUBNET" ]; then
    ENV_VARS="SCAN_SUBNET=$SCAN_SUBNET,$ENV_VARS"
fi

echo ""
echo "Wykonaj na MikroTiku przez SSH ponizsze komendy:"
echo ""
echo "1. Upewnij sie ze REST API jest wlaczone (HTTP service):"
echo "   /ip/service/enable www"
echo ""
echo "2. Dodanie kontenera:"
echo "   $CMD"
echo ""
echo "3. Ustawienie zmiennych srodowiskowych (przez WinBox -> Containers -> Env):"
echo "   $ENV_VARS"
echo ""
echo "4. Dodanie schedulera (skan co $SCAN_INTERVAL):"
echo "   /system/scheduler/add name=bso-scan interval=$SCAN_INTERVAL on-event=\"/container/start [find tag~\\\"bso-scanner\\\"]\""
echo ""
echo "5. Pierwsze uruchomienie:"
echo "   /container/start [find tag~\"bso-scanner\"]"
echo ""
echo "Gotowe!"
