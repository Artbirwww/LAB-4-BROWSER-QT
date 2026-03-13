import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon
from PyQt5.QtGui import QIcon
from browser_window import AdvancedBrowser

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setWindowIcon(QIcon("nav/icon.png"))
    
    browser = AdvancedBrowser(incognito=False)
    browser.show()
    
    sys.exit(app.exec_())