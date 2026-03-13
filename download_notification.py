from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor, QBrush, QPen
import os

class DownloadNotification(QWidget):
    """Всплывающее уведомление о завершении загрузки"""
    
    def __init__(self, parent=None, file_name="", file_path="", theme="light"):
        super().__init__(parent)
        self.file_name = file_name
        self.file_path = file_path
        self.theme = theme
        self.timeout = 5000  # 5 секунд
        
        # Настройки окна
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(350, 100)
        
        self.setup_ui()
        
        # Таймер для автоматического закрытия
        self.timer = QTimer()
        self.timer.timeout.connect(self.fade_out)
        self.timer.start(self.timeout)
        
    def setup_ui(self):
        """Настройка интерфейса уведомления"""
        # Основной контейнер с тенью
        container = QFrame(self)
        container.setGeometry(5, 5, 340, 90)
        
        if self.theme == "dark":
            container.setStyleSheet("""
                QFrame {
                    background-color: #2d2d2d;
                    border: 1px solid #555555;
                    border-radius: 10px;
                }
            """)
        else:
            container.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 10px;
                }
            """)
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Иконка успеха
        icon_label = QLabel("✅")
        icon_label.setStyleSheet("font-size: 32px;")
        layout.addWidget(icon_label)
        
        # Текст уведомления
        text_layout = QVBoxLayout()
        text_layout.setSpacing(3)
        
        title_label = QLabel("Загрузка завершена!")
        if self.theme == "dark":
            title_label.setStyleSheet("color: white; font-weight: bold; font-size: 13px;")
        else:
            title_label.setStyleSheet("color: #1d1d1f; font-weight: bold; font-size: 13px;")
        text_layout.addWidget(title_label)
        
        file_label = QLabel(self.file_name)
        if self.theme == "dark":
            file_label.setStyleSheet("color: #cccccc; font-size: 11px;")
        else:
            file_label.setStyleSheet("color: #666666; font-size: 11px;")
        file_label.setWordWrap(True)
        file_label.setMaximumWidth(180)
        text_layout.addWidget(file_label)
        
        layout.addLayout(text_layout)
        
        # Кнопка открытия
        open_btn = QPushButton("📁")
        open_btn.setFixedSize(32, 32)
        open_btn.setToolTip("Открыть файл")
        open_btn.clicked.connect(self.open_file)
        
        if self.theme == "dark":
            open_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3d3d3d;
                    border: 1px solid #555555;
                    border-radius: 16px;
                    font-size: 16px;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #4d4d4d;
                }
            """)
        else:
            open_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #d0d0d0;
                    border-radius: 16px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
        layout.addWidget(open_btn)
        
        # Кнопка закрытия
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(24, 24)
        close_btn.setToolTip("Закрыть")
        close_btn.clicked.connect(self.close)
        
        if self.theme == "dark":
            close_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #aaaaaa;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    color: white;
                }
            """)
        else:
            close_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #999999;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    color: #333333;
                }
            """)
        layout.addWidget(close_btn)
        
    def open_file(self):
        """Открывает загруженный файл"""
        if os.path.exists(self.file_path):
            os.startfile(self.file_path)
        self.close()
        
    def fade_out(self):
        """Анимация исчезновения"""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.finished.connect(self.close)
        self.animation.start()
        
    def enterEvent(self, event):
        """При наведении мыши отменяем автоматическое закрытие"""
        self.timer.stop()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        """При уходе мыши возобновляем таймер"""
        self.timer.start(self.timeout)
        super().leaveEvent(event)