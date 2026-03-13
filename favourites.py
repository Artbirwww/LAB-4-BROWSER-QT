from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class BookmarksBar(QWidget):
    def __init__(self, browser_window):
        super().__init__()
        self.browser_window = browser_window
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(8)

        # Динамический стиль в зависимости от режима
        if hasattr(self.browser_window, 'incognito') and self.browser_window.incognito:
            # Стиль для инкогнито (тёмный)
            self.setStyleSheet("""
        BookmarksBar {
            background-color: #2d2d2d;
            border-top: 1px solid #555555;
            border-bottom: 1px solid #555555;
        }

        QLabel {
            color: #aaaaaa;
            font-size: 13px;
            font-weight: 500;
            padding: 6px 12px 6px 8px;
            background: transparent;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        QPushButton {
            background: transparent;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            padding: 6px 14px 6px 10px;
            font-size: 13px;
            font-weight: 400;
            text-align: left;
            min-width: 40px;
            max-width: 200px;
        }

        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.1);
            color: #ffffff;
        }

        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 0.15);
        }

        QPushButton:focus {
            outline: 2px solid rgba(255, 255, 255, 0.3);
            outline-offset: -2px;
        }

        QPushButton#showAllBtn {
            background: transparent;
            color: #66aaff;
            border: 1px solid #555555;
            border-radius: 16px;
            padding: 6px 18px 6px 14px;
            font-size: 12px;
            font-weight: 500;
            min-width: 100px;
            text-align: center;
        }

        QPushButton#showAllBtn:hover {
            background-color: rgba(102, 170, 255, 0.1);
            border-color: #66aaff;
        }

        QPushButton#showAllBtn:pressed {
            background-color: rgba(102, 170, 255, 0.2);
        }

        QToolTip {
            background-color: #2c2c2e;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 11px;
        }
        """)
        else:
            # Обычный стиль
            self.setStyleSheet("""
        BookmarksBar {
            background-color: #fafafc;
            border-top: 1px solid #e5e5e7;
            border-bottom: 1px solid #e5e5e7;
        }

        QLabel {
            color: #5c5c5e;
            font-size: 13px;
            font-weight: 500;
            padding: 6px 12px 6px 8px;
            background: transparent;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        QPushButton {
            background: transparent;
            color: #2c2c2e;
            border: none;
            border-radius: 6px;
            padding: 6px 14px 6px 10px;
            font-size: 13px;
            font-weight: 400;
            text-align: left;
            min-width: 40px;
            max-width: 200px;
        }

        QPushButton:hover {
            background-color: rgba(0, 0, 0, 0.04);
            color: #000000;
        }

        QPushButton:pressed {
            background-color: rgba(0, 0, 0, 0.08);
        }

        QPushButton:focus {
            outline: 2px solid rgba(0, 122, 255, 0.3);
            outline-offset: -2px;
        }

        QPushButton#showAllBtn {
            background: transparent;
            color: #0066cc;
            border: 1px solid #d9d9de;
            border-radius: 16px;
            padding: 6px 18px 6px 14px;
            font-size: 12px;
            font-weight: 500;
            min-width: 100px;
            text-align: center;
        }

        QPushButton#showAllBtn:hover {
            background-color: rgba(0, 102, 204, 0.04);
            border-color: #0066cc;
        }

        QPushButton#showAllBtn:pressed {
            background-color: rgba(0, 102, 204, 0.08);
        }

        QToolTip {
            background-color: #2c2c2e;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 11px;
        }
        """)

        # Используем QLabel с текстом вместо SVG для иконки закладок
        self.bookmarks_label = QLabel("📑 ЗАКЛАДКИ")
        layout.addWidget(self.bookmarks_label)

        self.bookmarks_container = QWidget()
        self.bookmarks_buttons_layout = QHBoxLayout(self.bookmarks_container)
        self.bookmarks_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.bookmarks_buttons_layout.setSpacing(2)
        layout.addWidget(self.bookmarks_container)

        layout.addStretch()

        # Кнопка "Все закладки" с текстовой иконкой
        self.show_all_btn = QPushButton("📁 Все закладки")
        self.show_all_btn.setObjectName("showAllBtn")
        
        # В инкогнито кнопка закладок отключена
        if hasattr(self.browser_window, 'incognito') and self.browser_window.incognito:
            self.show_all_btn.setEnabled(False)
            self.show_all_btn.setToolTip("В режиме инкогнито закладки недоступны")
        else:
            self.show_all_btn.clicked.connect(self.browser_window.show_all_bookmarks)
            
        layout.addWidget(self.show_all_btn)

    def load_bookmarks(self, bookmarks):
        # В инкогнито не показываем закладки
        if hasattr(self.browser_window, 'incognito') and self.browser_window.incognito:
            for i in reversed(range(self.bookmarks_buttons_layout.count())):
                widget = self.bookmarks_buttons_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            
            empty_label = QLabel("В инкогнито закладки недоступны")
            empty_label.setStyleSheet("color: #888888; padding: 6px 10px; font-style: italic;")
            self.bookmarks_buttons_layout.addWidget(empty_label)
            return

        for i in reversed(range(self.bookmarks_buttons_layout.count())):
            widget = self.bookmarks_buttons_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for title, url in bookmarks:
            short_title = title[:15] + "…" if len(title) > 15 else title
            btn = QPushButton(f"🔖 {short_title}")
            btn.setToolTip(f"{title}\n{url}")
            btn.setFixedHeight(28)
            btn.clicked.connect(lambda checked, u=url: self.browser_window.open_url(u))
            self.bookmarks_buttons_layout.addWidget(btn)

        if not bookmarks:
            empty_label = QLabel("Нет закладок")
            empty_label.setStyleSheet("color: #8e8e93; padding: 6px 10px; font-style: italic;")
            self.bookmarks_buttons_layout.addWidget(empty_label)