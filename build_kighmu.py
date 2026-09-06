#!/usr/bin/env python3
"""
kighmu-vpn builder - Génère l'image docker.io/adriop45/kighmu-vpn
UUID: aaaa0000-1111-4222-8333-444455556666
WSPATH: /@kighmu
Usage:
  python3 build_kighmu.py              # génère Dockerfile + entrypoint.sh + nginx.conf
  python3 build_kighmu.py --build      # génère + docker build
  python3 build_kighmu.py --build --push # génère + build + push
"""
import os, subprocess, argparse, textwrap, pathlib

UUID = "aaaa0000-1111-4222-8333-444455556666"
WSPATH = "/@kighmu"
IMAGE = "docker.io/adriop45/kighmu-vpn:latest"
PORT = 8080
XRAY_INTERNAL_PORT = 8081

DOCKERFILE = f"""FROM alpine:3.22
LABEL maintainer="adriop45 <kighmu>"
WORKDIR /root
ARG TARGETARCH
RUN apk add --no-cache ca-certificates tzdata bash wget unzip nginx \\
 && mkdir -p /etc/xray /var/log/xray /usr/local/bin /usr/share/xray /run/nginx \\
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
COPY nginx.conf /etc/nginx/nginx.conf
RUN chmod +x /entrypoint.sh
EXPOSE {PORT}
VOLUME ["/etc/xray","/var/log/xray"]
CMD ["/entrypoint.sh"]
"""

NGINX_CONF = f"""user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /run/nginx/nginx.pid;

events {{
    worker_connections 1024;
}}

http {{
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    access_log /var/log/nginx/access.log main;
    sendfile on;
    keepalive_timeout 65;

    upstream xray_backend {{
        server 127.0.0.1:{XRAY_INTERNAL_PORT};
    }}

    server {{
        listen ${{PORT}};
        listen [::]:${{PORT}};
        server_name _;

        # Health check endpoint for Cloud Run
        location = / {{
            return 200 "OK";
            add_header Content-Type text/plain;
        }}

        # WebSocket proxy to Xray
        location {WSPATH} {{
            proxy_pass http://xray_backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 86400;
            proxy_send_timeout 86400;
        }}

        # Deny all other paths
        location / {{
            return 404;
        }}
    }}
}}
"""

ENTRYPOINT = f"""#!/bin/sh
set -e
PORT="${{PORT:-{PORT}}}"
PASSWORD="${{PASSWORD:-{UUID}}}"
WSPATH="${{WSPATH:-{WSPATH}}}"

# Generate Xray config (listens on localhost only)
cat > /etc/xray/config.json <<EOF
{{
  "log": {{"loglevel": "warning"}},
  "inbounds": [{{
    "port": {XRAY_INTERNAL_PORT},
    "listen": "127.0.0.1",
    "protocol": "vless",
    "settings": {{"clients": [{{"id": "{UUID}","level": 0}}],"decryption": "none"}},
    "streamSettings": {{"network": "ws","wsSettings": {{"path": "{WSPATH}"}}}}
  }}],
  "outbounds": [{{"protocol": "freedom"}}]
}}
EOF

# Generate nginx config with actual PORT
sed -i "s/\\${{PORT}}/$PORT/g" /etc/nginx/nginx.conf

# Start nginx in background
nginx -g 'daemon off;' &

# Start Xray (foreground)
exec xray run -config /etc/xray/config.json
"""

def write_files():
    pathlib.Path("Dockerfile").write_text(DOCKERFILE, encoding="utf-8")
    pathlib.Path("entrypoint.sh").write_text(ENTRYPOINT, encoding="utf-8")
    pathlib.Path("nginx.conf").write_text(NGINX_CONF, encoding="utf-8")
    os.chmod("entrypoint.sh", 0o755)
    pathlib.Path(".dockerignore").write_text(".git\n.github\n", encoding="utf-8")
    print("✓ Dockerfile + entrypoint.sh + nginx.conf + .dockerignore générés")
    print(f"  UUID={UUID}  WSPATH={WSPATH}  PORT={PORT}  XRAY_INTERNAL_PORT={XRAY_INTERNAL_PORT}")

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