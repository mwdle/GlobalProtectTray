#!/bin/bash
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GP=$(command -v gpclient) || exit 1

echo "Configuring GlobalProtect Tray..."

read -p "Enter VPN Portal Hostname (e.g., vpn.example.com): " PORTAL
if [ -z "$PORTAL" ]; then echo "Error: Portal hostname is required."; exit 1; fi
read -p "Use the specified browser to authenticate (leave blank to use embedded browser), e.g., 'default', 'firefox', 'chrome', 'chromium', 'remote', or the path to the browser executable. Use 'remote' for headless servers: " BROWSER
read -p "Get around the OpenSSL 'unsafe legacy renegotiation' error using --fix-openssl? (y/N): " FIX_SSL

ARGS="$PORTAL"

# If user typed anything for browser (default, chrome, firefox), add the flag
if [ ! -z "$BROWSER" ]; then 
    ARGS="--browser $BROWSER $ARGS"
fi

# Add fix-openssl flag if user said yes
if [[ "$FIX_SSL" =~ ^[Yy]$ ]]; then 
    ARGS="--fix-openssl $ARGS"
fi

echo "$USER ALL=(ALL) NOPASSWD: SETENV: $GP" | sudo tee /etc/sudoers.d/gpclient-tray > /dev/null
sudo chmod 440 /etc/sudoers.d/gpclient-tray

chmod +x "$DIR/connect.py"

cat > "$HOME/.local/share/applications/global_protect_tray.desktop" << EOF
[Desktop Entry]
Name=GlobalProtect VPN
Comment=GlobalProtect-openconnect Tray
Exec="$DIR/connect.py" $ARGS
Icon=$DIR/resources/icon.svg
Type=Application
Categories=Network;
EOF

update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
echo "Successfully created desktop shortcut with provided args: $ARGS"