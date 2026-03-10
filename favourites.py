from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton

class BookmarksBar(QWidget):
    def __init__(self, browser_window):
        super().__init__()
        self.browser_window = browser_window
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)

        self.setStyleSheet("""
    /* Основная панель закладок - как в Safari */
    BookmarksBar {
        border-top: 1px solid #d9d9d9;
        border-bottom: 1px solid #d9d9d9;
    }
    
    QLabel {
        color: #8e8e93;
        font-size: 13px;
        font-weight: 400;
        padding: 4px 8px;
        background-color: transparent;
    }
    
    QPushButton {
        background-color: transparent;
        color: #1d1d1f;
        border: none;
        border-radius: 5px;
        padding: 4px 12px;
        font-size: 13px;
        font-weight: 400;
        text-align: center;
        min-width: 40px;
        max-width: 200px;
    }
    
    QPushButton:hover {
        background-color: rgba(0, 0, 0, 0.05);
        color: #1d1d1f;
    }
    
    QPushButton:pressed {
        background-color: rgba(0, 0, 0, 0.1);
    }
    
    QPushButton#showAllBtn {
        background-color: transparent;
        color: #0066cc;
        border: 0.5px solid #b3b3b3;
        border-radius: 4px;
        padding: 4px 14px;
        font-size: 12px;
        font-weight: 400;
        min-width: 90px;
    }
    
    QPushButton#showAllBtn:hover {
        background-color: rgba(0, 102, 204, 0.05);
        border-color: #0066cc;
    }
    
    QPushButton#showAllBtn:pressed {
        background-color: rgba(0, 102, 204, 0.1);
    }
    
    QToolTip {
        background-color: #f5f5f7;
        color: #1d1d1f;
        border: 0.5px solid #b3b3b3;
        border-radius: 4px;
        padding: 8px 12px;
        font-size: 11px;
    }
""")
        
        self.bookmarks_label = QLabel("Закладки:")
        layout.addWidget(self.bookmarks_label)
        
        self.bookmarks_container = QWidget()
        self.bookmarks_buttons_layout = QHBoxLayout(self.bookmarks_container)
        self.bookmarks_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.bookmarks_buttons_layout.setSpacing(2)
        layout.addWidget(self.bookmarks_container)
        
        layout.addStretch()
        
        self.show_all_btn = QPushButton("Все закладки")
        self.show_all_btn.clicked.connect(self.browser_window.show_all_bookmarks)
        layout.addWidget(self.show_all_btn)
        
    def load_bookmarks(self, bookmarks):
        for i in reversed(range(self.bookmarks_buttons_layout.count())):
            widget = self.bookmarks_buttons_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        for title, url in bookmarks:
            short_title = title[:15] + "..." if len(title) > 15 else title
            
            btn = QPushButton(short_title)
            btn.setToolTip(f"{title}\n{url}")
            btn.setFixedHeight(25)
            btn.clicked.connect(lambda checked, u=url: self.browser_window.open_url(u))
            self.bookmarks_buttons_layout.addWidget(btn)