#!/usr/bin/env python3
import sys, os, signal, shutil, argparse
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtCore import QProcess, QTimer
from PyQt5.QtGui import QIcon, QPixmap

def main():
    parser = argparse.ArgumentParser(description="GlobalProtect Tray")
    parser.add_argument("portal", help="VPN portal hostname")
    parser.add_argument("--browser", help="Use the specified browser to authenticate, e.g., 'default', 'firefox', 'chrome', 'chromium', 'remote', or the path to the browser executable. Use 'remote' for headless servers", default=None)
    parser.add_argument("--fix-openssl", action="store_true", help="Get around the OpenSSL 'unsafe legacy renegotiation' error")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    path = os.path.dirname(os.path.abspath(__file__))
    gp = shutil.which("gpclient")
    gp_process = QProcess()

    def disconnect():
        gp_process.blockSignals(True)
        QProcess.startDetached("sudo", ["-E", gp, "disconnect"])
        if not gp_process.waitForFinished(2500):
            gp_process.kill()
        app.quit()

    gp_process.setProcessChannelMode(QProcess.MergedChannels)
    gp_process.finished.connect(lambda exit_code: (
        tray.showMessage("Error", gp_process.readAll().data().decode()[:100], 3) if exit_code else None,
        QTimer.singleShot(3000, app.quit) if exit_code else app.quit()
    ))

    cmd_args = ["-E", gp]
    if args.fix_openssl:
        cmd_args.append("--fix-openssl")
    cmd_args.append("connect")
    if args.browser:
        cmd_args.extend(["--browser", args.browser])
    cmd_args.append(args.portal)

    gp_process.start("sudo", cmd_args)

    tray = QSystemTrayIcon(QIcon(QPixmap(os.path.join(path, "resources", "icon.svg"))), app)
    tray.setToolTip(f"GlobalProtect: {args.portal}")
    
    menu = QMenu()
    menu.addAction("Disconnect", disconnect)
    tray.setContextMenu(menu)
    tray.show()

    signal.signal(signal.SIGINT, lambda *a: disconnect())
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()