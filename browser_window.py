from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt, QPoint, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

from database import Database
from theme_switcher import ThemeManager
from title_bar import TitleBar
from navbar import NavigationBar
from favourites import BookmarksBar
from tab_widget import TabWidget
from history_dialog import HistoryDialog
from favourites_dialog import BookmarksDialog

class AdvancedBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("POVTIAS CO. INC. BROWSER")
        self.setGeometry(100, 100, 1200, 800)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.database = Database()
        self.theme_switcher = ThemeManager()
        self.current_theme = self.database.get_setting("theme", "light")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.title_bar = TitleBar(self)
        self.nav_bar = NavigationBar(self)
        self.favourites = BookmarksBar(self)
        self.tabs = TabWidget(self)
        # self.tabs = CustomTabWidget(self)
        
        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(self.nav_bar)
        main_layout.addWidget(self.favourites)
        main_layout.addWidget(self.tabs)
        
        
        self.load_bookmarks()

        self.apply_theme()

        self.add_new_tab()
        
        self.dragging = False
        self.drag_position = QPoint()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if event.pos().y() <= self.title_bar.height():
                self.dragging = True
                self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
                event.accept()
                
    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
            
    def mouseReleaseEvent(self, event):
        self.dragging = False
        
    def apply_theme(self):
        style = self.theme_switcher.get_theme_style(self.current_theme)
        self.setStyleSheet(style)

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.database.save_setting("theme", theme_name)
        self.apply_theme()
        
    def load_bookmarks(self):
        bookmarks = self.database.get_bookmarks()
        self.favourites.load_bookmarks(bookmarks)
        
    def add_new_tab(self, qurl=None):
        self.tabs.add_new_tab(qurl)
        
    def current_browser(self):
        return self.tabs.current_browser()
        
    def update_url_bar(self, qurl, browser=None):
        if browser == self.current_browser():
            self.nav_bar.update_url(qurl)
            
    def navigate_to_url(self):
        url = self.nav_bar.url_bar.text()
        self.open_url(url)
        
    def open_url(self, url):
        if url:
            if not url.startswith("http") and not url.startswith("https"):
                if "." in url and not " " in url:
                    url = "http://" + url
                else:
                    url = "https://ya.ru/search/?text=" + url.replace(" ", "+")
            self.current_browser().setUrl(QUrl(url))

    def go_home(self):
        self.current_browser().setUrl(QUrl("https://ya.ru"))
        
    def add_bookmark(self):
        browser = self.current_browser()
        if browser:
            url = browser.url().toString()
            title = browser.page().title() or "Без названия"
            
            if self.database.bookmark_exists(url):
                QMessageBox.information(
                    self, "Информация",
                    "Эта страница уже добавлена в закладки!"
                )
                return
            
            new_title, ok = QInputDialog.getText(
                self, "Добавить закладку",
                "Введите название для закладки:",
                text=title
            )
            
            if ok and new_title:
                self.database.add_bookmark(new_title, url)
                self.load_bookmarks()
                QMessageBox.information(self, "Успех", "Закладка добавлена!")
                
    def show_history(self):
        dialog = HistoryDialog(self)
        dialog.exec_()
        
    def show_all_bookmarks(self):
        dialog = BookmarksDialog(self)
        dialog.exec_()
        
    def clear_history(self):
        reply = QMessageBox.question(
            self, "Очистка истории",
            "Вы уверены, что хотите очистить всю историю?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.database.clear_history()
            QMessageBox.information(self, "Успех", "История очищена!")
            
    def closeEvent(self, event):
        self.database.close()
        event.accept()