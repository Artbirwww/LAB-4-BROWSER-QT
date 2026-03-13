from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QDialogButtonBox, QMessageBox, QListWidgetItem
from PyQt5.QtCore import Qt

class BookmarksDialog(QDialog):
    def __init__(self, browser_window):
        super().__init__(browser_window)
        self.browser_window = browser_window
        self.setWindowTitle("Все закладки")
        self.setGeometry(200, 200, 500, 400)
        
        # Применяем тему - используем правильное имя атрибута (theme_switcher)
        theme = browser_window.current_theme
        if hasattr(browser_window, 'theme_switcher'):
            self.setStyleSheet(browser_window.theme_switcher.get_dialog_style(theme))
        
        self.setup_ui()
        self.load_bookmarks()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        self.bookmarks_list = QListWidget()
        self.bookmarks_list.itemDoubleClicked.connect(self.open_bookmark)
        layout.addWidget(self.bookmarks_list)
        
        # Кнопки
        button_box = QDialogButtonBox()
        delete_btn = button_box.addButton("Удалить выбранное", QDialogButtonBox.ActionRole)
        close_btn = button_box.addButton("Закрыть", QDialogButtonBox.RejectRole)
        
        delete_btn.clicked.connect(self.delete_selected)
        close_btn.clicked.connect(self.close)
        
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        
    def load_bookmarks(self):
        """Загружает все закладки из базы данных"""
        if hasattr(self.browser_window, 'incognito') and self.browser_window.incognito:
            return
        self.bookmarks_list.clear()
        bookmarks = self.browser_window.database.get_all_bookmarks()
        
        for title, url in bookmarks:
            item_text = f"{title}\n{url}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, url)
            self.bookmarks_list.addItem(item)
            
    def open_bookmark(self, item):
        """Открывает закладку в текущей вкладке"""
        url = item.data(Qt.UserRole)
        self.browser_window.open_url(url)
        self.close()
        
    def delete_selected(self):
        """Удаляет выбранную закладку"""
        current_item = self.bookmarks_list.currentItem()
        if current_item:
            url = current_item.data(Qt.UserRole)
            title = current_item.text().split('\n')[0]  # Берем только название
            
            reply = QMessageBox.question(
                self, "Удаление закладки",
                f"Удалить закладку '{title}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Удаляем из базы данных
                self.browser_window.database.delete_bookmark(url)
                
                # Удаляем из списка
                self.bookmarks_list.takeItem(self.bookmarks_list.row(current_item))
                
                # Обновляем панель закладок
                self.browser_window.load_bookmarks()
                
                QMessageBox.information(self, "Успех", "Закладка удалена!")