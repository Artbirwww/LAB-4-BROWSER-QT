from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox, QInputDialog, QShortcut
from PyQt5.QtCore import Qt, QPoint, QUrl
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile

from database import Database
from theme_switcher import ThemeManager
from title_bar import TitleBar
from navbar import NavigationBar
from favourites import BookmarksBar
from tab_widget import TabWidget
from history_dialog import HistoryDialog
from favourites_dialog import BookmarksDialog

class AdvancedBrowser(QMainWindow):
    def __init__(self, incognito=False):
        super().__init__()
        self.incognito = incognito
        
        if incognito:
            self.setWindowTitle("POVTIAS CO. INC. BROWSER - ИНКОГНИТО")
        else:
            self.setWindowTitle("POVTIAS CO. INC. BROWSER")
            
        # Устанавливаем геометрию, но потом сразу разворачиваем на весь экран
        self.setGeometry(100, 100, 1200, 800)
        
        # Убираем стандартный заголовок окна для кастомного
        self.setWindowFlags(Qt.FramelessWindowHint)

        # База данных только для обычного режима
        if not incognito:
            self.database = Database()
        else:
            self.database = None
            
        self.theme_switcher = ThemeManager()
        
        # Для инкогнито всегда используем темную тему
        if incognito:
            self.current_theme = "dark"
        else:
            self.current_theme = self.database.get_setting("theme", "light") if self.database else "light"

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.title_bar = TitleBar(self)
        self.nav_bar = NavigationBar(self)
        self.favourites = BookmarksBar(self)
        self.tabs = TabWidget(self, incognito)

        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(self.nav_bar)
        main_layout.addWidget(self.favourites)
        main_layout.addWidget(self.tabs)

        if not incognito:
            self.load_bookmarks()
            
        self.apply_theme()
        self.add_new_tab()

        self.dragging = False
        self.drag_position = QPoint()
        
        # Устанавливаем шорткаты
        self.setup_shortcuts()
        
        # Разворачиваем окно на весь экран после инициализации
        # Используем QTimer чтобы окно успело полностью инициализироваться
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(100, self.showMaximized)

    def setup_shortcuts(self):
        """Настройка горячих клавиш"""
        
        # Навигация
        self.shortcut_back = QShortcut(QKeySequence("Alt+Left"), self)
        self.shortcut_back.activated.connect(self.go_back)
        
        self.shortcut_forward = QShortcut(QKeySequence("Alt+Right"), self)
        self.shortcut_forward.activated.connect(self.go_forward)
        
        self.shortcut_reload = QShortcut(QKeySequence("Ctrl+R"), self)
        self.shortcut_reload.activated.connect(self.reload_page)
        
        self.shortcut_home = QShortcut(QKeySequence("Alt+Home"), self)
        self.shortcut_home.activated.connect(self.go_home)
        
        # Вкладки
        self.shortcut_new_tab = QShortcut(QKeySequence("Ctrl+T"), self)
        self.shortcut_new_tab.activated.connect(lambda: self.add_new_tab())
        
        self.shortcut_close_tab = QShortcut(QKeySequence("Ctrl+W"), self)
        self.shortcut_close_tab.activated.connect(self.close_current_tab)
        
        self.shortcut_next_tab = QShortcut(QKeySequence("Ctrl+Tab"), self)
        self.shortcut_next_tab.activated.connect(self.next_tab)
        
        self.shortcut_prev_tab = QShortcut(QKeySequence("Ctrl+Shift+Tab"), self)
        self.shortcut_prev_tab.activated.connect(self.prev_tab)
        
        # Цифровые шорткаты для переключения на конкретные вкладки (Ctrl+1..8)
        for i in range(1, 9):
            shortcut = QShortcut(QKeySequence(f"Ctrl+{i}"), self)
            shortcut.activated.connect(lambda idx=i-1: self.switch_to_tab(idx))
        
        # Окна
        self.shortcut_new_window = QShortcut(QKeySequence("Ctrl+N"), self)
        self.shortcut_new_window.activated.connect(self.open_new_window)
        
        self.shortcut_incognito = QShortcut(QKeySequence("Ctrl+Shift+N"), self)
        self.shortcut_incognito.activated.connect(self.open_incognito_window)
        
        self.shortcut_fullscreen = QShortcut(QKeySequence("F11"), self)
        self.shortcut_fullscreen.activated.connect(self.toggle_fullscreen)
        
        # Поиск и адресная строка
        self.shortcut_focus_url = QShortcut(QKeySequence("Ctrl+L"), self)
        self.shortcut_focus_url.activated.connect(self.focus_url_bar)
        
        self.shortcut_focus_url_alt = QShortcut(QKeySequence("Alt+D"), self)
        self.shortcut_focus_url_alt.activated.connect(self.focus_url_bar)
        
        self.shortcut_search = QShortcut(QKeySequence("Ctrl+K"), self)
        self.shortcut_search.activated.connect(self.focus_search)
        
        # Закладки и история
        self.shortcut_bookmark = QShortcut(QKeySequence("Ctrl+D"), self)
        self.shortcut_bookmark.activated.connect(self.add_bookmark)
        
        self.shortcut_bookmarks = QShortcut(QKeySequence("Ctrl+Shift+B"), self)
        self.shortcut_bookmarks.activated.connect(self.show_all_bookmarks)
        
        self.shortcut_history = QShortcut(QKeySequence("Ctrl+H"), self)
        self.shortcut_history.activated.connect(self.show_history)
        
        self.shortcut_clear_history = QShortcut(QKeySequence("Ctrl+Shift+Del"), self)
        self.shortcut_clear_history.activated.connect(self.clear_history)
        
        # Масштабирование
        self.shortcut_zoom_in = QShortcut(QKeySequence("Ctrl+="), self)
        self.shortcut_zoom_in.activated.connect(self.zoom_in)
        
        self.shortcut_zoom_out = QShortcut(QKeySequence("Ctrl+-"), self)
        self.shortcut_zoom_out.activated.connect(self.zoom_out)
        
        self.shortcut_zoom_reset = QShortcut(QKeySequence("Ctrl+0"), self)
        self.shortcut_zoom_reset.activated.connect(self.zoom_reset)
        
        # Дополнительные функции
        self.shortcut_print = QShortcut(QKeySequence("Ctrl+P"), self)
        self.shortcut_print.activated.connect(self.print_page)
        
        self.shortcut_save = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcut_save.activated.connect(self.save_page)
        
        self.shortcut_find = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut_find.activated.connect(self.find_in_page)
        
        self.shortcut_stop = QShortcut(QKeySequence("Esc"), self)
        self.shortcut_stop.activated.connect(self.stop_loading)

    def go_back(self):
        """Перейти назад"""
        browser = self.current_browser()
        if browser and browser.history().canGoBack():
            browser.back()

    def go_forward(self):
        """Перейти вперед"""
        browser = self.current_browser()
        if browser and browser.history().canGoForward():
            browser.forward()

    def reload_page(self):
        """Обновить страницу"""
        browser = self.current_browser()
        if browser:
            browser.reload()

    def close_current_tab(self):
        """Закрыть текущую вкладку"""
        current_index = self.tabs.tab_bar.currentIndex()
        if current_index >= 0:
            self.tabs.close_tab(current_index)

    def next_tab(self):
        """Переключиться на следующую вкладку"""
        count = self.tabs.count()
        if count > 1:
            current = self.tabs.tab_bar.currentIndex()
            next_index = (current + 1) % count
            self.tabs.tab_bar.setCurrentIndex(next_index)

    def prev_tab(self):
        """Переключиться на предыдущую вкладку"""
        count = self.tabs.count()
        if count > 1:
            current = self.tabs.tab_bar.currentIndex()
            prev_index = (current - 1) % count
            self.tabs.tab_bar.setCurrentIndex(prev_index)

    def switch_to_tab(self, index):
        """Переключиться на вкладку по индексу"""
        if 0 <= index < self.tabs.count():
            self.tabs.tab_bar.setCurrentIndex(index)

    def open_new_window(self):
        """Открыть новое окно"""
        from browser_window import AdvancedBrowser
        self.new_window = AdvancedBrowser(incognito=False)
        self.new_window.show()

    def open_incognito_window(self):
        """Открыть окно инкогнито"""
        from browser_window import AdvancedBrowser
        self.incognito_window = AdvancedBrowser(incognito=True)
        self.incognito_window.show()

    def toggle_fullscreen(self):
        """Переключить полноэкранный режим"""
        if self.isFullScreen():
            self.showMaximized()  # Возвращаем в развернутое состояние, но не в обычное
            # Обновляем иконку в title_bar
            if hasattr(self, 'title_bar'):
                self.title_bar.maximize_btn.setText("□")
                self.title_bar.maximize_btn.setToolTip("Развернуть")
        else:
            self.showFullScreen()
            # Обновляем иконку в title_bar
            if hasattr(self, 'title_bar'):
                self.title_bar.maximize_btn.setText("❐")
                self.title_bar.maximize_btn.setToolTip("Восстановить")

    def focus_url_bar(self):
        """Фокусировка на адресной строке"""
        self.nav_bar.url_bar.setFocus()
        self.nav_bar.url_bar.selectAll()

    def focus_search(self):
        """Фокусировка на поиске"""
        self.nav_bar.url_bar.setFocus()
        self.nav_bar.url_bar.clear()
        self.nav_bar.url_bar.setPlaceholderText("Поиск...")

    def zoom_in(self):
        """Увеличить масштаб"""
        browser = self.current_browser()
        if browser:
            browser.setZoomFactor(browser.zoomFactor() + 0.1)

    def zoom_out(self):
        """Уменьшить масштаб"""
        browser = self.current_browser()
        if browser:
            browser.setZoomFactor(max(0.3, browser.zoomFactor() - 0.1))

    def zoom_reset(self):
        """Сбросить масштаб"""
        browser = self.current_browser()
        if browser:
            browser.setZoomFactor(1.0)

    def print_page(self):
        """Печать страницы"""
        browser = self.current_browser()
        if browser:
            browser.page().print()

    def save_page(self):
        """Сохранить страницу"""
        browser = self.current_browser()
        if browser:
            browser.page().save()

    def find_in_page(self):
        """Поиск на странице"""
        browser = self.current_browser()
        if browser:
            browser.page().findText("")

    def stop_loading(self):
        """Остановить загрузку"""
        browser = self.current_browser()
        if browser:
            browser.stop()

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
        """Изменение темы (недоступно в инкогнито)"""
        if self.incognito:
            QMessageBox.information(self, "Режим инкогнито", 
                                   "В режиме инкогнито доступна только тёмная тема!")
            return
        self.current_theme = theme_name
        self.database.save_setting("theme", theme_name)
        self.apply_theme()

    def load_bookmarks(self):
        if not self.incognito:
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
        if self.incognito:
            QMessageBox.information(self, "Режим инкогнито", 
                                   "В режиме инкогнито нельзя добавлять закладки!")
            return
            
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
        if self.incognito:
            QMessageBox.information(self, "Режим инкогнито", 
                                   "В режиме инкогнито история не сохраняется!")
            return
        
        dialog = HistoryDialog(self)
        dialog.exec_()

    def show_all_bookmarks(self):
        if self.incognito:
            QMessageBox.information(self, "Режим инкогнито", 
                                   "В режиме инкогнито нет закладок!")
            return
            
        dialog = BookmarksDialog(self)
        dialog.exec_()

    def clear_history(self):
        if self.incognito:
            return
            
        reply = QMessageBox.question(
            self, "Очистка истории",
            "Вы уверены, что хотите очистить всю историю?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.database.clear_history()
            QMessageBox.information(self, "Успех", "История очищена!")

    def add_to_history(self, title, url):
        """Добавляет запись в историю только если не в режиме инкогнито"""
        if not self.incognito and self.database:
            self.database.add_to_history(title, url)

    def closeEvent(self, event):
        # Очищаем ресурсы
        if hasattr(self, 'tabs'):
            self.tabs.deleteLater()
        if not self.incognito and hasattr(self, 'database'):
            self.database.close()
        event.accept()