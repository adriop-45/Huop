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

[Telegram](https://t.me/kighmu) · [Achat licence](https://t.me/kighmu)

</div>

---

## 📑 Sommaire

- [📦 Prérequis](#-prérequis)
- [🚀 Installation](#-installation)
- [🔧 Tunnels supportés](#-tunnels-supportés)
- [💎 Fonctionnalités](#-fonctionnalités)
- [🔐 Licence](#-licence)
- [🛟 Support](#-support)

---

## 📦 Prérequis

Mettre à jour le système avant l'installation :

```bash
apt update && apt upgrade -y
```

> 💡 Si le noyau a été mis à jour, **redémarrer** :
> ```bash
> reboot
> ```
> Attendre ~30 secondes avant de vous reconnecter.

**Exigences** :

| Ressource | Minimum |
|---|---|
| **OS** | Debian 11+ / Ubuntu 20.04+ |
| **RAM** | 512 MB |
| **CPU** | 1 vCPU |
| **Disque** | 2 GB libre |
| **Réseau** | IPv4 publique |
| **Accès** | `root` |

---

## 🚀 Installation

**One-liner** :

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/adriop-45/Huop/main/install.sh)
```

Le script détecte l'architecture, télécharge le binaire et l'installe
automatiquement. La clé de licence est demandée au premier lancement.

---

## 🔧 Tunnels supportés

| Tunnel | Transport | Port(s) |
|---|---|---|
| OpenSSH + Dropbear | TCP | 22 / 109 |
| SSH-WS | WebSocket | 80 |
| SSL/TLS | TLS | 444 |
| SlowDNS | DNS | 53 |
| Xray (VMess / VLESS / Trojan) | TCP / WS / gRPC / xHTTP | 443 / 8880 |
| V2Ray-DNS | TCP / DNS | 5401 |
| UDP-Custom | UDP | 36712 |
| Hysteria | QUIC | 20000 – 50000 |
| ZIVPN | UDP | 5667 / 6000 – 19999 |
| BadVPN | UDP | 7100 / 7200 / 7300 |
| HAProxy | TCP / TLS | 443 / 8880 |

---

## 💎 Fonctionnalités

- 👥 **Gestion utilisateurs** : création, suppression, renouvellement,
  verrouillage, quota data par utilisateur
- 🔄 **Persistance** : triple-redondant (systemd timer + cron + daemon)
- 🛡️ **Firewall** : nftables isolé, watchdog anti-conflit
- 🤖 **Telegram Bot** : dashboard, CRUD users, multi-revendeurs
- 📊 **Monitoring** : vnstat + quota SSH temps réel

---

## 🔐 Licence

Huop est un panel **commercial**. Une clé de licence est requise.

- **Trial** : 7 jours, support communautaire
- **Commercial** : 365 jours, support Telegram direct, mises à jour

**Achat / infos** : [@kighmu sur Telegram](https://t.me/kighmu)

---

## 🛟 Support

- 📩 Telegram : [@kighmu](https://t.me/kighmu)
- 🐛 Issues : ce dépôt GitHub

---

<div align="center">

**© Huop. Tous droits réservés.**

[Telegram](https://t.me/kighmu) · [GitHub](https://github.com/adriop-45/Huop)

</div>
