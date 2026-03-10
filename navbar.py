from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit, QMenu
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QIcon

class NavigationBar(QWidget):
    def __init__(self, browser_window):
        super().__init__()
        self.browser_window = browser_window
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)  # Уменьшаем расстояние между кнопками
        
        # Общий стиль для всех кнопок навигации
        button_style = """
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
                padding: 4px;
                min-width: 32px;
                max-width: 32px;
                min-height: 32px;
                max-height: 32px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.2);
            }
        """
        
        # Кнопки навигации
        self.back_btn = QPushButton()
        self.back_btn.setIcon(QIcon("nav/back_8e26he9iqu7d_32.png"))
        self.back_btn.setIconSize(self.back_btn.sizeHint())
        self.back_btn.setStyleSheet(button_style)
        self.back_btn.setFixedSize(36, 36)  # Фиксированный размер
        self.back_btn.setToolTip("Назад")
        self.back_btn.clicked.connect(lambda: self.browser_window.current_browser().back())
        layout.addWidget(self.back_btn)
        
        self.forward_btn = QPushButton()
        self.forward_btn.setIcon(QIcon("nav/right_416kq89mn9be_32.png"))
        self.forward_btn.setIconSize(self.forward_btn.sizeHint())
        self.forward_btn.setStyleSheet(button_style)
        self.forward_btn.setFixedSize(36, 36)
        self.forward_btn.setToolTip("Вперед")
        self.forward_btn.clicked.connect(lambda: self.browser_window.current_browser().forward())
        layout.addWidget(self.forward_btn)
        
        self.reload_btn = QPushButton()
        self.reload_btn.setIcon(QIcon("nav/rotate_37fgt6373sl6_32.png"))
        self.reload_btn.setIconSize(self.reload_btn.sizeHint())
        self.reload_btn.setStyleSheet(button_style)
        self.reload_btn.setFixedSize(36, 36)
        self.reload_btn.setToolTip("Обновить")
        self.reload_btn.clicked.connect(lambda: self.browser_window.current_browser().reload())
        layout.addWidget(self.reload_btn)
        
        # Адресная строка с растяжением
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Введите адрес или поисковый запрос...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px;
                font-size: 14px;
                min-height: 24px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
                outline: none;
            }
        """)
        layout.addWidget(self.url_bar, 1)  # Растягивается
        
        # Кнопка добавления закладки
        self.bookmark_btn = QPushButton()
        self.bookmark_btn.setIcon(QIcon("nav/star_t3vvqsp20gur_32.png"))
        self.bookmark_btn.setIconSize(self.bookmark_btn.sizeHint())
        self.bookmark_btn.setStyleSheet(button_style)
        self.bookmark_btn.setFixedSize(36, 36)
        self.bookmark_btn.setToolTip("Добавить в закладки")
        self.bookmark_btn.clicked.connect(self.browser_window.add_bookmark)
        layout.addWidget(self.bookmark_btn)
        
        # Кнопка новой вкладки
        self.new_tab_btn = QPushButton()
        self.new_tab_btn.setIcon(QIcon("nav/add_5ztfflf69ahd_32.png"))
        self.new_tab_btn.setIconSize(self.new_tab_btn.sizeHint())
        self.new_tab_btn.setStyleSheet(button_style)
        self.new_tab_btn.setFixedSize(36, 36)
        self.new_tab_btn.setToolTip("Новая вкладка")
        self.new_tab_btn.clicked.connect(self.browser_window.add_new_tab)
        layout.addWidget(self.new_tab_btn)
        
        # Кнопка меню
        self.menu_btn = QPushButton("⋮")
        self.menu_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
                padding: 4px;
                min-width: 36px;
                max-width: 36px;
                min-height: 36px;
                max-height: 36px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.2);
            }
        """)
        self.menu_btn.setFixedSize(36, 36)
        self.menu_btn.setToolTip("Меню")
        self.menu_btn.clicked.connect(self.show_menu)
        layout.addWidget(self.menu_btn)
        
    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser_window.open_url(url)
        
    def update_url(self, url):
        self.url_bar.setText(url.toString())
        self.url_bar.setCursorPosition(0)
        
    def show_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px;
            }
            QMenu::item {
                padding: 6px 24px 6px 24px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background-color: #4a90e2;
                color: white;
            }
        """)
        
        # Подменю тем
        theme_menu = menu.addMenu("Тема оформления")
        theme_menu.setStyleSheet(menu.styleSheet())
        
        for theme_name in self.browser_window.theme_switcher.get_theme_names():
            theme_info = self.browser_window.theme_switcher.THEMES[theme_name]
            action = theme_menu.addAction(theme_info["name"])
            action.triggered.connect(lambda checked, t=theme_name: self.browser_window.change_theme(t))
        
        menu.addSeparator()
        
        # История
        history_action = menu.addAction("История")
        history_action.triggered.connect(self.browser_window.show_history)
        
        clear_history_action = menu.addAction("🗑 Очистить историю")
        clear_history_action.triggered.connect(self.browser_window.clear_history)
        
        menu.addSeparator()
        
        # Показываем меню под кнопкой
        menu.exec_(self.menu_btn.mapToGlobal(QPoint(0, self.menu_btn.height())))