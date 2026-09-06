#!/usr/bin/env python3
"""
kighmu-vpn builder - Génère l'image docker.io/adriop45/kighmu-vpn
UUID: aaaa0000-1111-4222-8333-444455556666
WSPATH: /@kighmu
Usage:
  python3 build_kighmu.py              # génère Dockerfile + entrypoint.sh
  python3 build_kighmu.py --build      # génère + docker build
  python3 build_kighmu.py --build --push # génère + build + push
"""
import os, subprocess, argparse, textwrap, pathlib

UUID = "aaaa0000-1111-4222-8333-444455556666"
WSPATH = "/@kighmu"
IMAGE = "docker.io/adriop45/kighmu-vpn:latest"
PORT = 8080

DOCKERFILE = f"""FROM alpine:3.22
LABEL maintainer="adriop45 <kighmu>"
WORKDIR /root
ARG TARGETARCH
RUN apk add --no-cache ca-certificates tzdata bash wget unzip \\
 && mkdir -p /etc/xray /var/log/xray /usr/local/bin /usr/share/xray \\
 && XARCH=$(echo ${{TARGETARCH:-amd64}} | sed 's/amd64/64/;s/arm64/arm64-v8a/;s/arm/32/') \\
 && wget -qO /tmp/Xray.zip https://github.com/XTLS/Xray-core/releases/download/v25.12.8/Xray-linux-${{XARCH}}.zip \\
 && unzip -q /tmp/Xray.zip -d /tmp/xray \\
 && mv /tmp/xray/xray /usr/local/bin/xray \\
 && chmod +x /usr/local/bin/xray \\
 && wget -qO /usr/share/xray/geosite.dat https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/geosite.dat \\
 && wget -qO /usr/share/xray/geoip.dat https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/geoip.dat \\
 && rm -rf /tmp/Xray.zip /tmp/xray
ENV TZ=Asia/Shanghai
ENV PORT={PORT}
ENV PASSWORD={UUID}
ENV WSPATH={WSPATH}
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE {PORT}
VOLUME ["/etc/xray","/var/log/xray"]
CMD ["/entrypoint.sh"]
"""

ENTRYPOINT = f"""#!/bin/sh
set -e
PORT="${{PORT:-{PORT}}}"
PASSWORD="${{PASSWORD:-{UUID}}}"
WSPATH="${{WSPATH:-{WSPATH}}}"
cat > /etc/xray/config.json <<EOF
{{
  "log": {{"loglevel": "warning"}},
"inbounds": [{{
    "port": {PORT},
    "protocol": "vless",
    "settings": {{"clients": [{{"id": "{PASSWORD}","level": 0}}],"decryption": "none"}},
    "streamSettings": {{"network": "ws","wsSettings": {{"path": "{WSPATH}"}}}}
  }}],
  "outbounds": [{{"protocol": "freedom"}}]
}}
EOF
exec xray run -config /etc/xray/config.json
"""

def write_files():
    pathlib.Path("Dockerfile").write_text(DOCKERFILE, encoding="utf-8")
    pathlib.Path("entrypoint.sh").write_text(ENTRYPOINT, encoding="utf-8")
    os.chmod("entrypoint.sh", 0o755)
    pathlib.Path(".dockerignore").write_text(".git\n.github\n", encoding="utf-8")
    print("✓ Dockerfile + entrypoint.sh + .dockerignore générés")
    print(f"  UUID={UUID}  WSPATH={WSPATH}  PORT={PORT}")

def build_image():
    subprocess.run(["docker", "build", "-t", IMAGE, "."], check=True)
    print(f"✓ Build OK -> {IMAGE}")

def push_image():
    subprocess.run(["docker", "push", IMAGE], check=True)
    print(f"✓ Push OK -> {IMAGE}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--build", action="store_true", help="docker build après génération")
    p.add_argument("--push", action="store_true", help="docker push (nécessite docker login)")
    args = p.parse_args()
    write_files()
    if args.build: build_image()
    if args.push: push_image()
    if not args.build:
        print("\nEnsuite en local:")
        print("  docker build -t docker.io/adriop45/kighmu-vpn:latest .")
        print("  docker push docker.io/adriop45/kighmu-vpn:latest")
