#!/bin/bash
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GP=$(command -v gpclient) || exit 1

echo "$USER ALL=(ALL) NOPASSWD: SETENV: $GP" | sudo tee /etc/sudoers.d/gpclient-tray > /dev/null
sudo chmod 440 /etc/sudoers.d/gpclient-tray

chmod +x "$DIR/connect.py"
cat > "$HOME/.local/share/applications/global_protect_tray.desktop" << EOF
[Desktop Entry]
Name=GlobalProtect VPN
Exec="$DIR/connect.py"
Icon=$DIR/resources/icon.svg
Type=Application
Categories=Network;
EOF

update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true