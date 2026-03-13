from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabBar, QStackedWidget, QPushButton, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtCore import QUrl, Qt

class TabWidget(QWidget):
    def __init__(self, browser_window, incognito=False):
        super().__init__()
        self.browser_window = browser_window
        self.incognito = incognito

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Создаем горизонтальный контейнер для панели вкладок и кнопок
        tab_container = QWidget()
        tab_layout = QHBoxLayout(tab_container)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(0)

        # Создаем панель вкладок
        self.tab_bar = QTabBar()
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.setMovable(True)
        self.tab_bar.setExpanding(False)
        self.tab_bar.setDrawBase(False)
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
        self.tab_bar.currentChanged.connect(self.tab_changed)

        # Кнопка новой вкладки
        self.new_tab_btn = QPushButton()
        self.new_tab_btn.setFixedSize(28, 28)
        self.new_tab_btn.setCursor(Qt.PointingHandCursor)
        self.new_tab_btn.clicked.connect(lambda: self.add_new_tab())
        self.new_tab_btn.setToolTip("Новая вкладка (Ctrl+T)")
        self.new_tab_btn.setText("+")

        # Кнопка нового окна инкогнито
        self.incognito_btn = QPushButton()
        self.incognito_btn.setFixedSize(28, 28)
        self.incognito_btn.setCursor(Qt.PointingHandCursor)
        self.incognito_btn.clicked.connect(self.open_incognito_window)
        self.incognito_btn.setToolTip("Новое окно инкогнито (Ctrl+Shift+N)")
        self.incognito_btn.setText("🕶️")

        # Добавляем вкладки и кнопки в контейнер
        tab_layout.addWidget(self.tab_bar)
        tab_layout.addWidget(self.new_tab_btn)
        tab_layout.addWidget(self.incognito_btn)
        tab_layout.addStretch()

        # Создаем стек для содержимого вкладок
        self.stack = QStackedWidget()

        layout.addWidget(tab_container)
        layout.addWidget(self.stack)

        self.browsers = []
        self.profiles = []  # Сохраняем ссылки на профили для предотвращения удаления

        # Устанавливаем стиль
        self.setup_style()

    def open_incognito_window(self):
        """Открывает новое окно в режиме инкогнито"""
        from browser_window import AdvancedBrowser
        self.incognito_window = AdvancedBrowser(incognito=True)
        self.incognito_window.show()

    def add_new_tab(self, qurl=None):
        """Добавляет новую вкладку"""
        try:
            if qurl is None:
                qurl = QUrl("https://ya.ru")
            elif isinstance(qurl, str):
                qurl = QUrl(qurl)

            # Создаем браузер с соответствующим профилем
            if self.incognito:
                # Для инкогнито создаем временный профиль с уникальным именем
                profile = QWebEngineProfile()  # Временный профиль
                self.profiles.append(profile)  # Сохраняем ссылку
                browser = QWebEngineView()
                page = QWebEnginePage(profile, browser)
                browser.setPage(page)
            else:
                browser = QWebEngineView()
                # Используем стандартный профиль

            browser.setUrl(qurl)

            # Настраиваем профиль для инкогнито - отключаем сохранение данных
            if self.incognito:
                profile = browser.page().profile()
                profile.setHttpCacheType(QWebEngineProfile.NoCache)
                profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
                profile.setPersistentStoragePath("")  # Отключаем постоянное хранилище

            # Подключаем сигнал загрузки
            browser.page().profile().downloadRequested.connect(
                self.browser_window.handle_download
            )

            self.stack.addWidget(browser)
            self.browsers.append(browser)

            # Добавляем индикатор инкогнито в заголовок вкладки
            tab_text = "● Загрузка..."
            if self.incognito:
                tab_text = "🕶️ " + tab_text

            index = self.tab_bar.addTab(tab_text)
            self.tab_bar.setTabData(index, {"loading": True, "url": qurl.toString(), "browser": browser})
            self.tab_bar.setCurrentIndex(index)
            self.stack.setCurrentIndex(index)

            browser.urlChanged.connect(
                lambda url, b=browser: self.browser_window.update_url_bar(url, b)
            )
            browser.loadFinished.connect(
                lambda ok, b=browser: self.update_title(b)
            )
            browser.loadStarted.connect(
                lambda: self.set_tab_loading(index, True)
            )

            # Добавляем в историю только если не в режиме инкогнито
            if not self.incognito:
                self.browser_window.add_to_history("Загрузка...", qurl.toString())

            print(f"Добавлена новая вкладка{' (инкогнито)' if self.incognito else ''}. Всего вкладок: {self.count()}")

        except Exception as e:
            print(f"Ошибка при создании вкладки: {e}")

    def set_tab_loading(self, index, loading):
        if 0 <= index < self.tab_bar.count():
            data = self.tab_bar.tabData(index) or {}
            data['loading'] = loading
            self.tab_bar.setTabData(index, data)

    def current_browser(self):
        current_index = self.stack.currentIndex()
        if current_index >= 0 and current_index < len(self.browsers):
            return self.browsers[current_index]
        return None

    def count(self):
        return len(self.browsers)

    def tab_changed(self, index):
        if index >= 0 and index < len(self.browsers):
            self.stack.setCurrentIndex(index)
            browser = self.browsers[index]
            if browser:
                self.browser_window.update_url_bar(browser.url(), browser)

    def update_title(self, browser):
        """Обновляет заголовок вкладки"""
        try:
            if browser in self.browsers:
                index = self.browsers.index(browser)
                title = browser.page().title()
                if title:
                    short_title = title[:20] + "…" if len(title) > 20 else title

                    # Добавляем индикатор инкогнито
                    if self.incognito:
                        short_title = "🕶️ " + short_title

                    self.tab_bar.setTabText(index, f" {short_title}")
                    self.set_tab_loading(index, False)

                    if browser == self.current_browser():
                        self.browser_window.title_bar.update_title(short_title)

                    # Добавляем в историю только если не в режиме инкогнито
                    if not self.incognito:
                        self.browser_window.add_to_history(title, browser.url().toString())
        except Exception as e:
            print(f"Ошибка при обновлении заголовка: {e}")

    def close_tab(self, index):
        if len(self.browsers) > 1:
            browser = self.browsers[index]

            # Получаем профиль до удаления
            if self.incognito:
                try:
                    profile = browser.page().profile()
                    # Удаляем страницу перед удалением браузера
                    page = browser.page()
                    browser.setPage(None)  # Отвязываем страницу
                    page.deleteLater()
                except:
                    pass

            self.stack.removeWidget(browser)
            browser.deleteLater()
            self.browsers.pop(index)
            self.tab_bar.removeTab(index)

            # Очищаем неиспользуемые профили
            if self.incognito:
                # Оставляем только профили для существующих браузеров
                self.profiles = [p for p in self.profiles if any(
                    hasattr(b.page(), 'profile') and b.page().profile() == p
                    for b in self.browsers
                )]
        else:
            self.browser_window.close()

    def indexOf(self, browser):
        if browser in self.browsers:
            return self.browsers.index(browser)
        return -1

    def setup_style(self):
        if self.incognito:
            # Тёмный стиль для инкогнито
            self.setStyleSheet("""
        QTabBar::tab {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #3d3d3d, stop: 1 #2d2d2d);
            border: 1px solid #555555;
            border-bottom: none;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            min-width: 140px;
            max-width: 200px;
            height: 28px;
            padding: 0px 20px 0px 10px;
            margin-right: 2px;
            margin-top: 2px;
            color: #ffffff;
            font-size: 12px;
            font-weight: 400;
        }

        QTabBar::tab:selected {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #4d4d4d, stop: 1 #3d3d3d);
            border-bottom: 1px solid #4d4d4d;
            margin-bottom: -1px;
            color: #ffffff;
            font-weight: 500;
        }

        QTabBar::tab:hover:!selected {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #4d4d4d, stop: 1 #3d3d3d);
        }

        QTabBar::tab:first {
            margin-left: 5px;
        }

        QTabBar::close-button {
            width: 0px;
        }

        QTabBar {
            qproperty-drawBase: 0;
            background-color: transparent;
            min-height: 32px;
            max-height: 32px;
        }

        QPushButton {
            background-color: transparent;
            border: none;
            border-radius: 6px;
            margin-top: 2px;
            font-size: 16px;
            color: #ffffff;
        }

        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }

        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 0.15);
        }

        QStackedWidget {
            background-color: #2d2d2d;
            border: none;
        }

        QWebEngineView {
            background-color: #2d2d2d;
        }

        QToolTip {
            background-color: #2c2c2e;
            color: #ffffff;
            border: none;
            border-radius: 5px;
            padding: 6px 10px;
            font-size: 11px;
        }
        """)
        else:
            # Обычный светлый стиль
            self.setStyleSheet("""
        QTabBar::tab {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #f9f9f9, stop: 1 #f2f2f2);
            border: 1px solid #d9d9d9;
            border-bottom: none;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            min-width: 140px;
            max-width: 200px;
            height: 28px;
            padding: 0px 20px 0px 10px;
            margin-right: 2px;
            margin-top: 2px;
            color: #333333;
            font-size: 12px;
            font-weight: 400;
        }

        QTabBar::tab:selected {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #ffffff, stop: 1 #f9f9f9);
            border-bottom: 1px solid #ffffff;
            margin-bottom: -1px;
            color: #000000;
            font-weight: 500;
        }

        QTabBar::tab:hover:!selected {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #f0f0f0, stop: 1 #e8e8e8);
        }

        QTabBar::tab:first {
            margin-left: 5px;
        }

        QTabBar::close-button {
            width: 0px;
        }

        QTabBar {
            qproperty-drawBase: 0;
            background-color: transparent;
            min-height: 32px;
            max-height: 32px;
        }

        QPushButton {
            background-color: transparent;
            border: none;
            border-radius: 6px;
            margin-top: 2px;
            font-size: 16px;
            color: #666666;
        }

        QPushButton:hover {
            background-color: rgba(0, 0, 0, 0.06);
        }

        QPushButton:pressed {
            background-color: rgba(0, 0, 0, 0.1);
        }

        QStackedWidget {
            background-color: #ffffff;
            border: none;
        }

        QWebEngineView {
            background-color: #ffffff;
        }

        QToolTip {
            background-color: #2c2c2e;
            color: #ffffff;
            border: none;
            border-radius: 5px;
            padding: 6px 10px;
            font-size: 11px;
        }
        """)