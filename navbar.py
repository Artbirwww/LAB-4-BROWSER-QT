from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit, QMenu, QFrame, QApplication
from PyQt5.QtCore import QPoint, Qt, QByteArray, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt5.QtSvg import QSvgRenderer

class NavigationBar(QWidget):
    def __init__(self, browser_window):
        super().__init__()
        self.browser_window = browser_window
        self.setup_ui()

    def get_svg_icon(self, icon_name, color="#666666", hover_color="#0066cc"):
        """Возвращает SVG иконку по имени"""

        icons = {
            "back": '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M12 4L6 10L12 16" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>''',

            "forward": '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M8 4L14 10L8 16" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>''',

            "reload": '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M15 8L18 5L15 2" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M3 12L6 15L3 18" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M18 5C18 10 14 14 9 14C6.5 14 4.5 13 3 11.5" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>
                <path d="M2 9C2 4 6 2 9 2C11.5 2 14 4 15 6" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>
            </svg>''',

            "home": '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M3 9L10 3L17 9V17H13V12H7V17H3V9Z" stroke="{color}" stroke-width="1.5" stroke-linejoin="round"/>
            </svg>''',

            "bookmark": '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M5 3H15V17L10 13L5 17V3Z" stroke="{color}" stroke-width="1.5" stroke-linejoin="round"/>
            </svg>''',

            "bookmark_filled": '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M5 3H15V17L10 13L5 17V3Z" fill="{color}" stroke="{color}" stroke-width="1.5" stroke-linejoin="round"/>
            </svg>''',

            "new_tab": '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <rect x="3" y="3" width="14" height="14" rx="2" stroke="{color}" stroke-width="1.5"/>
                <path d="M10 6V14M6 10H14" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
            </svg>''',

            "menu": '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <circle cx="10" cy="5" r="1.5" fill="{color}"/>
                <circle cx="10" cy="10" r="1.5" fill="{color}"/>
                <circle cx="10" cy="15" r="1.5" fill="{color}"/>
            </svg>''',

            "search": '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <circle cx="9" cy="9" r="5" stroke="{color}" stroke-width="1.5"/>
                <path d="M13 13L17 17" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
            </svg>''',

            "lock": '''<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <rect x="3" y="7" width="10" height="7" rx="1" stroke="{color}" stroke-width="1.2"/>
                <path d="M5 7V4C5 2.5 6 1 8 1C10 1 11 2.5 11 4V7" stroke="{color}" stroke-width="1.2" stroke-linecap="round"/>
                <circle cx="8" cy="10" r="1" fill="{color}"/>
            </svg>''',

            "incognito": '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <circle cx="10" cy="7" r="3" stroke="{color}" stroke-width="1.5"/>
                <path d="M3 14C3 12.5 5.5 11 10 11C14.5 11 17 12.5 17 14" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M2 7H5M15 7H18" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
                <circle cx="6" cy="15" r="2" stroke="{color}" stroke-width="1.5"/>
                <circle cx="14" cy="15" r="2" stroke="{color}" stroke-width="1.5"/>
            </svg>''',

            "theme": '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <circle cx="10" cy="10" r="7" stroke="{color}" stroke-width="1.5"/>
                <path d="M10 3V6M10 14V17M3 10H6M14 10H17" stroke="{color}" stroke-width="1.2" stroke-linecap="round"/>
                <circle cx="10" cy="10" r="2" fill="{color}"/>
            </svg>''',

            "history": '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <circle cx="10" cy="10" r="7" stroke="{color}" stroke-width="1.5"/>
                <path d="M10 6V10L13 13" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
                <circle cx="5" cy="5" r="1" fill="{color}"/>
            </svg>''',

            "clear": '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M4 4L16 16M16 4L4 16" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>
                <circle cx="10" cy="10" r="7" stroke="{color}" stroke-width="1.5"/>
            </svg>''',

            "zoom_in": '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <circle cx="9" cy="9" r="5" stroke="{color}" stroke-width="1.5"/>
                <path d="M13 13L17 17" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M7 9H11M9 7V11" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
            </svg>''',

            "zoom_out": '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <circle cx="9" cy="9" r="5" stroke="{color}" stroke-width="1.5"/>
                <path d="M13 13L17 17" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M7 9H11" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
            </svg>''',

            "fullscreen": '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M3 8V5H8M17 8V5H12M3 12V15H8M17 12V15H12" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
            </svg>''',

            "window": '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <rect x="3" y="3" width="14" height="14" rx="2" stroke="{color}" stroke-width="1.5"/>
                <path d="M3 7H17" stroke="{color}" stroke-width="1.2"/>
            </svg>''',

            "download": '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M10 3V13M10 13L13 10M10 13L7 10" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M3 15H17V17H3V15Z" fill="{color}" stroke="{color}" stroke-width="1.2"/>
                <rect x="4" y="15" width="12" height="2" fill="{color}"/>
            </svg>''',

            "settings": '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <circle cx="10" cy="10" r="3" stroke="{color}" stroke-width="1.5"/>
                <path d="M17 10C17 8.9 17.9 8 19 8V6C17.9 6 17 5.1 17 4V3C17 1.9 16.1 1 15 1H5C3.9 1 3 1.9 3 3V4C3 5.1 2.1 6 1 6V8C2.1 8 3 8.9 3 10C3 11.1 2.1 12 1 12V14C2.1 14 3 14.9 3 16V17C3 18.1 3.9 19 5 19H15C16.1 19 17 18.1 17 17V16C17 14.9 17.9 14 19 14V12C17.9 12 17 11.1 17 10Z" stroke="{color}" stroke-width="1.2"/>
            </svg>''',
        }

        return icons.get(icon_name, "").format(color=color)

    def create_icon(self, svg_content, size=20):
        """Создание QIcon из SVG"""
        renderer = QSvgRenderer(QByteArray(svg_content.encode()))
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        renderer.render(painter)
        painter.end()

        return QIcon(pixmap)

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(6)

        is_incognito = self.browser_window.incognito
        icon_color = "#ffffff" if is_incognito else "#5f6368"
        hover_color = "#1a73e8"

        # Основной стиль для панели
        if is_incognito:
            self.setStyleSheet("""
                NavigationBar {
                    background-color: #202124;
                    border-bottom: 1px solid #3c4043;
                }

                NavigationBar QPushButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 8px;
                    min-width: 36px;
                    max-width: 36px;
                    min-height: 36px;
                    max-height: 36px;
                    margin: 0px 2px;
                }

                NavigationBar QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                }

                NavigationBar QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 0.15);
                }

                NavigationBar QPushButton:disabled {
                    opacity: 0.3;
                }

                NavigationBar QLineEdit {
                    border: 1px solid #3c4043;
                    border-radius: 22px;
                    padding: 8px 16px 8px 36px;
                    font-size: 14px;
                    min-height: 22px;
                    background-color: #303134;
                    color: #e8eaed;
                    selection-background-color: #1a73e8;
                }

                NavigationBar QLineEdit:hover {
                    background-color: #3c4043;
                    border-color: #5f6368;
                }

                NavigationBar QLineEdit:focus {
                    border-color: #1a73e8;
                    background-color: #303134;
                }

                NavigationBar QLineEdit::placeholder {
                    color: #9aa0a6;
                    font-style: normal;
                }

                NavigationBar QMenu {
                    background-color: #303134;
                    border: 1px solid #3c4043;
                    border-radius: 8px;
                    padding: 6px;
                    font-size: 13px;
                    color: #e8eaed;
                }

                NavigationBar QMenu::item {
                    padding: 8px 32px 8px 40px;
                    border-radius: 5px;
                }

                NavigationBar QMenu::item:selected {
                    background-color: #1a73e8;
                    color: #ffffff;
                }

                NavigationBar QMenu::item:disabled {
                    color: #9aa0a6;
                }

                NavigationBar QMenu::separator {
                    height: 1px;
                    background-color: #3c4043;
                    margin: 6px 10px;
                }

                NavigationBar QToolTip {
                    background-color: #202124;
                    color: #e8eaed;
                    border: 1px solid #3c4043;
                    border-radius: 5px;
                    padding: 6px 12px;
                    font-size: 11px;
                }
            """)
        else:
            self.setStyleSheet("""
                NavigationBar {
                    background-color: #f8f9fa;
                    border-bottom: 1px solid #dadce0;
                }

                NavigationBar QPushButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 8px;
                    min-width: 36px;
                    max-width: 36px;
                    min-height: 36px;
                    max-height: 36px;
                    margin: 0px 2px;
                }

                NavigationBar QPushButton:hover {
                    background-color: rgba(60, 64, 67, 0.08);
                }

                NavigationBar QPushButton:pressed {
                    background-color: rgba(60, 64, 67, 0.12);
                }

                NavigationBar QPushButton:disabled {
                    opacity: 0.3;
                }

                NavigationBar QLineEdit {
                    border: 1px solid #dadce0;
                    border-radius: 22px;
                    padding: 8px 16px 8px 36px;
                    font-size: 14px;
                    min-height: 22px;
                    background-color: #ffffff;
                    color: #3c4043;
                    selection-background-color: #1a73e8;
                    selection-color: #ffffff;
                }

                NavigationBar QLineEdit:hover {
                    background-color: #ffffff;
                    border-color: #bdc1c6;
                }

                NavigationBar QLineEdit:focus {
                    border-color: #1a73e8;
                    background-color: #ffffff;
                }

                NavigationBar QLineEdit::placeholder {
                    color: #80868b;
                    font-style: normal;
                }

                NavigationBar QMenu {
                    background-color: #ffffff;
                    border: 1px solid #dadce0;
                    border-radius: 8px;
                    padding: 6px;
                    font-size: 13px;
                    color: #3c4043;
                }

                NavigationBar QMenu::item {
                    padding: 8px 32px 8px 40px;
                    border-radius: 5px;
                }

                NavigationBar QMenu::item:selected {
                    background-color: #1a73e8;
                    color: #ffffff;
                }

                NavigationBar QMenu::item:disabled {
                    color: #80868b;
                }

                NavigationBar QMenu::separator {
                    height: 1px;
                    background-color: #dadce0;
                    margin: 6px 10px;
                }

                NavigationBar QToolTip {
                    background-color: #3c4043;
                    color: #ffffff;
                    border: none;
                    border-radius: 5px;
                    padding: 6px 12px;
                    font-size: 11px;
                }
            """)

        # Кнопки навигации с SVG иконками
        self.back_btn = NavigationButton(self.get_svg_icon("back", icon_color),
                                          self.get_svg_icon("back", hover_color))
        self.back_btn.setToolTip("Назад (Alt+←)")
        self.back_btn.clicked.connect(lambda: self.browser_window.current_browser().back())
        layout.addWidget(self.back_btn)

        self.forward_btn = NavigationButton(self.get_svg_icon("forward", icon_color),
                                             self.get_svg_icon("forward", hover_color))
        self.forward_btn.setToolTip("Вперед (Alt+→)")
        self.forward_btn.clicked.connect(lambda: self.browser_window.current_browser().forward())
        layout.addWidget(self.forward_btn)

        self.reload_btn = NavigationButton(self.get_svg_icon("reload", icon_color),
                                            self.get_svg_icon("reload", hover_color))
        self.reload_btn.setToolTip("Обновить (Ctrl+R)")
        self.reload_btn.clicked.connect(lambda: self.browser_window.current_browser().reload())
        layout.addWidget(self.reload_btn)

        self.home_btn = NavigationButton(self.get_svg_icon("home", icon_color),
                                          self.get_svg_icon("home", hover_color))
        self.home_btn.setToolTip("Домой")
        self.home_btn.clicked.connect(lambda: self.browser_window.open_url("https://www.google.com"))
        layout.addWidget(self.home_btn)

        # Адресная строка с иконкой
        url_container = QWidget()
        url_layout = QHBoxLayout(url_container)
        url_layout.setContentsMargins(0, 0, 0, 0)
        url_layout.setSpacing(0)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Введите адрес или поисковый запрос... (Ctrl+L для фокуса)")
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # Индикатор безопасности (замок)
        self.security_icon = QPushButton()
        self.security_icon.setFixedSize(32, 36)
        self.security_icon.setIcon(self.create_icon(self.get_svg_icon("lock", "#9aa0a6"), 16))
        self.security_icon.setCursor(Qt.ArrowCursor)
        self.security_icon.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                min-width: 32px;
                max-width: 32px;
            }
            QPushButton:hover {
                background-color: transparent;
            }
        """)

        url_layout.addWidget(self.security_icon)
        url_layout.addWidget(self.url_bar, 1)

        layout.addWidget(url_container, 1)

        # Кнопки действий
        self.bookmark_btn = NavigationButton(self.get_svg_icon("bookmark", icon_color),
                                              self.get_svg_icon("bookmark_filled", "#fbbc04"))
        self.bookmark_btn.setToolTip("Добавить в закладки (Ctrl+D)")
        self.bookmark_btn.clicked.connect(self.browser_window.add_bookmark)
        layout.addWidget(self.bookmark_btn)

        self.new_tab_btn = NavigationButton(self.get_svg_icon("new_tab", icon_color),
                                             self.get_svg_icon("new_tab", hover_color))
        self.new_tab_btn.setToolTip("Новая вкладка (Ctrl+T)")
        self.new_tab_btn.clicked.connect(self.browser_window.add_new_tab)
        layout.addWidget(self.new_tab_btn)

        self.menu_btn = NavigationButton(self.get_svg_icon("menu", icon_color),
                                          self.get_svg_icon("menu", hover_color))
        self.menu_btn.setToolTip("Меню")
        self.menu_btn.clicked.connect(self.show_menu)
        layout.addWidget(self.menu_btn)

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser_window.open_url(url)

    def update_url(self, url):
        url_str = url.toString()
        self.url_bar.setText(url_str)
        self.url_bar.setCursorPosition(0)

        # Обновляем иконку безопасности
        if url_str.startswith("https://"):
            self.security_icon.setIcon(self.create_icon(self.get_svg_icon("lock", "#34a853"), 16))
        else:
            self.security_icon.setIcon(self.create_icon(self.get_svg_icon("lock", "#9aa0a6"), 16))

    def show_menu(self):
        menu = QMenu(self)
        icon_color = "#5f6368"

        # Новое окно
        new_window_action = menu.addAction(self.create_icon(self.get_svg_icon("window", icon_color), 16), " Новое окно\tCtrl+N")
        new_window_action.triggered.connect(self.open_new_window)

        # Новое окно инкогнито
        incognito_action = menu.addAction(self.create_icon(self.get_svg_icon("incognito", icon_color), 16), " Новое окно инкогнито\tCtrl+Shift+N")
        incognito_action.triggered.connect(self.open_incognito_window)

        menu.addSeparator()

        # Загрузки
        downloads_action = menu.addAction(self.create_icon(self.get_svg_icon("download", icon_color), 16), " Загрузки\tCtrl+J")
        downloads_action.triggered.connect(self.browser_window.show_downloads)
        
        # Настройки
        settings_action = menu.addAction(self.create_icon(self.get_svg_icon("settings", icon_color), 16), " Настройки\tCtrl+,")
        settings_action.triggered.connect(self.browser_window.show_settings)

        menu.addSeparator()

        # Подменю тем
        theme_menu = menu.addMenu(self.create_icon(self.get_svg_icon("theme", icon_color), 16), " Тема оформления")
        for theme_name in self.browser_window.theme_switcher.get_theme_names():
            theme_info = self.browser_window.theme_switcher.THEMES[theme_name]
            action = theme_menu.addAction(f" {theme_info['name']}")
            action.triggered.connect(lambda checked, t=theme_name: self.browser_window.change_theme(t))

        menu.addSeparator()

        # Закладки
        bookmarks_action = menu.addAction(self.create_icon(self.get_svg_icon("bookmark", icon_color), 16), " Все закладки\tCtrl+Shift+B")
        bookmarks_action.triggered.connect(self.browser_window.show_all_bookmarks)

        # История
        history_action = menu.addAction(self.create_icon(self.get_svg_icon("history", icon_color), 16), " История\tCtrl+H")
        history_action.triggered.connect(self.browser_window.show_history)

        clear_history_action = menu.addAction(self.create_icon(self.get_svg_icon("clear", icon_color), 16), " Очистить историю\tCtrl+Shift+Del")
        clear_history_action.triggered.connect(self.browser_window.clear_history)

        menu.addSeparator()

        # Масштабирование
        zoom_in_action = menu.addAction(self.create_icon(self.get_svg_icon("zoom_in", icon_color), 16), " Увеличить\tCtrl+=")
        zoom_in_action.triggered.connect(self.browser_window.zoom_in)

        zoom_out_action = menu.addAction(self.create_icon(self.get_svg_icon("zoom_out", icon_color), 16), " Уменьшить\tCtrl+-")
        zoom_out_action.triggered.connect(self.browser_window.zoom_out)

        menu.addSeparator()

        # Полноэкранный режим
        fullscreen_action = menu.addAction(self.create_icon(self.get_svg_icon("fullscreen", icon_color), 16), " Полноэкранный режим\tF11")
        fullscreen_action.triggered.connect(self.browser_window.toggle_fullscreen)

        # Показываем меню под кнопкой
        menu.exec_(self.menu_btn.mapToGlobal(QPoint(0, self.menu_btn.height())))

    def open_new_window(self):
        """Открывает новое окно браузера"""
        from browser_window import AdvancedBrowser
        self.new_window = AdvancedBrowser(incognito=False)
        self.new_window.show()

    def open_incognito_window(self):
        """Открывает новое окно в режиме инкогнито"""
        from browser_window import AdvancedBrowser
        self.incognito_window = AdvancedBrowser(incognito=True)
        self.incognito_window.show()


class NavigationButton(QPushButton):
    """Кнопка навигации с поддержкой hover эффектов"""

    def __init__(self, normal_svg, hover_svg, parent=None):
        super().__init__(parent)
        self.normal_svg = normal_svg
        self.hover_svg = hover_svg
        self.is_hovered = False

        self.setCursor(Qt.PointingHandCursor)
        self.setIconSize(QSize(20, 20))
        self.update_icon()

    def create_icon_from_svg(self, svg_content):
        renderer = QSvgRenderer(QByteArray(svg_content.encode()))
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        renderer.render(painter)
        painter.end()

        return QIcon(pixmap)

    def update_icon(self):
        svg = self.hover_svg if self.is_hovered else self.normal_svg
        self.setIcon(self.create_icon_from_svg(svg))

    def enterEvent(self, event):
        self.is_hovered = True
        self.update_icon()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_hovered = False
        self.update_icon()
        super().leaveEvent(event)