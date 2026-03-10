from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(40)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        
        # Заголовок окна
        self.title_label = QLabel("POVTIAS CO. INC. BROWSER")
        self.title_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.title_label)
        
        # Растягивающийся пробел
        layout.addStretch()
        
        # Кнопки управления окном
        self.minimize_btn = QPushButton("─")
        self.minimize_btn.setFixedSize(30, 30)
        self.minimize_btn.clicked.connect(self.parent.showMinimized)
        self.minimize_btn.setToolTip("Свернуть")
        layout.addWidget(self.minimize_btn)
        
        self.maximize_btn = QPushButton("□")
        self.maximize_btn.setFixedSize(30, 30)
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        self.maximize_btn.setToolTip("Развернуть")
        layout.addWidget(self.maximize_btn)
        
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.clicked.connect(self.parent.close)
        self.close_btn.setToolTip("Закрыть")
        self.close_btn.setStyleSheet("""
            QPushButton:hover {
                background-color: #ff4444;
                color: white;
            }
        """)
        layout.addWidget(self.close_btn)
        
    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.maximize_btn.setText("□")
        else:
            self.parent.showMaximized()
            self.maximize_btn.setText("❐")
            
    def update_title(self, title):
        self.title_label.setText(f"POVTIAS CO. INC. BROWSER - {title}")