# Huop

> Panel professionnel de gestion de tunnels VPN — installation en une commande.

Huop est un panneau d'administration VPS qui déploie, supervise et gère
automatiquement un ensemble complet de tunnels VPN sur Debian / Ubuntu.
Pensé pour les revendeurs et les administrateurs qui veulent un outil
unique, stable, persistant après reboot, et pilotable en ligne de commande
comme via Telegram.

## Installation

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/adriop-45/Huop/main/install.sh)
```

Le script détecte l'architecture (x86_64 / ARM64), télécharge le binaire
correspondant depuis ce dépôt et l'installe dans `/usr/local/bin/kighmu`.
Connexion SSH ou console KVM requise.

> Debian 11+ / Ubuntu 20.04+ — root requis.

## Tunnels supportés

| Tunnel | Transport | Port(s) |
|---|---|---|
| OpenSSH + Dropbear | TCP direct | 22 / 109 |
| SSH-WS (slipstream) | WebSocket | 80 |
| SSL/TLS tunnel | TLS direct | 444 |
| SlowDNS (dnstt) | DNS over UDP | 53 |
| Xray — VMess / VLESS / Trojan | TCP / WS / gRPC / xHTTP / HTTPUpgrade | 443 / 8880 |
| V2Ray-DNS | TCP over DNS tunnel | 5401 |
| UDP-Custom (catchall DNAT) | UDP | 36712 |
| Hysteria v1 | QUIC | 20000 – 50000 |
| ZIVPN | UDP obfuscated | 5667 / 6000 – 19999 |
| BadVPN UDPGW | UDP | 7100 / 7200 / 7300 |
| HAProxy (load-balancing / TLS) | TCP | 443 / 8880 / 9898 |

## Fonctionnalités

- **Gestion utilisateurs** : création / suppression / renouvellement /
  verrouillage / quota data par compte et par protocole.
- **Persistance** : systemd timer + cron triple-redondant pour la
  régénération des bannières et la synchronisation des quotas — résiste
  aux reboots et plantages VPS.
- **Firewall nftables** : isolation par table inet + service
  `nftables-tunnel@.service`, watchdog de dédup pour éviter les conflits
  avec Docker et les tables tierces.
- **Telegram Bot** : panneau d'administration Telegram (dashboard,
  CRUD users, services, revendeurs).
- **Multi-revendeurs** : sous-bots Telegram isolés, quotas et expirations
  dédiés, tunnels autorisés par revendeur.
- **Trafic temps réel** : vnstat + comptabilité SSH par utilisateur
  via compteurs nftables.

## Licence

Huop est un panel **commercial**. Une clé de licence est requise pour
l'utilisation professionnelle (validation de licence liée au matériel,
mise à jour automatique, support).

Pour obtenir une clé de licence ou des informations tarifaires :

- **Telegram** : [@kighmu](https://t.me/kighmu)

## Support

- Telegram : [@kighmu](https://t.me/kighmu)
- Issues GitHub : ouvrir un ticket sur ce dépôt

---

© Huop. Tous droits réservés.
