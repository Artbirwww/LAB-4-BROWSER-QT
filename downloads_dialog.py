from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget, 
                             QPushButton, QLabel, QProgressBar, QFileDialog,
                             QMessageBox, QWidget, QListWidgetItem, QMenu)
from PyQt5.QtCore import Qt, QUrl, QTimer, QSize
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPainter
from PyQt5.QtWebEngineWidgets import QWebEngineDownloadItem
import os
import time
import shutil
from datetime import datetime, timedelta

class DownloadItem(QWidget):
    """Виджет для отображения одного скачиваемого файла"""
    
    def __init__(self, download_item, parent=None):
        super().__init__(parent)
        self.download_item = download_item
        self.start_time = time.time()
        self.last_bytes = 0
        self.speed = 0
        self.remaining_time = "—"
        
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Верхняя строка с именем файла и статусом
        top_layout = QHBoxLayout()
        
        # Иконка файла
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(24, 24)
        self.update_icon()
        top_layout.addWidget(self.icon_label)
        
        # Имя файла
        self.filename_label = QLabel(os.path.basename(self.download_item.path()))
        self.filename_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        self.filename_label.setWordWrap(True)
        top_layout.addWidget(self.filename_label, 1)
        
        # Статус/размер
        self.size_label = QLabel()
        self.size_label.setStyleSheet("color: #666; font-size: 12px;")
        top_layout.addWidget(self.size_label)
        
        layout.addLayout(top_layout)
        
        # Прогресс бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #e0e0e0;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background-color: #1a73e8;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Нижняя строка с информацией о скорости
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(15)
        
        self.speed_label = QLabel("Скорость: 0 КБ/с")
        self.speed_label.setStyleSheet("color: #666; font-size: 11px;")
        bottom_layout.addWidget(self.speed_label)
        
        self.time_label = QLabel("Осталось: —")
        self.time_label.setStyleSheet("color: #666; font-size: 11px;")
        bottom_layout.addWidget(self.time_label)
        
        bottom_layout.addStretch()
        
        # Кнопки управления
        self.pause_btn = QPushButton("⏸")
        self.pause_btn.setFixedSize(24, 24)
        self.pause_btn.setToolTip("Приостановить")
        self.pause_btn.clicked.connect(self.toggle_pause)
        bottom_layout.addWidget(self.pause_btn)
        
        self.cancel_btn = QPushButton("✕")
        self.cancel_btn.setFixedSize(24, 24)
        self.cancel_btn.setToolTip("Отменить")
        self.cancel_btn.clicked.connect(self.cancel_download)
        bottom_layout.addWidget(self.cancel_btn)
        
        self.open_folder_btn = QPushButton("📁")
        self.open_folder_btn.setFixedSize(24, 24)
        self.open_folder_btn.setToolTip("Открыть папку")
        self.open_folder_btn.clicked.connect(self.open_folder)
        self.open_folder_btn.hide()  # Показываем только после завершения
        bottom_layout.addWidget(self.open_folder_btn)
        
        layout.addLayout(bottom_layout)
        
        # Таймер для обновления скорости
        self.speed_timer = QTimer()
        self.speed_timer.timeout.connect(self.update_speed)
        self.speed_timer.start(1000)  # Обновляем каждую секунду
        
    def setup_connections(self):
        self.download_item.downloadProgress.connect(self.update_progress)
        self.download_item.stateChanged.connect(self.state_changed)
        
    def update_icon(self):
        """Обновляет иконку в зависимости от типа файла"""
        ext = os.path.splitext(self.download_item.path())[1].lower()
        
        # Простые эмодзи для разных типов файлов
        icon_map = {
            '.pdf': '📄', '.doc': '📝', '.docx': '📝',
            '.xls': '📊', '.xlsx': '📊',
            '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️',
            '.mp3': '🎵', '.wav': '🎵',
            '.mp4': '🎬', '.avi': '🎬', '.mkv': '🎬',
            '.zip': '📦', '.rar': '📦', '.7z': '📦',
            '.exe': '⚙️', '.msi': '⚙️',
        }
        
        icon_char = icon_map.get(ext, '📎')
        self.icon_label.setText(icon_char)
        self.icon_label.setStyleSheet("font-size: 20px;")
        
    def update_progress(self, bytes_received, bytes_total):
        """Обновляет прогресс загрузки"""
        if bytes_total > 0:
            progress = int((bytes_received / bytes_total) * 100)
            self.progress_bar.setValue(progress)
            
            # Обновляем размер
            received_mb = bytes_received / (1024 * 1024)
            total_mb = bytes_total / (1024 * 1024)
            self.size_label.setText(f"{received_mb:.1f} МБ / {total_mb:.1f} МБ")
        else:
            # Если неизвестен общий размер
            received_mb = bytes_received / (1024 * 1024)
            self.size_label.setText(f"{received_mb:.1f} МБ / ? МБ")
            
    def update_speed(self):
        """Обновляет скорость загрузки и оставшееся время"""
        if self.download_item.state() == QWebEngineDownloadItem.DownloadInProgress:
            bytes_received = self.download_item.receivedBytes()
            bytes_total = self.download_item.totalBytes()
            
            # Вычисляем скорость
            current_bytes = bytes_received
            if self.last_bytes > 0:
                speed_bps = current_bytes - self.last_bytes  # байт в секунду
                self.speed = speed_bps
                
                # Форматируем скорость
                if speed_bps < 1024:
                    speed_str = f"{speed_bps} Б/с"
                elif speed_bps < 1024 * 1024:
                    speed_str = f"{speed_bps / 1024:.1f} КБ/с"
                else:
                    speed_str = f"{speed_bps / (1024 * 1024):.1f} МБ/с"
                    
                self.speed_label.setText(f"Скорость: {speed_str}")
                
                # Вычисляем оставшееся время
                if bytes_total > 0 and speed_bps > 0:
                    remaining_bytes = bytes_total - bytes_received
                    remaining_seconds = remaining_bytes / speed_bps
                    
                    if remaining_seconds < 60:
                        self.remaining_time = f"{int(remaining_seconds)} сек"
                    elif remaining_seconds < 3600:
                        self.remaining_time = f"{int(remaining_seconds / 60)} мин"
                    else:
                        hours = int(remaining_seconds / 3600)
                        minutes = int((remaining_seconds % 3600) / 60)
                        self.remaining_time = f"{hours} ч {minutes} мин"
                        
                    self.time_label.setText(f"Осталось: {self.remaining_time}")
                    
            self.last_bytes = bytes_received
            
    def state_changed(self, state):
        """Обрабатывает изменение состояния загрузки"""
        if state == QWebEngineDownloadItem.DownloadCompleted:
            self.progress_bar.setValue(100)
            self.size_label.setText("Завершено")
            self.pause_btn.hide()
            self.cancel_btn.hide()
            self.open_folder_btn.show()
            self.speed_timer.stop()
            self.speed_label.setText("Загрузка завершена")
            self.time_label.hide()
        elif state == QWebEngineDownloadItem.DownloadCancelled:
            self.speed_label.setText("Отменено")
            self.pause_btn.hide()
            self.cancel_btn.hide()
            self.speed_timer.stop()
        elif state == QWebEngineDownloadItem.DownloadInterrupted:
            self.speed_label.setText(f"Ошибка: {self.download_item.interruptReasonString()}")
            self.speed_timer.stop()
            
    def toggle_pause(self):
        """Приостанавливает или возобновляет загрузку"""
        if self.download_item.state() == QWebEngineDownloadItem.DownloadInProgress:
            self.download_item.pause()
            self.pause_btn.setText("▶")
            self.pause_btn.setToolTip("Возобновить")
        else:
            self.download_item.resume()
            self.pause_btn.setText("⏸")
            self.pause_btn.setToolTip("Приостановить")
            
    def cancel_download(self):
        """Отменяет загрузку"""
        self.download_item.cancel()
        
    def open_folder(self):
        """Открывает папку с загруженным файлом"""
        path = self.download_item.path()
        if os.path.exists(path):
            os.startfile(os.path.dirname(path))


