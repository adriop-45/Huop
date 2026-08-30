<div align="center">

# Huop

**Panel professionnel de gestion de tunnels VPN**
*Installation en une commande · Debian · Ubuntu · x86_64 / ARM64*

<br/>

![Version](https://img.shields.io/badge/version-V3.9.9-00FFCC?style=for-the-badge)
![Platform](https://img.shields.io/badge/platform-Debian%20%7C%20Ubuntu-1f425f?style=for-the-badge&logo=debian&logoColor=white)
![Arch](https://img.shields.io/badge/arch-x86__64%20%7C%20ARM64-blue?style=for-the-badge&logo=linux&logoColor=white)
![License](https://img.shields.io/badge/license-Commercial-FF6FCF?style=for-the-badge)
![Status](https://img.shields.io/badge/status-stable-success?style=for-the-badge)

<br/>

**Un panneau unique pour déployer, superviser et gérer un parc complet de tunnels VPN — avec persistance après reboot, bot Telegram intégré, et système multi-revendeurs.**

<br/>

[Telegram Support](https://t.me/kighmu) · [Buy a License](https://t.me/kighmu) · [Tunnels](#-tunnels-supportés) · [Install](#-installation-rapide) · [Features](#-fonctionnalités)

</div>

---

## 📑 Table des matières

- [⚡ Aperçu](#-aperçu)
- [📦 Prérequis](#-prérequis)
- [🚀 Installation rapide](#-installation-rapide)
- [🔧 Tunnels supportés](#-tunnels-supportés)
- [🧩 Architecture](#-architecture)
- [💎 Fonctionnalités](#-fonctionnalités)
- [🔐 Licence](#-licence)
- [🛟 Support](#-support)
- [📜 Crédits](#-crédits)

---

## ⚡ Aperçu

Huop est un panneau d'administration VPS **tout-en-un** conçu pour les
revendeurs et les administrateurs qui veulent un outil unique, stable,
persistant après reboot, et pilotable en ligne de commande **comme**
via Telegram.

Pensé pour des installations de production :
- **Zéro dépendance externe** au runtime (binaire statique, autocontenu)
- **Persistance triple-redondante** (systemd timer + cron + daemon)
- **Validation de licence liée au matériel** (anti-piratage)
- **Rollback automatique** en cas de crash d'un service (watchdogs 1 min)
- **Multi-tenants** via système de revendeurs intégrés

```
┌──────────────────────────────────────────────────────────────────┐
│                          VPS / Serveur                            │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐  │
│  │ Xray      │  │ Hysteria   │  │ ZIVPN      │  │ SlowDNS    │  │
│  │ 443/8880  │  │ 20000-50000│  │ 5667/6k-20k│  │ 53         │  │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  │
│        │               │               │               │         │
│  ┌─────┴───────────────┴───────────────┴───────────────┴──────┐  │
│  │                    HAProxy (TLS termination)               │  │
│  └─────┬──────────────────────────────────────────────────────┘  │
│        │                                                          │
│  ┌─────┴──────┐  ┌──────────┐  ┌──────────┐  ┌─────────────┐     │
│  │ Dropbear  │  │ SSH-WS   │  │ SSL/TLS  │  │ BadVPN UDPGW│     │
│  │ 109       │  │ 80       │  │ 444      │  │ 7100-7300   │     │
│  └────────────┘  └──────────┘  └──────────┘  └─────────────┘     │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Huop Panel (binaire statique  →  /usr/local/bin/kighmu)   │ │
│  │  + Telegram Bot  + License watchdog  + Quota trackers       │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📦 Prérequis

Avant l'installation, mettre à jour le système :

```bash
apt update && apt upgrade -y
```

> 💡 Si le noyau a été mis à jour, **redémarrer** avant l'installation :
> ```bash
> reboot
> ```
> Attendre ~30 secondes avant de vous reconnecter.

**Exigences minimales** :

| Ressource | Minimum | Recommandé |
|---|---|---|
| **OS** | Debian 11 / Ubuntu 20.04 | Debian 12 / Ubuntu 22.04 |
| **RAM** | 512 MB | 1 GB+ |
| **CPU** | 1 vCPU | 2 vCPU+ |
| **Disque** | 2 GB libre | 5 GB+ |
| **Réseau** | IPv4 publique | IPv4 + IPv6 |
| **Accès** | `root` (SSH ou console) | — |

---

## 🚀 Installation rapide

**One-liner** (recommandé) :

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/adriop-45/Huop/main/install.sh)
```

**Méthode manuelle** (clone direct) :

```bash
git clone https://github.com/adriop-45/Huop.git
cd Huop
chmod +x install.sh
./install.sh
```

Le script :

1. ✅ Détecte automatiquement l'architecture (`x86_64` ou `ARM64`)
2. ✅ Télécharge le binaire compilé correspondant (29 MB / 27 MB)
3. ✅ Valide l'intégrité (signature ELF + taille minimale)
4. ✅ Installe les dépendances système (`curl`, `nftables`, `jq`, `sqlite3`, `vnstat`...)
5. ✅ Lance le panneau en mode interactif

Une fois installé, le menu principal s'affiche. Saisissez votre **clé
de licence** lorsque demandé (voir [Licence](#-licence)).

<details>
<summary><b>🔧 Désinstallation complète</b></summary>

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/adriop-45/Huop/main/install.sh) --auto-uninstall
```

Supprime **tous** les services, fichiers, configurations, utilisateurs
système et redémarre le VPS. ⚠️ **Action irréversible**.

</details>

---

## 🔧 Tunnels supportés

| # | Tunnel | Transport | Port(s) | Protocoles |
|---|---|---|---|---|
| 1 | **OpenSSH + Dropbear** | TCP direct | `22` / `109` | SSH v2 |
| 2 | **SSH-WS (slipstream)** | WebSocket | `80` | HTTP/WS tunneled |
| 3 | **SSL/TLS tunnel** | TLS direct | `444` | TLS 1.3 |
| 4 | **SlowDNS (dnstt)** | DNS over UDP | `53` | TXT records |
| 5 | **Xray** | Multi-transport | `443` / `8880` | VMess · VLESS · Trojan · Shadowsocks |
| 6 | **Xray transports** | xHTTP / gRPC / WS | `10012-10019` (local) | Splitting / mux |
| 7 | **V2Ray-DNS** | TCP over DNS tunnel | `5401` | VLESS + Trojan |
| 8 | **UDP-Custom** | UDP + catchall DNAT | `36712` | Password auth |
| 9 | **Hysteria v1** | QUIC | `20000 – 50000` | Obfuscation |
| 10 | **ZIVPN** | UDP obfuscated | `5667` / `6000 – 19999` | obfs=zivpn |
| 11 | **BadVPN UDPGW** | UDP | `7100` / `7200` / `7300` | UDP gateway |
| 12 | **HAProxy** | TCP/TLS fronting | `443` / `8880` / `9898` | LB + SNI routing |

---

## 🧩 Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         STRUCTURE INTERNE                            │
└─────────────────────────────────────────────────────────────────────┘

  /etc/kighmu/                 Configuration centrale
  ├── users/                    Meta-données par utilisateur (key=value)
  ├── banners/                  Bannières SSH pre-auth (HTML)
  ├── state/                    Flags persistants (optimized, autostart…)
  ├── ssh-shell.sh              Login shell wrapper
  └── bot/                      Telegram bot (token, resellers.db, audit)

  /etc/xray/                   Config Xray (10001-10019 inbounds)
  /etc/zivpn/                  Config + quota-state ZIVPN
  /etc/hysteria/               Config Hysteria
  /etc/dnsdist/                Config SlowDNS
  /etc/ssh/sshd_config.d/      Match User Banner (pre-auth HTML)

  /etc/systemd/system/
  ├── xray.service              Xray daemon
  ├── haproxy.service           HAProxy daemon
  ├── kighmu-ssh-tracker.service  Quota tracker SSH (Restart=always)
  ├── kighmu-ssh-quota-sync.timer Regen banners + sync (60s, Persistent)
  ├── kighmu-bot.service        Telegram bot
  └── kighmu-watchdog.{service,timer}  License watchdog (5s boot, 1h)

  /usr/local/bin/
  ├── kighmu                    Binaire principal
  ├── kighmu-bot                Alias bot
  ├── xray                      Binaire Xray
  ├── v2ray                     Binaire V2Ray
  ├── hysteria-linux-amd64      Binaire Hysteria
  ├── zivpn                     Binaire ZIVPN
  ├── sshws / ssl_tls           Tunnels SSH
  ├── udp-custom                Catchall UDP
  ├── dnstt-server              SlowDNS
  └── badvpn-udpgw              BadVPN
```

---

## 💎 Fonctionnalités

<details>
<summary><b>👥 Gestion des utilisateurs</b></summary>

- Création / suppression / renouvellement / verrouillage par protocole
- Quota data par utilisateur (GB, auto-bloquant au dépassement)
- Expiration automatique (cron `*/5` + `quota-enforce`)
- Bannières SSH dynamiques (pre-auth HTML + post-login texte)
- Limite IP par utilisateur
- Bulk operations : `renew 1,3-5 30` · `setquota 1-3 50`

</details>

<details>
<summary><b>🔄 Persistance après reboot</b></summary>

- **Systemd timer** `kighmu-ssh-quota-sync.timer` (60s, `Persistent=true`)
- **Cron fallback** `*/5 * * * * kighmu --ssh-quota-sync`
- **Daemon tracker** `kighmu-ssh-tracker.service` (`Restart=always`)
- Survit aux plantages, redémarrages, timeouts keep-alive
- Watchdogs 1-3 min sur tous les services critiques

</details>

<details>
<summary><b>🛡️ Firewall nftables</b></summary>

- Isolation par table `inet <protocole>` (nftables-tunnel@.service)
- Watchdog de dédup pour éviter conflits avec Docker et tables tierces
- Catchall DNAT pour UDP-Custom (exclusion slowdns port 53)
- Tables indépendantes pour SSH quota tracking (connexion-based)

</details>

<details>
<summary><b>🤖 Telegram Bot</b></summary>

- Dashboard : users, services, ressources, trafic
- CRUD users par protocole (SSH / Xray / V2Ray-DNS / ZIVPN / Hysteria)
- Multi-revendeurs : sous-bots isolés, quotas dédiés, tunnels autorisés
- Authentification par Telegram ID ou par access code
- Notification d'expiration automatique
- Compatible python-telegram-bot v13+

</details>

<details>
<summary><b>📊 Trafic et monitoring</b></summary>

- vnstat : trafic D / W / M par interface
- Comptage SSH par utilisateur via compteurs nftables
- Statistiques Xray via API dokodemo-door
- Quota enforcer (cron `*/5`) bloque automatiquement les dépassements
- Alerte Telegram quand quota > 90%

</details>

<details>
<summary><b>🔐 Sécurité et licence</b></summary>

- Licence liée au matériel (fingerprint HMAC-SHA256)
- Vérification toutes les heures (timer `kighmu-watchdog.timer`)
- Auto-désinstallation silencieuse si licence expirée / absente
- Token Telegram chiffré en SQLite (HMAC + machine-id)

</details>

---

## 🔐 Licence

Huop est un panel **commercial**. Une clé de licence est requise pour
l'utilisation professionnelle.

| Inclus | Gratuit (trial) | Commercial |
|---|---|---|
| Durée | 7 jours | 365 jours |
| Support | Communautaire | Telegram direct |
| Mises à jour | — | Incluses |
| Revendeurs | 1 | Illimités |
| Quota data | 50 GB | Illimité |
| Prix | 0 € | Sur demande |

**Pour obtenir une clé de licence** :

- 📩 **Telegram** : [@kighmu](https://t.me/kighmu)
- 📨 **Inbox** : [@kighmu](https://t.me/kighmu)

> 💼 Tarifs dégressifs pour les revendeurs et les parcs > 5 VPS.

---

## 🛟 Support

- 📩 **Telegram** : [@kighmu](https://t.me/kighmu) — réponse sous 24h
- 🐛 **Issues GitHub** : [github.com/adriop-45/Huop/issues](https://github.com/adriop-45/Huop/issues)
- 📖 **Documentation** : ce README

**Avant d'ouvrir un ticket**, préparez :

```bash
# Logs des services
journalctl -u kighmu-bot -u xray -u haproxy -n 100 --no-pager

# Statut du panel
kighmu --render main

# Version OS / arch
uname -a && cat /etc/os-release
```

---

## 📜 Crédits

Huop s'appuie sur les briques open-source suivantes :

- [Xray-core](https://github.com/XTLS/Xray-core) — proxy multi-protocole
- [V2Ray](https://github.com/v2fly/v2ray-core) — fallback VLESS/Trojan
- [Hysteria](https://github.com/apernet/hysteria) — QUIC proxy
- [ZIVPN](https://github.com/zahidbd2/udp-zivpn) — UDP obfuscated
- [dnstt](https://github.com/bugsfounder/dnstt) — DNS tunnel
- [BadVPN](https://github.com/ambrop72/badvpn) — UDP gateway
- [HAProxy](http://www.haproxy.org/) — load balancer
- [Nuitka](https://nuitka.net/) — Python-to-C compilation

---

<div align="center">

**© Huop. Tous droits réservés.**

Made with ❤️ by the Huop team

[Telegram](https://t.me/kighmu) · [GitHub](https://github.com/adriop-45/Huop)

</div>
