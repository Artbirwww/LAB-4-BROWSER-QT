from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer

class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(44)
        self.dragging = False
        self.drag_position = None
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(8)
        
        # Устанавливаем стиль для всего заголовка
        self.setStyleSheet("""
    TitleBar {
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                   stop: 0 #f5f5f7, stop: 1 #ffffff);
        border-bottom: 1px solid #d9d9d9;
    }
    
    QLabel {
        color: #1d1d1f;
        font-size: 14px;
        font-weight: 500;
        padding: 0px 8px;
        background: transparent;
        letter-spacing: 0.3px;
    }
    
    QPushButton {
        background-color: transparent;
        border: none;
        border-radius: 6px;
        min-width: 32px;
        max-width: 32px;
        min-height: 32px;
        max-height: 32px;
        margin: 0px 2px;
    }
    
    QPushButton:hover {
        background-color: rgba(0, 0, 0, 0.06);
    }
    
    QPushButton:pressed {
        background-color: rgba(0, 0, 0, 0.1);
    }
    
    QPushButton#minimizeBtn:hover {
        background-color: rgba(0, 0, 0, 0.08);
    }
    
    QPushButton#maximizeBtn:hover {
        background-color: rgba(0, 0, 0, 0.08);
    }
    
    QPushButton#closeBtn {
        margin-left: 4px;
    }
    
    QPushButton#closeBtn:hover {
        background-color: #ff4444;
    }
    
    QPushButton#closeBtn:pressed {
        background-color: #cc0000;
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
        minimize_icon = self.create_icon_from_svg(self.get_minimize_svg(), 16, 16)
        maximize_icon = self.create_icon_from_svg(self.get_maximize_svg(), 16, 16)
        close_icon = self.create_icon_from_svg(self.get_close_svg(), 16, 16)
        
        # Заголовок окна
        self.title_label = QLabel("POVTIAS CO. INC. BROWSER")
        self.title_label.setStyleSheet("""
            QLabel {
                font-weight: 600;
                color: #1d1d1f;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.title_label)
        
        # Растягивающийся пробел
        layout.addStretch()
        
        # Кнопки управления окном
        self.minimize_btn = QPushButton()
        self.minimize_btn.setObjectName("minimizeBtn")
        self.minimize_btn.setIcon(minimize_icon)
        self.minimize_btn.setIconSize(self.minimize_btn.iconSize().scaled(16, 16, Qt.KeepAspectRatio))
        self.minimize_btn.clicked.connect(self.parent.showMinimized)
        self.minimize_btn.setToolTip("Свернуть")
        layout.addWidget(self.minimize_btn)
        
        self.maximize_btn = QPushButton()
        self.maximize_btn.setObjectName("maximizeBtn")
        self.maximize_btn.setIcon(maximize_icon)
        self.maximize_btn.setIconSize(self.maximize_btn.iconSize().scaled(16, 16, Qt.KeepAspectRatio))
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        self.maximize_btn.setToolTip("Развернуть")
        layout.addWidget(self.maximize_btn)
        
        self.close_btn = QPushButton()
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setIcon(close_icon)
        self.close_btn.setIconSize(self.close_btn.iconSize().scaled(16, 16, Qt.KeepAspectRatio))
        self.close_btn.clicked.connect(self.parent.close)
        self.close_btn.setToolTip("Закрыть")
        layout.addWidget(self.close_btn)
        
        # Включаем перетаскивание окна
        self.mousePressEvent = self.mouse_press_event
        self.mouseMoveEvent = self.mouse_move_event
        self.mouseReleaseEvent = self.mouse_release_event
        
    def get_minimize_svg(self):
        return """<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 8H13" stroke="#666666" stroke-width="1.5" stroke-linecap="round"/>
        </svg>"""
    
    def get_maximize_svg(self):
        return """<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="3" width="10" height="10" rx="1.5" stroke="#666666" stroke-width="1.2"/>
        </svg>"""
    
    def get_close_svg(self):
        return """<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M4 4L12 12M12 4L4 12" stroke="#666666" stroke-width="1.5" stroke-linecap="round"/>
        </svg>"""
    
    def get_restore_svg(self):
        return """<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="5" y="5" width="8" height="8" rx="1.2" stroke="#666666" stroke-width="1.2"/>
            <rect x="3" y="3" width="8" height="8" rx="1.2" stroke="#666666" stroke-width="1.2" fill="white"/>
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
    
    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            restore_icon = self.create_icon_from_svg(self.get_maximize_svg(), 16, 16)
            self.maximize_btn.setIcon(restore_icon)
            self.maximize_btn.setToolTip("Развернуть")
        else:
            self.parent.showMaximized()
            restore_icon = self.create_icon_from_svg(self.get_restore_svg(), 16, 16)
            self.maximize_btn.setIcon(restore_icon)
            self.maximize_btn.setToolTip("Восстановить")
            
    def update_title(self, title):
        self.title_label.setText(f"POVTIAS CO. INC. BROWSER")
        
    def mouse_press_event(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.parent.frameGeometry().topLeft()
            event.accept()
            
    def mouse_move_event(self, event):
        if self.dragging and not self.parent.isMaximized():
            self.parent.move(event.globalPos() - self.drag_position)
            event.accept()
            
    def mouse_release_event(self, event):
        self.dragging = False
        event.accept()