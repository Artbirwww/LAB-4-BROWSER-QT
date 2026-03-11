from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtSvg import QSvgWidget

class BookmarksBar(QWidget):
    def __init__(self, browser_window):
        super().__init__()
        self.browser_window = browser_window
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(8)

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
        
        # Создаем иконки через QSvgWidget
        self.bookmarks_icon = QSvgWidget()
        self.bookmarks_icon.setFixedSize(16, 16)
        self.bookmarks_icon.load(self.get_bookmark_icon_svg())
        
        # Контейнер для лейбла с иконкой
        label_container = QWidget()
        label_layout = QHBoxLayout(label_container)
        label_layout.setContentsMargins(0, 0, 0, 0)
        label_layout.setSpacing(4)
        label_layout.addWidget(self.bookmarks_icon)
        
        self.bookmarks_label = QLabel("ЗАКЛАДКИ")
        label_layout.addWidget(self.bookmarks_label)
        label_layout.addStretch()
        
        layout.addWidget(label_container)
        
        self.bookmarks_container = QWidget()
        self.bookmarks_buttons_layout = QHBoxLayout(self.bookmarks_container)
        self.bookmarks_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.bookmarks_buttons_layout.setSpacing(2)
        layout.addWidget(self.bookmarks_container)
        
        layout.addStretch()
        
        # Кнопка "Все закладки" с SVG иконкой
        self.show_all_btn = QPushButton(" Все закладки")
        self.show_all_btn.setObjectName("showAllBtn")
        self.show_all_btn.setIcon(QIcon(self.pixmap_from_svg(self.get_folder_icon_svg(), 14, 14)))
        self.show_all_btn.setIconSize(self.show_all_btn.iconSize().scaled(14, 14, Qt.KeepAspectRatio))
        self.show_all_btn.clicked.connect(self.browser_window.show_all_bookmarks)
        layout.addWidget(self.show_all_btn)
        
    def get_bookmark_icon_svg(self):
        return """<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 2.5C3 2.22386 3.22386 2 3.5 2H12.5C12.7761 2 13 2.22386 13 2.5V13.5C13 13.6899 12.8599 13.8625 12.6798 13.9237C12.4997 13.9849 12.3027 13.9264 12.18 13.78L8 9.05L3.82 13.78C3.69726 13.9264 3.50032 13.9849 3.32022 13.9237C3.14012 13.8625 3 13.6899 3 13.5V2.5Z" 
            fill="#5c5c5e" stroke="#5c5c5e" stroke-width="0.5"/>
        </svg>"""
    
    def get_folder_icon_svg(self):
        return """<svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M1.5 3.5C1.5 2.94772 1.94772 2.5 2.5 2.5H5.5C5.77614 2.5 6 2.72386 6 3V3.5H11.5C12.0523 3.5 12.5 3.94772 12.5 4.5V10.5C12.5 11.0523 12.0523 11.5 11.5 11.5H2.5C1.94772 11.5 1.5 11.0523 1.5 10.5V3.5Z" 
            fill="#0066cc" stroke="#0066cc" stroke-width="0.5"/>
            <path d="M6 3.5H1.5V4.5H6V3.5Z" fill="#0066cc" fill-opacity="0.3"/>
        </svg>"""
    
    def pixmap_from_svg(self, svg_content, width, height):
        """Создает QPixmap из SVG строки"""
        from PyQt5.QtCore import QByteArray, QBuffer
        from PyQt5.QtSvg import QSvgRenderer
        from PyQt5.QtGui import QPainter
        
        renderer = QSvgRenderer(QByteArray(svg_content.encode()))
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        return pixmap
    
    def load_bookmarks(self, bookmarks):
        for i in reversed(range(self.bookmarks_buttons_layout.count())):
            widget = self.bookmarks_buttons_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        for title, url in bookmarks:
            short_title = title[:15] + "…" if len(title) > 15 else title
            
            btn = QPushButton(f" {short_title}")
            
            # Создаем SVG иконку для каждой закладки
            bookmark_svg = """<svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M2.5 2C2.22386 2 2 2.22386 2 2.5V9.5C2 9.6899 2.14012 9.8625 2.32022 9.9237C2.50032 9.9849 2.69726 9.9264 2.82 9.78L6 6.05L9.18 9.78C9.30274 9.9264 9.49968 9.9849 9.67978 9.9237C9.85988 9.8625 10 9.6899 10 9.5V2.5C10 2.22386 9.77614 2 9.5 2H2.5Z" 
                fill="#5c5c5e"/>
            </svg>"""
            
            btn.setIcon(QIcon(self.pixmap_from_svg(bookmark_svg, 12, 12)))
            btn.setIconSize(btn.iconSize().scaled(12, 12, Qt.KeepAspectRatio))
            btn.setToolTip(f"{title}\n{url}")
            btn.setFixedHeight(28)
            btn.clicked.connect(lambda checked, u=url: self.browser_window.open_url(u))
            self.bookmarks_buttons_layout.addWidget(btn)
        
        if not bookmarks:
            empty_label = QLabel("Нет закладок")
            empty_label.setStyleSheet("color: #8e8e93; padding: 6px 10px; font-style: italic;")
            self.bookmarks_buttons_layout.addWidget(empty_label)