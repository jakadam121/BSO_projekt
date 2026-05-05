#!/bin/sh
# install.sh - automatyczna instalacja BSO Scanner na MikroTik RouterOS
# Uruchamiane przez SSH na routerze MikroTik

set -e

# === KONFIGURACJA - uzytkownik moze zmienic przed uruchomieniem ===
DOCKER_IMAGE="${DOCKER_IMAGE:-sadjgasjdg/bso-scanner-v2:latest}"
SCAN_SUBNET="${SCAN_SUBNET:-192.168.40.0/24}"
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
    echo "Przyklad: EMAIL_TO=ja@gmail.com SMTP_USER=ja@gmail.com SMTP_PASS=apppass sh install.sh"
    exit 1
fi

echo "================================================"
echo "BSO Scanner - automatyczna instalacja"
echo "================================================"
echo "Docker image:  $DOCKER_IMAGE"
echo "Skanowana siec: $SCAN_SUBNET"
echo "Email:         $EMAIL_TO"
echo "Interwal:      $SCAN_INTERVAL"
echo "================================================"

CMD="/container/add remote-image=$DOCKER_IMAGE interface=veth1 root-dir=/tmp/scanner start-on-boot=no logging=yes"

echo ""
echo "Wykonaj na MikroTiku przez SSH ponizsze komendy:"
echo ""
echo "1. Dodanie kontenera:"
echo "   $CMD"
echo ""
echo "2. Ustawienie zmiennych srodowiskowych (przez WinBox -> Containers -> Env):"
echo "   SCAN_SUBNET=$SCAN_SUBNET"
echo "   SCAN_TYPE=$SCAN_TYPE"
echo "   EMAIL_TO=$EMAIL_TO"
echo "   SMTP_USER=$SMTP_USER"
echo "   SMTP_PASS=$SMTP_PASS"
echo "   SMTP_SERVER=$SMTP_SERVER"
echo "   SMTP_PORT=$SMTP_PORT"
echo "   REPORT_FORMAT=$REPORT_FORMAT"
echo ""
echo "3. Dodanie schedulera (skan co $SCAN_INTERVAL):"
echo "   /system/scheduler/add name=bso-scan interval=$SCAN_INTERVAL on-event=\"/container/start [find tag~\\\"bso-scanner\\\"]\""
echo ""
echo "4. Pierwsze uruchomienie:"
echo "   /container/start [find tag~\"bso-scanner\"]"
echo ""
echo "Gotowe!"