#!/usr/bin/env bash
set -e

# Huop — Installation automatique
OWNER="adriop-45"; REPO="Huop"
BASES=(
    "https://raw.githubusercontent.com/${OWNER}/${REPO}/main"
    "https://github.com/${OWNER}/${REPO}/raw/main"
)

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'; CYAN='\033[0;36m'
WHITE='\033[0;97m'; GRAY='\033[0;90m'; RST='\033[0m'

echo -e "\n  ${CYAN}╔══════════════════════════════════════════════════════╗${RST}"
echo -e "              ${WHITE}Huop — Installation automatique${RST}"
echo -e "  ${CYAN}╚══════════════════════════════════════════════════════╝${RST}\n"

[[ $EUID -eq 0 ]] || { echo -e "  ${RED}✗${RST} Root requis."; exit 1; }

os_id=$(grep ^ID= /etc/os-release 2>/dev/null | cut -d= -f2 | tr -d '"')
[[ "$os_id" =~ ^(debian|ubuntu)$ ]] || { echo -e "  ${RED}✗${RST} Debian/Ubuntu seulement."; exit 1; }

# Telechargement multi-miroirs : IPv4 force, reprises, erreurs visibles.
dl() {
    local rel="$1" out="$2" mins="${3:-1024}" base rc
    for base in "${BASES[@]}"; do
        echo -e "  ${GRAY}→ Source : ${base}/${rel}${RST}"
        rm -f "$out"
        rc=0
        curl -4 -fsSL --retry 3 --retry-delay 2 --connect-timeout 15 --max-time 900 \
             "${base}/${rel}" -o "$out" || rc=$?
        if [[ $rc -eq 0 && -s "$out" ]]; then
            local sz; sz=$(stat -c%s "$out" 2>/dev/null || echo 0)
            if (( sz >= mins )); then return 0; fi
            echo -e "  ${YELLOW}✗ Fichier tronque (${sz} octets < ${mins}) — miroir suivant...${RST}"
        else
            echo -e "  ${YELLOW}✗ Echec curl (code ${rc}) — miroir suivant...${RST}"
        fi
    done
    echo -e "  ${RED}✗ Téléchargement impossible : ${rel}${RST}"
    exit 1
}

require_elf() {
    [[ "$(head -c4 "$1" 2>/dev/null)" == $'\x7fELF' ]] || {
        echo -e "  ${RED}✗ Fichier invalide reçu (${1}) — abandon."; exit 1; }
}

export DEBIAN_FRONTEND=noninteractive
echo -e "  ${YELLOW}→${RST} Mise à jour des paquets..."
apt-get update -qq
echo -e "  ${YELLOW}→${RST} Installation des dépendances..."
apt-get install -y -qq curl git sqlite3 openssl screen nftables jq unzip python3 vnstat 2>/dev/null

case "$(uname -m)" in
    x86_64|amd64)  BIN_NAME="install2.bin";      MIN_SZ=20000000 ;;
    aarch64|arm64) BIN_NAME="install2-arm64.bin"; MIN_SZ=20000000 ;;
    *) echo -e "  ${RED}✗${RST} Architecture non supportée : $(uname -m)"; exit 1 ;;
esac

BIN="/usr/local/bin/kighmu"
echo -e "  ${YELLOW}→${RST} Téléchargement du binaire (${BIN_NAME})..."
dl "${BIN_NAME}" "$BIN" "$MIN_SZ"
require_elf "$BIN"
chmod 700 "$BIN"

echo -e "  ${GREEN}✓${RST} Lancement du panneau..."
"$BIN" --install
