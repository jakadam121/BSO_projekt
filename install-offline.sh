#!/bin/sh
# install-offline.sh - instalacja BSO Scanner na MikroTik bez internetu
# Wymaga plikow: bso-scanner.tar, bso-config.rsc

set -e

MIKROTIK_IP="${MIKROTIK_IP:-192.168.40.2}"
MIKROTIK_USER="${MIKROTIK_USER:-admin}"

if [ ! -f "bso-scanner.tar" ] || [ ! -f "bso-config.rsc" ]; then
    echo "BLAD: brak plikow bso-scanner.tar lub bso-config.rsc"
    exit 1
fi

echo "================================================"
echo "BSO Scanner - instalacja offline"
echo "================================================"
echo "MikroTik:  $MIKROTIK_USER@$MIKROTIK_IP"
echo "================================================"

echo ""
echo "[1/3] Wysylanie obrazu Docker (26 MB) na MikroTika..."
scp bso-scanner.tar $MIKROTIK_USER@$MIKROTIK_IP:/

echo ""
echo "[2/3] Wysylanie konfiguracji na MikroTika..."
scp bso-config.rsc $MIKROTIK_USER@$MIKROTIK_IP:/

echo ""
echo "[3/3] Importowanie konfiguracji i ladowanie obrazu..."
ssh $MIKROTIK_USER@$MIKROTIK_IP "/import file-name=bso-config.rsc"

echo ""
echo "================================================"
echo "GOTOWE!"
echo "================================================"
echo ""
echo "Aby uruchomic skan recznie, wpisz na MikroTiku:"
echo "  /container/start [find tag~\"bso-scanner\"]"
echo ""
echo "Skaner i tak uruchomi sie automatycznie co 24h (scheduler)."