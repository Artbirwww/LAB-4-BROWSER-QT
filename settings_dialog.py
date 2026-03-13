from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                             QWidget, QLabel, QComboBox, QLineEdit, QPushButton,
                             QFileDialog, QCheckBox, QGroupBox, QRadioButton,
                             QButtonGroup, QSpinBox, QMessageBox)
from PyQt5.QtCore import Qt, QSettings
import winreg
import os
import sys

class SettingsDialog(QDialog):
    """Диалог настроек браузера"""
    
    def __init__(self, browser_window, parent=None):
        super().__init__(parent or browser_window)
        self.browser_window = browser_window
        self.settings = QSettings('Povtias', 'Browser')
        
        self.setWindowTitle("Настройки")
        self.setGeometry(200, 200, 600, 500)
        self.setMinimumSize(550, 450)
        
        # Применяем тему
        theme = browser_window.current_theme
        if hasattr(browser_window, 'theme_switcher'):
            self.setStyleSheet(browser_window.theme_switcher.get_dialog_style(theme))
            
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Создаем вкладки
        self.tabs = QTabWidget()
        
        # Вкладка "Основные"
        self.general_tab = self.create_general_tab()
        self.tabs.addTab(self.general_tab, "⚙️ Основные")
        
        # Вкладка "Поиск"
        self.search_tab = self.create_search_tab()
        self.tabs.addTab(self.search_tab, "🔍 Поиск")
        
        # Вкладка "Загрузки"
        self.downloads_tab = self.create_downloads_tab()
        self.tabs.addTab(self.downloads_tab, "⬇️ Загрузки")
        
        # Вкладка "Приватность"
        self.privacy_tab = self.create_privacy_tab()
        self.tabs.addTab(self.privacy_tab, "🛡️ Приватность")
        
        main_layout.addWidget(self.tabs)
        
        # Кнопки
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.save_settings)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                padding: 8px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
        """)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #ccc;
                padding: 8px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        button_layout.addWidget(cancel_btn)
        
        main_layout.addLayout(button_layout)
        
    def create_general_tab(self):
        """Создает вкладку основных настроек"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Домашняя страница
        home_group = QGroupBox("Домашняя страница")
        home_layout = QVBoxLayout(home_group)
        
        self.home_radio_current = QRadioButton("Текущая страница")
        self.home_radio_current.toggled.connect(self.on_home_radio_toggled)
        home_layout.addWidget(self.home_radio_current)
        
        self.home_radio_blank = QRadioButton("Пустая страница")
        home_layout.addWidget(self.home_radio_blank)
        
        self.home_radio_custom = QRadioButton("Другая страница:")
        home_layout.addWidget(self.home_radio_custom)
        
        custom_home_layout = QHBoxLayout()
        custom_home_layout.addSpacing(20)
        self.home_custom_edit = QLineEdit()
        self.home_custom_edit.setPlaceholderText("https://ya.ru")
        custom_home_layout.addWidget(self.home_custom_edit)
        home_layout.addLayout(custom_home_layout)
        
        layout.addWidget(home_group)
        
        # Язык интерфейса
        lang_group = QGroupBox("Язык интерфейса")
        lang_layout = QHBoxLayout(lang_group)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("Русский", "ru")
        self.lang_combo.addItem("English", "en")
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        
        layout.addWidget(lang_group)
        
        # Тема оформления
        theme_group = QGroupBox("Тема оформления")
        theme_layout = QHBoxLayout(theme_group)
        
        self.theme_combo = QComboBox()
        for theme_name in self.browser_window.theme_switcher.get_theme_names():
            theme_info = self.browser_window.theme_switcher.THEMES[theme_name]
            self.theme_combo.addItem(theme_info['name'], theme_name)
            
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        
        layout.addWidget(theme_group)
        
        # Браузер по умолчанию
        default_group = QGroupBox("Браузер по умолчанию")
        default_layout = QVBoxLayout(default_group)
        
        self.default_check_label = QLabel()
        default_layout.addWidget(self.default_check_label)
        
        self.set_default_btn = QPushButton("Сделать браузером по умолчанию")
        self.set_default_btn.clicked.connect(self.set_as_default_browser)
        default_layout.addWidget(self.set_default_btn)
        
        layout.addWidget(default_group)
        
        # Обновляем статус после создания всех виджетов
        self.update_default_browser_status()
        
        layout.addStretch()
        return widget
        
    def create_search_tab(self):
        """Создает вкладку настроек поиска"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Поисковая система по умолчанию
        search_group = QGroupBox("Поисковая система по умолчанию")
        search_layout = QVBoxLayout(search_group)
        
        self.search_combo = QComboBox()
        
        # Добавляем популярные поисковые системы
        search_engines = [
            ("Яндекс", "https://ya.ru/search/?text="),
            ("Google", "https://www.google.com/search?q="),
            ("DuckDuckGo", "https://duckduckgo.com/?q="),
            ("Bing", "https://www.bing.com/search?q="),
            ("Mail.ru", "https://go.mail.ru/search?q=")
        ]
        
        for name, url in search_engines:
            self.search_combo.addItem(name, url)
            
        search_layout.addWidget(self.search_combo)
        
        # Добавляем информационную метку
        info_label = QLabel(
            "Поисковая система будет использоваться при вводе запросов\n"
            "в адресную строку (если введенный текст не является URL)"
        )
        info_label.setStyleSheet("color: #666; font-size: 11px; padding: 5px;")
        info_label.setWordWrap(True)
        search_layout.addWidget(info_label)
        
        layout.addWidget(search_group)
        
        # Дополнительные настройки поиска
        extra_group = QGroupBox("Дополнительные настройки")
        extra_layout = QVBoxLayout(extra_group)
        
        self.search_suggestions = QCheckBox("Показывать подсказки при поиске")
        self.search_suggestions.setChecked(True)
        extra_layout.addWidget(self.search_suggestions)
        
        self.search_history = QCheckBox("Сохранять историю поиска")
        self.search_history.setChecked(True)
        extra_layout.addWidget(self.search_history)
        
        layout.addWidget(extra_group)
        
        layout.addStretch()
        return widget
        
    def create_downloads_tab(self):
        """Создает вкладку настроек загрузок"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Папка для загрузок
        folder_group = QGroupBox("Папка для загрузок")
        folder_layout = QVBoxLayout(folder_group)
        
        # Текущая папка
        folder_path_layout = QHBoxLayout()
        self.download_folder_label = QLabel()
        folder_path_layout.addWidget(self.download_folder_label, 1)
        
        self.change_folder_btn = QPushButton("Изменить")
        self.change_folder_btn.clicked.connect(self.change_download_folder)
        folder_path_layout.addWidget(self.change_folder_btn)
        
        folder_layout.addLayout(folder_path_layout)
        
        # Кнопка открыть папку
        open_folder_btn = QPushButton("📁 Открыть папку загрузок")
        open_folder_btn.clicked.connect(self.open_download_folder)
        folder_layout.addWidget(open_folder_btn)
        
        layout.addWidget(folder_group)
        
        # Поведение при загрузке
        behavior_group = QGroupBox("Поведение при загрузке")
        behavior_layout = QVBoxLayout(behavior_group)
        
        self.ask_location = QCheckBox("Всегда спрашивать, куда сохранять файлы")
        behavior_layout.addWidget(self.ask_location)
        
        self.show_notifications = QCheckBox("Показывать уведомления о завершении загрузки")
        self.show_notifications.setChecked(True)
        behavior_layout.addWidget(self.show_notifications)
        
        self.auto_open = QCheckBox("Автоматически открывать загруженные файлы")
        behavior_layout.addWidget(self.auto_open)
        
        layout.addWidget(behavior_group)
        
        # Очистка загрузок
        cleanup_group = QGroupBox("Очистка")
        cleanup_layout = QVBoxLayout(cleanup_group)
        
        self.clear_on_exit = QCheckBox("Очищать список завершенных загрузок при выходе")
        cleanup_layout.addWidget(self.clear_on_exit)
        
        layout.addWidget(cleanup_group)
        
        # Обновляем метку после создания
        self.update_download_folder_label()
        
        layout.addStretch()
        return widget
        
    def create_privacy_tab(self):
        """Создает вкладку настроек приватности"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # История
        history_group = QGroupBox("История")
        history_layout = QVBoxLayout(history_group)
        
        self.save_history = QCheckBox("Сохранять историю просмотров")
        self.save_history.setChecked(True)
        history_layout.addWidget(self.save_history)
        
        clear_history_btn = QPushButton("Очистить историю")
        clear_history_btn.clicked.connect(self.clear_history)
        history_layout.addWidget(clear_history_btn)
        
        layout.addWidget(history_group)
        
        # Куки и данные сайтов
        cookies_group = QGroupBox("Куки и данные сайтов")
        cookies_layout = QVBoxLayout(cookies_group)
        
        self.allow_cookies = QCheckBox("Разрешить сохранение куки")
        self.allow_cookies.setChecked(True)
        cookies_layout.addWidget(self.allow_cookies)
        
        self.block_third_party = QCheckBox("Блокировать сторонние куки")
        cookies_layout.addWidget(self.block_third_party)
        
        clear_cookies_btn = QPushButton("Очистить все куки")
        clear_cookies_btn.clicked.connect(self.clear_cookies)
        cookies_layout.addWidget(clear_cookies_btn)
        
        layout.addWidget(cookies_group)
        
        # Кеш
        cache_group = QGroupBox("Кеш")
        cache_layout = QVBoxLayout(cache_group)
        
        cache_size_layout = QHBoxLayout()
        cache_size_layout.addWidget(QLabel("Размер кеша:"))
        
        self.cache_size_spin = QSpinBox()
        self.cache_size_spin.setRange(50, 1000)
        self.cache_size_spin.setSuffix(" МБ")
        self.cache_size_spin.setValue(250)
        cache_size_layout.addWidget(self.cache_size_spin)
        cache_size_layout.addStretch()
        
        cache_layout.addLayout(cache_size_layout)
        
        clear_cache_btn = QPushButton("Очистить кеш")
        clear_cache_btn.clicked.connect(self.clear_cache)
        cache_layout.addWidget(clear_cache_btn)
        
        layout.addWidget(cache_group)
        
        layout.addStretch()
        return widget
        
    def on_home_radio_toggled(self):
        """Обрабатывает переключение радио-кнопок домашней страницы"""
        self.home_custom_edit.setEnabled(self.home_radio_custom.isChecked())
        
    def update_default_browser_status(self):
        """Обновляет статус браузера по умолчанию"""
        if self.is_default_browser():
            self.default_check_label.setText("✅ Браузер POVTIAS CO. INC. является браузером по умолчанию")
            self.set_default_btn.setEnabled(False)
        else:
            self.default_check_label.setText("❌ Браузер POVTIAS CO. INC. не является браузером по умолчанию")
            self.set_default_btn.setEnabled(True)
            
    def is_default_browser(self):
        """Проверяет, является ли текущий браузер браузером по умолчанию"""
        if sys.platform == 'win32':
            try:
                # Проверяем в реестре Windows
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice")
                progid, _ = winreg.QueryValueEx(key, 'Progid')
                return 'povtias' in progid.lower()
            except:
                return False
        return False
        
    def set_as_default_browser(self):
        """Устанавливает браузер как браузер по умолчанию"""
        if sys.platform == 'win32':
            try:
                # Для Windows используем системный диалог
                os.system('start ms-settings:defaultapps')
                QMessageBox.information(
                    self,
                    "Настройка браузера по умолчанию",
                    "Пожалуйста, выберите POVTIAS CO. INC. BROWSER в открывшемся окне настроек."
                )
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось открыть настройки: {e}")
                
    def change_download_folder(self):
        """Изменяет папку для загрузок"""
        current_folder = self.browser_window.get_download_folder()
        
        folder = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку для загрузок",
            current_folder
        )
        
        if folder:
            self.browser_window.set_download_folder(folder)
            self.update_download_folder_label()
            
    def update_download_folder_label(self):
        """Обновляет метку с папкой загрузок"""
        folder = self.browser_window.get_download_folder()
        self.download_folder_label.setText(folder)
        
    def open_download_folder(self):
        """Открывает папку загрузок"""
        folder = self.browser_window.get_download_folder()
        if os.path.exists(folder):
            os.startfile(folder)
            
    def clear_history(self):
        """Очищает историю просмотров"""
        reply = QMessageBox.question(
            self,
            "Очистка истории",
            "Вы уверены, что хотите очистить всю историю просмотров?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.browser_window.database.clear_history()
            QMessageBox.information(self, "Успех", "История очищена!")
            
    def clear_cookies(self):
        """Очищает куки"""
        reply = QMessageBox.question(
            self,
            "Очистка куки",
            "Вы уверены, что хотите очистить все куки?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Очищаем куки для всех профилей
            for i in range(self.browser_window.tabs.count()):
                browser = self.browser_window.tabs.browsers[i]
                if browser and browser.page():
                    profile = browser.page().profile()
                    profile.cookieStore().deleteAllCookies()
                    
            QMessageBox.information(self, "Успех", "Куки очищены!")
            
    def clear_cache(self):
        """Очищает кеш"""
        reply = QMessageBox.question(
            self,
            "Очистка кеша",
            "Вы уверены, что хотите очистить кеш?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Очищаем HTTP кеш для всех профилей
            for i in range(self.browser_window.tabs.count()):
                browser = self.browser_window.tabs.browsers[i]
                if browser and browser.page():
                    profile = browser.page().profile()
                    profile.clearHttpCache()
                    
            QMessageBox.information(self, "Успех", "Кеш очищен!")
            
    def load_settings(self):
        """Загружает настройки из QSettings"""
        # Основные настройки
        home_page = self.settings.value('home_page', 'https://ya.ru')
        if home_page == 'about:blank':
            self.home_radio_blank.setChecked(True)
        elif home_page == 'current':
            self.home_radio_current.setChecked(True)
        else:
            self.home_radio_custom.setChecked(True)
            self.home_custom_edit.setText(home_page)
            
        # Тема
        theme = self.settings.value('theme', 'light')
        index = self.theme_combo.findData(theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
            
        # Поиск
        search_engine = self.settings.value('search_engine', 'https://ya.ru/search/?text=')
        index = self.search_combo.findData(search_engine)
        if index >= 0:
            self.search_combo.setCurrentIndex(index)
            
        self.search_suggestions.setChecked(
            self.settings.value('search_suggestions', True, type=bool)
        )
        self.search_history.setChecked(
            self.settings.value('search_history', True, type=bool)
        )
        
        # Загрузки
        self.ask_location.setChecked(
            self.settings.value('ask_download_location', False, type=bool)
        )
        self.show_notifications.setChecked(
            self.settings.value('download_notifications', True, type=bool)
        )
        self.auto_open.setChecked(
            self.settings.value('auto_open_downloads', False, type=bool)
        )
        self.clear_on_exit.setChecked(
            self.settings.value('clear_downloads_on_exit', False, type=bool)
        )
        
        # Приватность
        self.save_history.setChecked(
            self.settings.value('save_history', True, type=bool)
        )
        self.allow_cookies.setChecked(
            self.settings.value('allow_cookies', True, type=bool)
        )
        self.block_third_party.setChecked(
            self.settings.value('block_third_party_cookies', False, type=bool)
        )
        
        self.cache_size_spin.setValue(
            self.settings.value('cache_size', 250, type=int)
        )
        
    def save_settings(self):
        """Сохраняет настройки в QSettings"""
        # Основные настройки
        if self.home_radio_blank.isChecked():
            self.settings.setValue('home_page', 'about:blank')
        elif self.home_radio_current.isChecked():
            self.settings.setValue('home_page', 'current')
        else:
            self.settings.setValue('home_page', self.home_custom_edit.text())
            
        # Тема
        theme = self.theme_combo.currentData()
        self.settings.setValue('theme', theme)
        if hasattr(self.browser_window, 'change_theme'):
            self.browser_window.change_theme(theme)
            
        # Поиск
        search_engine = self.search_combo.currentData()
        self.settings.setValue('search_engine', search_engine)
        self.settings.setValue('search_suggestions', self.search_suggestions.isChecked())
        self.settings.setValue('search_history', self.search_history.isChecked())
        
        # Загрузки
        self.settings.setValue('ask_download_location', self.ask_location.isChecked())
        self.settings.setValue('download_notifications', self.show_notifications.isChecked())
        self.settings.setValue('auto_open_downloads', self.auto_open.isChecked())
        self.settings.setValue('clear_downloads_on_exit', self.clear_on_exit.isChecked())
        
        # Приватность
        self.settings.setValue('save_history', self.save_history.isChecked())
        self.settings.setValue('allow_cookies', self.allow_cookies.isChecked())
        self.settings.setValue('block_third_party_cookies', self.block_third_party.isChecked())
        self.settings.setValue('cache_size', self.cache_size_spin.value())
        
        self.settings.sync()
        
        QMessageBox.information(self, "Успех", "Настройки сохранены!")
        self.accept()