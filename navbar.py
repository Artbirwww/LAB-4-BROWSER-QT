from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit, QMenu
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer

class NavigationBar(QWidget):
    def __init__(self, browser_window):
        super().__init__()
        self.browser_window = browser_window
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)
        
        # Основной стиль для панели
        self.setStyleSheet("""
    NavigationBar {
        background-color: #f5f5f7;
        border-bottom: 1px solid #d9d9d9;
    }
    
    QPushButton {
        background-color: transparent;
        border: none;
        border-radius: 6px;
        min-width: 36px;
        max-width: 36px;
        min-height: 36px;
        max-height: 36px;
        margin: 0px 2px;
    }
    
    QPushButton:hover {
        background-color: rgba(0, 0, 0, 0.06);
    }
    
    QPushButton:pressed {
        background-color: rgba(0, 0, 0, 0.1);
    }
    
    QPushButton:disabled {
        opacity: 0.4;
    }
    
    QLineEdit {
        border: 1px solid #d9d9d9;
        border-radius: 18px;
        padding: 8px 16px;
        font-size: 14px;
        min-height: 22px;
        background-color: #ffffff;
        selection-background-color: #4a90e2;
    }
    
    QLineEdit:hover {
        border-color: #b3b3b3;
        background-color: #ffffff;
    }
    
    QLineEdit:focus {
        border-color: #0066cc;
        background-color: #ffffff;
        outline: none;
    }
    
    QLineEdit::placeholder {
        color: #8e8e93;
        font-style: italic;
    }
    
    QMenu {
        background-color: #ffffff;
        border: 0.5px solid #d9d9d9;
        border-radius: 8px;
        padding: 6px;
        font-size: 13px;
    }
    
    QMenu::item {
        padding: 8px 28px 8px 28px;
        border-radius: 5px;
        color: #1d1d1f;
    }
    
    QMenu::item:selected {
        background-color: #0066cc;
        color: #ffffff;
    }
    
    QMenu::item:disabled {
        color: #8e8e93;
    }
    
    QMenu::separator {
        height: 0.5px;
        background-color: #d9d9d9;
        margin: 6px 10px;
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
        
        # Создаем SVG иконки
        back_icon = self.create_icon_from_svg(self.get_back_svg(), 20, 20)
        forward_icon = self.create_icon_from_svg(self.get_forward_svg(), 20, 20)
        reload_icon = self.create_icon_from_svg(self.get_reload_svg(), 20, 20)
        bookmark_icon = self.create_icon_from_svg(self.get_bookmark_svg(), 20, 20)
        new_tab_icon = self.create_icon_from_svg(self.get_new_tab_svg(), 20, 20)
        
        # Кнопки навигации
        self.back_btn = QPushButton()
        self.back_btn.setIcon(back_icon)
        self.back_btn.setIconSize(self.back_btn.iconSize().scaled(20, 20, Qt.KeepAspectRatio))
        self.back_btn.setToolTip("Назад")
        self.back_btn.clicked.connect(lambda: self.browser_window.current_browser().back())
        layout.addWidget(self.back_btn)
        
        self.forward_btn = QPushButton()
        self.forward_btn.setIcon(forward_icon)
        self.forward_btn.setIconSize(self.forward_btn.iconSize().scaled(20, 20, Qt.KeepAspectRatio))
        self.forward_btn.setToolTip("Вперед")
        self.forward_btn.clicked.connect(lambda: self.browser_window.current_browser().forward())
        layout.addWidget(self.forward_btn)
        
        self.reload_btn = QPushButton()
        self.reload_btn.setIcon(reload_icon)
        self.reload_btn.setIconSize(self.reload_btn.iconSize().scaled(20, 20, Qt.KeepAspectRatio))
        self.reload_btn.setToolTip("Обновить")
        self.reload_btn.clicked.connect(lambda: self.browser_window.current_browser().reload())
        layout.addWidget(self.reload_btn)
        
        # Адресная строка
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Введите адрес или поисковый запрос...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        layout.addWidget(self.url_bar, 1)
        
        # Кнопка добавления закладки
        self.bookmark_btn = QPushButton()
        self.bookmark_btn.setIcon(bookmark_icon)
        self.bookmark_btn.setIconSize(self.bookmark_btn.iconSize().scaled(20, 20, Qt.KeepAspectRatio))
        self.bookmark_btn.setToolTip("Добавить в закладки")
        self.bookmark_btn.clicked.connect(self.browser_window.add_bookmark)
        layout.addWidget(self.bookmark_btn)
        
        # Кнопка новой вкладки
        self.new_tab_btn = QPushButton()
        self.new_tab_btn.setIcon(new_tab_icon)
        self.new_tab_btn.setIconSize(self.new_tab_btn.iconSize().scaled(20, 20, Qt.KeepAspectRatio))
        self.new_tab_btn.setToolTip("Новая вкладка")
        self.new_tab_btn.clicked.connect(self.browser_window.add_new_tab)
        layout.addWidget(self.new_tab_btn)
        
        # Кнопка меню с SVG иконкой
        self.menu_btn = QPushButton()
        self.menu_btn.setIcon(self.create_icon_from_svg(self.get_menu_svg(), 20, 20))
        self.menu_btn.setIconSize(self.menu_btn.iconSize().scaled(20, 20, Qt.KeepAspectRatio))
        self.menu_btn.setToolTip("Меню")
        self.menu_btn.clicked.connect(self.show_menu)
        layout.addWidget(self.menu_btn)
        
    def get_back_svg(self):
        return """<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 4L6 10L12 16" stroke="#666666" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>"""
    
    def get_forward_svg(self):
        return """<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M8 4L14 10L8 16" stroke="#666666" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>"""
    
    def get_reload_svg(self):
        return """<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 4L16 8L12 8" stroke="#666666" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M4 12L4 16L8 16" stroke="#666666" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M4 8C4.5 6 6.5 4 10 4C13 4 15 6 16 8" stroke="#666666" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M16 12C15.5 14 13.5 16 10 16C7 16 5 14 4 12" stroke="#666666" stroke-width="1.5" stroke-linecap="round"/>
        </svg>"""
    
    def get_bookmark_svg(self):
        return """<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M5 3.5C5 3.22386 5.22386 3 5.5 3H14.5C14.7761 3 15 3.22386 15 3.5V16.5C15 16.6899 14.874 16.8625 14.6924 16.9237C14.5108 16.9849 14.3116 16.9264 14.1874 16.78L10 12.05L5.8126 16.78C5.6884 16.9264 5.4892 16.9849 5.3076 16.9237C5.126 16.8625 5 16.6899 5 16.5V3.5Z" 
            stroke="#666666" stroke-width="1.2" fill="transparent"/>
        </svg>"""
    
    def get_new_tab_svg(self):
        return """<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="3" width="14" height="14" rx="2" stroke="#666666" stroke-width="1.2"/>
            <path d="M10 6V14M6 10H14" stroke="#666666" stroke-width="1.2" stroke-linecap="round"/>
        </svg>"""
    
    def get_menu_svg(self):
        return """<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="10" cy="5" r="1.5" fill="#666666"/>
            <circle cx="10" cy="10" r="1.5" fill="#666666"/>
            <circle cx="10" cy="15" r="1.5" fill="#666666"/>
        </svg>"""
    
    def get_lock_svg(self):
        return """<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="7" width="10" height="7" rx="1.5" stroke="#27ae60" stroke-width="1.2"/>
            <path d="M5 7V5C5 3.5 6 2 8 2C10 2 11 3.5 11 5V7" stroke="#27ae60" stroke-width="1.2" stroke-linecap="round"/>
        </svg>"""
    
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
        
    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser_window.open_url(url)
        
    def update_url(self, url):
        url_str = url.toString()
        self.url_bar.setText(url_str)
        self.url_bar.setCursorPosition(0)
        
        # Добавляем индикатор безопасности (можно расширить)
        if url_str.startswith("https://"):
            self.url_bar.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #d9d9d9;
                    border-radius: 18px;
                    padding: 8px 16px;
                    font-size: 14px;
                    background-color: #ffffff;
                }
                QLineEdit:focus {
                    border-color: #0066cc;
                }
            """)
        else:
            self.url_bar.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #d9d9d9;
                    border-radius: 18px;
                    padding: 8px 16px;
                    font-size: 14px;
                    background-color: #ffffff;
                }
                QLineEdit:focus {
                    border-color: #0066cc;
                }
            """)
        
    def show_menu(self):
        menu = QMenu(self)

        # Подменю тем
        theme_menu = menu.addMenu("🎨 Тема оформления")

        for theme_name in self.browser_window.theme_switcher.get_theme_names():
            theme_info = self.browser_window.theme_switcher.THEMES[theme_name]
            action = theme_menu.addAction(theme_info["name"])
            action.triggered.connect(lambda checked, t=theme_name: self.browser_window.change_theme(t))

        menu.addSeparator()

        # Блокировка рекламы
        ad_block_enabled = self.browser_window.database.get_setting("ad_block", "false") == "true"
        ad_block_action = menu.addAction("🚫 Блокировка рекламы")
        ad_block_action.setCheckable(True)
        ad_block_action.setChecked(ad_block_enabled)
        ad_block_action.triggered.connect(self.toggle_ad_block)

        menu.addSeparator()

        # История
        history_action = menu.addAction("📋 История")
        history_action.triggered.connect(self.browser_window.show_history)

        clear_history_action = menu.addAction("🗑 Очистить историю")
        clear_history_action.triggered.connect(self.browser_window.clear_history)

        menu.addSeparator()

        # Показываем меню под кнопкой
        menu.exec_(self.menu_btn.mapToGlobal(QPoint(0, self.menu_btn.height())))

    def toggle_ad_block(self, checked):
        """Включает/выключает блокировку рекламы"""
        self.browser_window.database.save_setting("ad_block", "true" if checked else "false")
        self.browser_window.apply_ad_block_setting()