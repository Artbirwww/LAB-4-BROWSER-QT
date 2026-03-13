from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox, QInputDialog, QShortcut, QFileDialog, QDialog
from PyQt5.QtCore import Qt, QPoint, QUrl, QStandardPaths, QSettings, QTimer
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineDownloadItem

from database import Database
from theme_switcher import ThemeManager
from title_bar import TitleBar
from navbar import NavigationBar
from favourites import BookmarksBar
from tab_widget import TabWidget
from history_dialog import HistoryDialog
from favourites_dialog import BookmarksDialog
from downloads_dialog import DownloadsDialog
from settings_dialog import SettingsDialog
import os

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
        
        # Инициализация загрузок и настроек
        self.downloads = []
        self.download_folder = self.get_default_download_folder()
        self.settings = QSettings('Povtias', 'Browser')
        self.search_engine = self.settings.value('search_engine', 'https://ya.ru/search/?text=')
        self.downloads_dialog = None

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

        # Загрузки и настройки
        self.shortcut_downloads = QShortcut(QKeySequence("Ctrl+J"), self)
        self.shortcut_downloads.activated.connect(self.show_downloads)

        self.shortcut_settings = QShortcut(QKeySequence("Ctrl+,"), self)
        self.shortcut_settings.activated.connect(self.show_settings)

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
            self.showMaximized()
            if hasattr(self, 'title_bar'):
                self.title_bar.maximize_btn.setText("□")
                self.title_bar.maximize_btn.setToolTip("Развернуть")
        else:
            self.showFullScreen()
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
        self.settings.setValue('theme', theme_name)
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
        """Открывает URL или выполняет поиск"""
        if url:
            if not url.startswith("http") and not url.startswith("https") and not url.startswith("about:"):
                if "." in url and not " " in url and not url.startswith("localhost"):
                    url = "http://" + url
                else:
                    # Используем выбранную поисковую систему
                    search_engine = self.get_search_engine()
                    url = search_engine + url.replace(" ", "+")
                    
            self.current_browser().setUrl(QUrl(url))

    def go_home(self):
        """Переходит на домашнюю страницу"""
        home_page = self.settings.value('home_page', 'https://ya.ru')
        
        if home_page == 'about:blank':
            self.current_browser().setUrl(QUrl("about:blank"))
        elif home_page == 'current':
            # Остаемся на текущей странице
            pass
        else:
            self.current_browser().setUrl(QUrl(home_page))

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

    def get_default_download_folder(self):
        """Возвращает папку загрузок по умолчанию"""
        return QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)
        
    def get_download_folder(self):
        """Возвращает текущую папку загрузок"""
        return self.settings.value('download_folder', self.download_folder)
        
    def set_download_folder(self, folder):
        """Устанавливает папку загрузок"""
        self.settings.setValue('download_folder', folder)
        self.download_folder = folder
        
    def handle_download(self, download_item):
        """Обрабатывает начало загрузки"""
        # Получаем настройки
        ask_location = self.settings.value('ask_download_location', False, type=bool)
        download_folder = self.get_download_folder()
        
        # Формируем имя файла
        suggested_filename = download_item.suggestedFileName()
        if not suggested_filename:
            # Пытаемся извлечь имя из URL
            url_path = download_item.url().path()
            suggested_filename = os.path.basename(url_path) if url_path else "download"
            
        if ask_location:
            # Спрашиваем, куда сохранить
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить файл",
                os.path.join(download_folder, suggested_filename),
                "Все файлы (*.*)"
            )
            if file_path:
                download_item.setPath(file_path)
                download_item.accept()
                self.add_to_downloads(download_item)
            else:
                download_item.cancel()
        else:
            # Сохраняем в папку загрузок
            file_path = os.path.join(download_folder, suggested_filename)
            
            # Если файл уже существует, добавляем номер
            counter = 1
            base, ext = os.path.splitext(file_path)
            while os.path.exists(file_path):
                file_path = f"{base} ({counter}){ext}"
                counter += 1
                
            download_item.setPath(file_path)
            download_item.accept()
            self.add_to_downloads(download_item)
            
            # Показываем уведомление о начале загрузки
            if self.settings.value('download_notifications', True, type=bool):
                self.show_notification("Загрузка начата", suggested_filename)
                
    def add_to_downloads(self, download_item):
        """Добавляет загрузку в список"""
        self.downloads.append(download_item)
        
        # Подключаем сигналы
        download_item.stateChanged.connect(
            lambda state, item=download_item: self.download_state_changed(state, item)
        )
        
        # Если диалог загрузок открыт, добавляем туда
        if self.downloads_dialog and self.downloads_dialog.isVisible():
            self.downloads_dialog.add_download(download_item)
            
    def download_state_changed(self, state, download_item):
        """Обрабатывает изменение состояния загрузки"""
        if state == QWebEngineDownloadItem.DownloadCompleted:
            file_path = download_item.path()
            file_name = os.path.basename(file_path)
            
            # Сохраняем в историю загрузок
            if not self.incognito and self.database:
                self.database.add_download(
                    file_name,
                    download_item.url().toString(),
                    file_path,
                    download_item.totalBytes()
                )
                self.database.finish_download(download_item.id())
            
            # Уведомление о завершении
            if self.settings.value('download_notifications', True, type=bool):
                self.show_download_notification(file_name, file_path)
                
            # Автоматическое открытие
            if self.settings.value('auto_open_downloads', False, type=bool):
                self.open_downloaded_file(file_path)
                
        elif state == QWebEngineDownloadItem.DownloadInterrupted:
            if self.settings.value('download_notifications', True, type=bool):
                self.show_notification(
                    "❌ Ошибка загрузки",
                    f"Не удалось загрузить {os.path.basename(download_item.path())}: {download_item.interruptReasonString()}"
                )
                
    def show_download_notification(self, file_name, file_path):
        """Показывает уведомление о завершении загрузки с действиями"""
        try:
            from PyQt5.QtWidgets import QSystemTrayIcon
            
            if not hasattr(self, 'tray_icon'):
                self.tray_icon = QSystemTrayIcon(self)
                self.tray_icon.setIcon(self.windowIcon())
                self.tray_icon.show()
            
            # Создаем уведомление
            message = f"Файл {file_name} успешно загружен"
            self.tray_icon.showMessage(
                "✅ Загрузка завершена",
                message,
                QSystemTrayIcon.Information,
                5000
            )
            
            # Сохраняем информацию о последнем загруженном файле
            self.last_downloaded_file = file_path
            
            # Подключаем обработчик клика по уведомлению
            self.tray_icon.messageClicked.connect(lambda: self.open_last_download())
            
        except Exception as e:
            print(f"Ошибка при показе уведомления: {e}")
            
    def open_last_download(self):
        """Открывает последний загруженный файл"""
        if hasattr(self, 'last_downloaded_file') and os.path.exists(self.last_downloaded_file):
            os.startfile(self.last_downloaded_file)
            
    def show_download_completed_dialog(self, file_name, file_path):
        """Показывает диалог с информацией о завершении загрузки"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Загрузка завершена")
        dialog.setFixedSize(400, 200)
        
        # Применяем тему
        if hasattr(self, 'theme_switcher'):
            dialog.setStyleSheet(self.theme_switcher.get_dialog_style(self.current_theme))
        
        layout = QVBoxLayout(dialog)
        
        # Иконка и сообщение
        message_layout = QHBoxLayout()
        
        icon_label = QLabel("✅")
        icon_label.setStyleSheet("font-size: 48px;")
        message_layout.addWidget(icon_label)
        
        text_layout = QVBoxLayout()
        text_layout.addWidget(QLabel(f"<b>Файл успешно загружен:</b>"))
        text_layout.addWidget(QLabel(file_name))
        text_layout.addWidget(QLabel(f"<small>{file_path}</small>"))
        message_layout.addLayout(text_layout)
        
        layout.addLayout(message_layout)
        
        layout.addStretch()
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        open_btn = QPushButton("📁 Открыть файл")
        open_btn.clicked.connect(lambda: (os.startfile(file_path), dialog.close()))
        button_layout.addWidget(open_btn)
        
        open_folder_btn = QPushButton("📂 Открыть папку")
        open_folder_btn.clicked.connect(lambda: (os.startfile(os.path.dirname(file_path)), dialog.close()))
        button_layout.addWidget(open_folder_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(dialog.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        dialog.exec_()
                
    def open_downloaded_file(self, file_path):
        """Открывает загруженный файл"""
        if os.path.exists(file_path):
            os.startfile(file_path)
            
    def show_notification(self, title, message):
        """Показывает системное уведомление"""
        try:
            from PyQt5.QtWidgets import QSystemTrayIcon
            if not hasattr(self, 'tray_icon'):
                self.tray_icon = QSystemTrayIcon(self)
                self.tray_icon.setIcon(self.windowIcon())
                self.tray_icon.show()
                
            self.tray_icon.showMessage(title, message, QSystemTrayIcon.Information, 3000)
        except:
            pass
            
    def show_downloads(self):
        """Показывает диалог загрузок"""
        if not self.downloads_dialog:
            from downloads_dialog import DownloadsDialog
            self.downloads_dialog = DownloadsDialog(self)
            
        self.downloads_dialog.show()
        self.downloads_dialog.raise_()
        self.downloads_dialog.activateWindow()
        
    def show_settings(self):
        """Показывает диалог настроек"""
        from settings_dialog import SettingsDialog
        dialog = SettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Применяем настройки поисковой системы
            self.update_search_engine()
            
    def update_search_engine(self):
        """Обновляет поисковую систему"""
        self.search_engine = self.settings.value('search_engine', 'https://ya.ru/search/?text=')
        
    def get_search_engine(self):
        """Возвращает URL поисковой системы"""
        if not hasattr(self, 'search_engine'):
            self.update_search_engine()
        return self.search_engine

    def closeEvent(self, event):
        # Очищаем ресурсы
        if hasattr(self, 'tabs'):
            self.tabs.deleteLater()
        if not self.incognito and hasattr(self, 'database'):
            self.database.close()
            
        # Очищаем загрузки при выходе если настроено
        if self.settings.value('clear_downloads_on_exit', False, type=bool):
            self.downloads.clear()
            
        event.accept()