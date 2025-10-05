#!/usr/bin/env bash
set -euo pipefail

CLOUDYPAD_REF="${CLOUDYPAD_REF:-v0.39.0}"
SUNSHINE_USER="${SUNSHINE_USER:-cloudy}"
SUNSHINE_PASS="${SUNSHINE_PASS:-CloudyPad123!}"
DOCKER_USER="${DOCKER_USER:-$USER}"
WG_IFACE="${WG_IFACE:-wg0}"
WG_PORT="${WG_PORT:-51820}"
WG_SERVER_IP="${WG_SERVER_IP:-10.10.0.1}"
WG_PEER_IP="${WG_PEER_IP:-10.10.0.2}"
WG_PEER_NAME="${WG_PEER_NAME:-moonlight-peer}"
COMPOSE_VERSION="${COMPOSE_VERSION:-v2.39.4}"
CLOUDYPAD_HOME="$HOME/cloudypad"
CLOUDYPAD_BIN="$HOME/.cloudypad/bin/cloudypad"
WIREGUARD_DIR="$HOME/wireguard"
WG_SYSTEM_CONF="/etc/wireguard/${WG_IFACE}.conf"
WG_SERVICE="wg-quick@${WG_IFACE}"

sudo apt-get update

sudo apt-get install -y git curl jq ansible wireguard qrencode xdotool python3

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required but not found. Install Docker before running this script." >&2
  exit 1
fi

if ! groups "$DOCKER_USER" | grep -q '\bdocker\b'; then
  sudo usermod -aG docker "$DOCKER_USER"
  echo "User '$DOCKER_USER' added to docker group. Log out/in or run 'newgrp docker'."
fi

sudo mkdir -p /usr/local/lib/docker/cli-plugins

if [ ! -x /usr/local/lib/docker/cli-plugins/docker-compose ]; then
  sudo curl -L "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-linux-x86_64" -o /usr/local/lib/docker/cli-plugins/docker-compose
  sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
fi

docker --version || true

docker compose version || true

if [ -d "$CLOUDYPAD_HOME" ]; then
  git -C "$CLOUDYPAD_HOME" fetch --all
  git -C "$CLOUDYPAD_HOME" pull --ff-only
else
  git clone https://github.com/PierreBeucher/cloudypad.git "$CLOUDYPAD_HOME"
fi

ansible-galaxy install -r "$CLOUDYPAD_HOME/ansible/requirements.yml"

if [ ! -x "$CLOUDYPAD_BIN" ]; then
  sg docker -c "cd '$CLOUDYPAD_HOME' && CLOUDYPAD_INSTALL_SKIP_DOCKER_CHECK=true CLOUDYPAD_SCRIPT_REF=${CLOUDYPAD_REF} bash install.sh"
else
  echo "Cloudy Pad CLI already present at $CLOUDYPAD_BIN; skipping installer."
fi

mkdir -p "$CLOUDYPAD_HOME/ansible/vars"

SUNSHINE_PASS_B64=$(printf '%s' "$SUNSHINE_PASS" | base64)

cat <<JSON > "$CLOUDYPAD_HOME/ansible/vars/sunshine-local.json"
{
  "ansible_connection": "local",
  "cloudypad_provider": "ssh",
  "sunshine_nvidia_enable": false,
  "sunshine_image_tag": "${CLOUDYPAD_REF#v}",
  "sunshine_web_username": "${SUNSHINE_USER}",
  "sunshine_web_password_base64": "${SUNSHINE_PASS_B64}",
  "sunshine_max_bitrate_kbps": "0"
}
JSON

cat <<JSON > "$CLOUDYPAD_HOME/ansible/vars/sunshine-override.json"
{
  "sunshine_additional_config": "capture = x11"
}
JSON

sg docker -c "cd '$CLOUDYPAD_HOME' && ansible-playbook ansible/sunshine.yml -i localhost, -e @ansible/vars/sunshine-local.json -e @ansible/vars/sunshine-override.json"

mkdir -p "$WIREGUARD_DIR"

SERVER_CONF_LOCAL="$WIREGUARD_DIR/${WG_IFACE}.conf"
PEER_CONF="$WIREGUARD_DIR/${WG_PEER_NAME}.conf"
KEY_CACHE="$WIREGUARD_DIR/.keys"

if [ -f "$KEY_CACHE" ]; then
  # shellcheck disable=SC1090
  source "$KEY_CACHE"
else
  SERVER_PRIV=$(wg genkey)
  SERVER_PUB=$(printf '%s' "$SERVER_PRIV" | wg pubkey)
  PEER_PRIV=$(wg genkey)
  PEER_PUB=$(printf '%s' "$PEER_PRIV" | wg pubkey)
  PSK=$(wg genpsk)
  cat <<KEYS > "$KEY_CACHE"
SERVER_PRIV='$SERVER_PRIV'
SERVER_PUB='$SERVER_PUB'
PEER_PRIV='$PEER_PRIV'
PEER_PUB='$PEER_PUB'
PSK='$PSK'
KEYS
  chmod 600 "$KEY_CACHE"
fi

cat <<CFG > "$SERVER_CONF_LOCAL"
# WireGuard server configuration
[Interface]
Address = ${WG_SERVER_IP}/24
ListenPort = ${WG_PORT}
PrivateKey = ${SERVER_PRIV}
SaveConfig = false

[Peer]
# ${WG_PEER_NAME}
PublicKey = ${PEER_PUB}
PresharedKey = ${PSK}
AllowedIPs = ${WG_PEER_IP}/32
CFG

cat <<CFG > "$PEER_CONF"
# WireGuard peer configuration
[Interface]
Address = ${WG_PEER_IP}/32
PrivateKey = ${PEER_PRIV}
DNS = 1.1.1.1

[Peer]
PublicKey = ${SERVER_PUB}
PresharedKey = ${PSK}
Endpoint = <server-public-ip>:${WG_PORT}
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
CFG

chmod 600 "$SERVER_CONF_LOCAL" "$PEER_CONF"

sudo mkdir -p /etc/wireguard

sudo cp "$SERVER_CONF_LOCAL" "$WG_SYSTEM_CONF"

sudo chmod 600 "$WG_SYSTEM_CONF"

sudo systemctl enable --now "$WG_SERVICE"

sudo systemctl restart "$WG_SERVICE"

wg show "$WG_IFACE" || true

echo "\n=== WireGuard Peer Config (${PEER_CONF}) ==="
cat "$PEER_CONF"

echo "\n=== WireGuard Peer QR Code ==="
qrencode -t ansiutf8 < "$PEER_CONF"

echo "\nSunshine deployment complete."
echo "Sunshine credentials => user: ${SUNSHINE_USER} password: ${SUNSHINE_PASS}"
echo "WireGuard interface ${WG_IFACE} is up using configuration at ${WG_SYSTEM_CONF}"
echo "Peer configuration stored in $PEER_CONF"
echo "Peer private key: ${PEER_PRIV}"
