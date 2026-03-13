from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QDialogButtonBox, QMessageBox, QListWidgetItem
from PyQt5.QtCore import Qt

class HistoryDialog(QDialog):
    def __init__(self, browser_window):
        super().__init__(browser_window)
        self.browser_window = browser_window
        self.setWindowTitle("История")
        self.setGeometry(200, 200, 600, 400)
        
        # Применяем тему
        theme = browser_window.current_theme
        self.setStyleSheet(browser_window.theme_switcher.get_dialog_style(theme))
        
        self.setup_ui()
        self.load_history()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.open_history_item)
        layout.addWidget(self.history_list)
        
        # Кнопки
        button_box = QDialogButtonBox()
        clear_btn = button_box.addButton("Очистить историю", QDialogButtonBox.ActionRole)
        close_btn = button_box.addButton("Закрыть", QDialogButtonBox.RejectRole)
        
        clear_btn.clicked.connect(self.clear_history)
        close_btn.clicked.connect(self.close)
        
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        
    def load_history(self):
        """Загружает все закладки из базы данных"""
        if hasattr(self.browser_window, 'incognito') and self.browser_window.incognito:
            return
        history_items = self.browser_window.database.get_history()
        
        for title, url, time in history_items:
            item_text = f"{title}\n{url} ({time})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, url)
            self.history_list.addItem(item)
            
    def open_history_item(self, item):
        url = item.data(Qt.UserRole)
        self.browser_window.open_url(url)
        self.close()
        
    def clear_history(self):
        reply = QMessageBox.question(
            self, "Очистка истории",
            "Вы уверены, что хотите очистить всю историю?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.browser_window.database.clear_history()
            self.history_list.clear()
            QMessageBox.information(self, "Успех", "История очищена!")