class DownloadsDialog(QDialog):
    """Диалог управления загрузками"""
    
    def __init__(self, browser_window, parent=None):
        super().__init__(parent or browser_window)
        self.browser_window = browser_window
        self.downloads = []  # Список активных загрузок
        self.completed_downloads = []  # Список завершенных загрузок
        
        self.setWindowTitle("Загрузки")
        self.setGeometry(200, 200, 700, 500)
        self.setMinimumSize(600, 400)
        
        # Применяем тему
        theme = browser_window.current_theme
        self.theme = theme
        if hasattr(browser_window, 'theme_switcher'):
            self.setStyleSheet(browser_window.theme_switcher.get_dialog_style(theme))
            
        self.setup_ui()
        self.load_downloads()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Заголовок
        title_layout = QHBoxLayout()
        
        title_label = QLabel("⬇️ Загрузки")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 5px;")
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        
        # Кнопка настроек папки загрузок
        self.folder_btn = QPushButton("📁 Папка загрузок")
        self.folder_btn.clicked.connect(self.change_download_folder)
        title_layout.addWidget(self.folder_btn)
        
        # Кнопка очистки завершенных
        self.clear_btn = QPushButton("🗑️ Очистить завершенные")
        self.clear_btn.clicked.connect(self.clear_completed)
        title_layout.addWidget(self.clear_btn)
        
        layout.addLayout(title_layout)
        
        # Текущая папка загрузок
        self.folder_label = QLabel()
        self.folder_label.setStyleSheet("color: #666; font-size: 12px; padding: 5px;")
        self.update_folder_label()
        layout.addWidget(self.folder_label)
        
        # Список загрузок
        self.downloads_list = QListWidget()
        self.downloads_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: transparent;
            }
            QListWidget::item {
                border-bottom: 1px solid #eee;
                padding: 0px;
            }
            QListWidget::item:selected {
                background-color: rgba(26, 115, 232, 0.1);
            }
        """)
        layout.addWidget(self.downloads_list)
        
        # Нижние кнопки
        button_box = QHBoxLayout()
        
        self.show_all_btn = QPushButton("Показать все")
        self.show_all_btn.clicked.connect(self.show_all_downloads)
        button_box.addWidget(self.show_all_btn)
        
        button_box.addStretch()
        
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.close)
        button_box.addWidget(close_btn)
        
        layout.addLayout(button_box)
        
    def update_folder_label(self):
        """Обновляет отображение текущей папки загрузок"""
        folder = self.browser_window.get_download_folder()
        self.folder_label.setText(f"📂 Текущая папка: {folder}")
        
    def change_download_folder(self):
        """Изменяет папку загрузок"""
        current_folder = self.browser_window.get_download_folder()
        
        folder = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку для загрузок",
            current_folder
        )
        
        if folder:
            self.browser_window.set_download_folder(folder)
            self.update_folder_label()
            
    def add_download(self, download_item):
        """Добавляет новую загрузку в список"""
        # Создаем элемент списка
        item = QListWidgetItem(self.downloads_list)
        item.setSizeHint(QSize(0, 120))  # Высота элемента
        
        # Создаем виджет для загрузки
        download_widget = DownloadItem(download_item)
        
        # Добавляем в список
        self.downloads_list.addItem(item)
        self.downloads_list.setItemWidget(item, download_widget)
        
        # Сохраняем ссылку
        self.downloads.append({
            'item': item,
            'widget': download_widget,
            'download': download_item
        })
        
        # Подключаем сигнал завершения
        download_item.stateChanged.connect(
            lambda state, d=download_item: self.download_finished(state, d)
        )
        
    def download_finished(self, state, download_item):
        """Обрабатывает завершение загрузки"""
        if state == QWebEngineDownloadItem.DownloadCompleted:
            # Перемещаем в список завершенных
            for d in self.downloads[:]:
                if d['download'] == download_item:
                    self.downloads.remove(d)
                    self.completed_downloads.append(d)
                    break
                    
    def clear_completed(self):
        """Очищает список завершенных загрузок"""
        for d in self.completed_downloads:
            row = self.downloads_list.row(d['item'])
            self.downloads_list.takeItem(row)
            
        self.completed_downloads.clear()
        
    def show_all_downloads(self):
        """Показывает все загрузки (активные и завершенные)"""
        # Просто обновляем список, все элементы уже видны
        pass
        
    def load_downloads(self):
        """Загружает список активных загрузок"""
        # Здесь можно загрузить сохраненные загрузки
        pass
        
    def closeEvent(self, event):
        """Сохраняет состояние перед закрытием"""
        # Здесь можно сохранить список загрузок
        event.accept()
    def state_changed(self, state):
        """Обрабатывает изменение состояния загрузки"""
        if state == QWebEngineDownloadItem.DownloadCompleted:
            self.progress_bar.setValue(100)
            self.size_label.setText("Завершено")
            self.pause_btn.hide()
            self.cancel_btn.hide()
            self.open_folder_btn.show()
            self.speed_timer.stop()
            self.speed_label.setText("✅ Загрузка завершена")
            self.time_label.hide()
            
            # Показываем уведомление о завершении
            self.show_completion_notification()
            
        elif state == QWebEngineDownloadItem.DownloadCancelled:
            self.speed_label.setText("❌ Отменено")
            self.pause_btn.hide()
            self.cancel_btn.hide()
            self.speed_timer.stop()
            
        elif state == QWebEngineDownloadItem.DownloadInterrupted:
            self.speed_label.setText(f"❌ Ошибка: {self.download_item.interruptReasonString()}")
            self.speed_timer.stop()
            
    def show_completion_notification(self):
        """Показывает уведомление о завершении загрузки"""
        try:
            from PyQt5.QtWidgets import QSystemTrayIcon
            
            # Получаем главное окно
            main_window = self.window()
            
            if hasattr(main_window, 'show_download_notification'):
                main_window.show_download_notification(
                    os.path.basename(self.download_item.path()),
                    self.download_item.path()
                )
        except Exception as e:
            print(f"Ошибка при показе уведомления: {e}")