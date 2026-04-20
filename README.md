# GlobalProtect Tray

A minimal, open-source system tray wrapper for the [GlobalProtect-openconnect](https://github.com/yuezk/GlobalProtect-openconnect) CLI client (`gpclient`).

The upstream project offers a GUI, but it is proprietary and paid. This project provides a free, lightweight alternative that wraps the CLI commands into a convenient and minimal system tray icon for easy connection management.

## Features

- **One-click Disconnect:** Easily disconnect via the tray menu.
- **Auto-Connect:** Launches your saved configuration immediately.
- **Seamless Permissions:** Automatically configures `sudoers` so you can run the root-required `gpclient` without constant password prompts.

## Requirements

- Linux
- Python 3
- `PyQt5` (Install via `pip install PyQt5` or `sudo dnf install python3-qt5` or `sudo apt install python3-pyqt5`)
- `gpclient` ([GlobalProtect-openconnect](https://github.com/yuezk/GlobalProtect-openconnect)) installed.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mwdle/GlobalProtectTray.git
   cd GlobalProtect-Tray
   ```

2. Run the installer:

   ```bash
   ./install.sh
   ```

The script will prompt you for:

- **VPN Portal Hostname** (e.g., `vpn.example.com`)
- **SAML Browser** (e.g., `chrome`, `firefox`, `default` for default system browser, or leave blank to use embedded browser)
- **OpenSSL Legacy Fix** (enable if encountering issues with legacy servers)

> **Note on Permissions:** The installer runs `sudo` to add a file to `/etc/sudoers.d/`.
> This allows your user to execute `gpclient` as root without entering a password,
> ensuring a seamless "click-to-connect" experience.

## Usage

Search for **GlobalProtect VPN** in your application launcher. The app will start the VPN connection (as configured in the installation) immediately. The tray icon serves as an indicator that you are connected, and right clicking it will reveal a disconnect button.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
