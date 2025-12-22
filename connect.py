#!/usr/bin/env python3
import sys, os, signal, shutil
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtCore import QProcess, QTimer
from PyQt5.QtGui import QIcon, QPixmap

def main():
    app = QApplication(sys.argv)
    path = os.path.dirname(os.path.abspath(__file__))
    gp = shutil.which("gpclient")
    gp_process = QProcess()

    def disconnect():
        gp_process.blockSignals(True)
        gp_process.kill()
        QProcess.startDetached("sudo", ["-E", gp, "disconnect"])
        app.quit()

    gp_process.setProcessChannelMode(QProcess.MergedChannels)
    gp_process.finished.connect(lambda exit_code: (
        tray.showMessage("Error", gp_process.readAll().data().decode()[:100], 3) if exit_code else None,
        QTimer.singleShot(3000, app.quit) if exit_code else app.quit()
    ))
    gp_process.start("sudo", ["-E", gp, "--fix-openssl", "connect", "--browser", "default", "vpn.yourportal.edu"])

    tray = QSystemTrayIcon(QIcon(QPixmap(os.path.join(path, "resources", "icon.svg"))), app)
    tray.setToolTip("GlobalProtect")
    
    menu = QMenu()
    menu.addAction("Disconnect", disconnect)
    tray.setContextMenu(menu)
    tray.show()

    signal.signal(signal.SIGINT, lambda *a: disconnect())
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()