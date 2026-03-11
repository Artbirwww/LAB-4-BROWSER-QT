from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabBar, QStackedWidget, QPushButton, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer

class TabWidget(QWidget):
    def __init__(self, browser_window):
        super().__init__()
        self.browser_window = browser_window
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Создаем горизонтальный контейнер для панели вкладок и кнопки
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
        self.new_tab_btn.clicked.connect(self.browser_window.add_new_tab)
        self.new_tab_btn.setToolTip("Новая вкладка")
        
        # Добавляем вкладки и кнопку в контейнер
        tab_layout.addWidget(self.tab_bar)
        tab_layout.addWidget(self.new_tab_btn)
        tab_layout.addStretch()
        
        # Создаем стек для содержимого вкладок
        self.stack = QStackedWidget()
        
        layout.addWidget(tab_container)
        layout.addWidget(self.stack)
        
        self.browsers = []
        
        # Устанавливаем стиль
        self.setup_style()
        
    def setup_style(self):
        # SVG иконка для новой вкладки
        new_tab_svg = """<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="3" width="14" height="14" rx="2" stroke="#666666" stroke-width="1.2"/>
            <path d="M10 6V14M6 10H14" stroke="#666666" stroke-width="1.2" stroke-linecap="round"/>
        </svg>"""
        
        new_tab_icon = self.create_icon_from_svg(new_tab_svg, 16, 16)
        self.new_tab_btn.setIcon(new_tab_icon)
        self.new_tab_btn.setIconSize(self.new_tab_btn.iconSize().scaled(16, 16, Qt.KeepAspectRatio))
        
        # SVG иконка для кнопки закрытия
        close_icon_svg = """<svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 3L9 9M9 3L3 9" stroke="#666666" stroke-width="1.2" stroke-linecap="round"/>
        </svg>"""
        
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
        padding: 0px 10px 0px 10px;
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
        image: url(:/close-tab.svg);
        subcontrol-position: right;
        padding: 2px;
        width: 16px;
        height: 16px;
        border-radius: 8px;
    }
    
    QTabBar::close-button:hover {
        background-color: rgba(0, 0, 0, 0.1);
    }
    
    QTabBar::close-button:pressed {
        background-color: rgba(0, 0, 0, 0.15);
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
        
    def create_icon_from_svg(self, svg_content, width, height):
        """Создает QIcon из SVG строки"""
        from PyQt5.QtCore import QByteArray
        
        renderer = QSvgRenderer(QByteArray(svg_content.encode()))
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        return QIcon(pixmap)
        
    def add_new_tab(self, qurl=None):
        try:
            if qurl is None or isinstance(qurl, bool):
                qurl = QUrl("https://ya.ru")
            elif isinstance(qurl, str):
                qurl = QUrl(qurl)
                
            browser = QWebEngineView()
            browser.setUrl(qurl)
            
            self.stack.addWidget(browser)
            self.browsers.append(browser)
            
            index = self.tab_bar.addTab("● Загрузка...")
            self.tab_bar.setTabData(index, {"loading": True, "url": qurl.toString()})
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
            
            self.browser_window.database.add_to_history("Загрузка...", qurl.toString())
            
            print(f"Добавлена новая вкладка. Всего вкладок: {self.count()}")
            
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
        try:
            if browser in self.browsers:
                index = self.browsers.index(browser)
                title = browser.page().title()
                if title:
                    short_title = title[:20] + "…" if len(title) > 20 else title
                    self.tab_bar.setTabText(index, f" {short_title}")
                    self.set_tab_loading(index, False)
                    
                    if browser == self.current_browser():
                        self.browser_window.title_bar.update_title(short_title)
                    
                    self.browser_window.database.add_to_history(title, browser.url().toString())
        except Exception as e:
            print(f"Ошибка при обновлении заголовка: {e}")
            
    def close_tab(self, index):
        if len(self.browsers) > 1:
            browser = self.browsers[index]
            self.stack.removeWidget(browser)
            browser.deleteLater()
            self.browsers.pop(index)
            self.tab_bar.removeTab(index)
        else:
            self.browser_window.close()
            
    def indexOf(self, browser):
        if browser in self.browsers:
            return self.browsers.index(browser)
        return -1