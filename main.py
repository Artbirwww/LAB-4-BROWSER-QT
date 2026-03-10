import sys
from PyQt5.QtWidgets import QApplication
from browser_window import AdvancedBrowser

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = AdvancedBrowser()
    browser.show()
    sys.exit(app.exec_())