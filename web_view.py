from PyQt5.QtWidgets import QMenu, QAction, QMessageBox
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QKeySequence, QGuiApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebEngineCore import QWebEngineContextMenuRequest
import os
import requests

class WebViewWithContextMenu(QWebEngineView):
    """QWebEngineView с кастомным контекстным меню"""
    
    def __init__(self, parent=None, browser_window=None):
        super().__init__(parent)
        self.browser_window = browser_window
        
    def contextMenuEvent(self, event):
        """Обрабатывает событие контекстного меню"""
        # Получаем request контекстного меню
        menu_request = self.lastContextMenuRequest()
        
        if not menu_request:
            return
            
        menu = QMenu(self)
        
        # Получаем информацию из request
        link_url = menu_request.linkUrl()
        image_url = menu_request.mediaUrl()
        is_editable = menu_request.isContentEditable()
        selected_text = menu_request.selectedText()
        
        # Навигация
        back_action = QAction("◀ Назад", self)
        back_action.setShortcut(QKeySequence("Alt+Left"))
        back_action.setEnabled(self.history().canGoBack())
        back_action.triggered.connect(self.back)
        menu.addAction(back_action)
        
        forward_action = QAction("▶ Вперед", self)
        forward_action.setShortcut(QKeySequence("Alt+Right"))
        forward_action.setEnabled(self.history().canGoForward())
        forward_action.triggered.connect(self.forward)
        menu.addAction(forward_action)
        
        reload_action = QAction("🔄 Перезагрузить", self)
        reload_action.setShortcut(QKeySequence("Ctrl+R"))
        reload_action.triggered.connect(self.reload)
        menu.addAction(reload_action)
        
        stop_action = QAction("⏹ Остановить", self)
        stop_action.setShortcut(QKeySequence("Esc"))
        stop_action.triggered.connect(self.stop)
        menu.addAction(stop_action)
        
        menu.addSeparator()
        
        # Действия со страницей
        save_as_action = QAction("💾 Сохранить как...", self)
        save_as_action.setShortcut(QKeySequence("Ctrl+S"))
        save_as_action.triggered.connect(self.save_page)
        menu.addAction(save_as_action)
        
        print_action = QAction("🖨 Печать...", self)
        print_action.setShortcut(QKeySequence("Ctrl+P"))
        print_action.triggered.connect(self.print_page)
        menu.addAction(print_action)
        
        # Действия с выделенным текстом
        if selected_text:
            menu.addSeparator()
            
            copy_action = QAction("📋 Копировать", self)
            copy_action.setShortcut(QKeySequence("Ctrl+C"))
            copy_action.triggered.connect(self.copy)
            menu.addAction(copy_action)
            
            if is_editable:
                cut_action = QAction("✂ Вырезать", self)
                cut_action.setShortcut(QKeySequence("Ctrl+X"))
                cut_action.triggered.connect(self.cut)
                menu.addAction(cut_action)
                
                paste_action = QAction("📌 Вставить", self)
                paste_action.setShortcut(QKeySequence("Ctrl+V"))
                paste_action.triggered.connect(self.paste)
                menu.addAction(paste_action)
            
            search_action = QAction("🔍 Найти в Интернете", self)
            search_action.triggered.connect(lambda: self.search_selection(selected_text))
            menu.addAction(search_action)
            
        # Действия со ссылками
        if link_url and not link_url.isEmpty():
            menu.addSeparator()
            
            link_menu = QMenu("🔗 Ссылка", menu)
            
            open_link_action = QAction("Открыть ссылку", link_menu)
            open_link_action.triggered.connect(lambda: self.setUrl(link_url))
            link_menu.addAction(open_link_action)
            
            open_link_new_tab_action = QAction("Открыть ссылку в новой вкладке", link_menu)
            open_link_new_tab_action.triggered.connect(lambda: self.open_link_in_new_tab(link_url))
            link_menu.addAction(open_link_new_tab_action)
            
            link_menu.addSeparator()
            
            copy_link_action = QAction("Копировать адрес ссылки", link_menu)
            copy_link_action.triggered.connect(lambda: self.copy_link(link_url))
            link_menu.addAction(copy_link_action)
            
            download_link_action = QAction("Сохранить ссылку как...", link_menu)
            download_link_action.triggered.connect(lambda: self.download_link(link_url))
            link_menu.addAction(download_link_action)
            
            menu.addMenu(link_menu)
            
        # Действия с изображениями
        if image_url and not image_url.isEmpty():
            menu.addSeparator()
            
            image_menu = QMenu("🖼 Изображение", menu)
            
            open_image_action = QAction("Открыть изображение", image_menu)
            open_image_action.triggered.connect(lambda: self.setUrl(image_url))
            image_menu.addAction(open_image_action)
            
            save_image_action = QAction("Сохранить изображение как...", image_menu)
            save_image_action.triggered.connect(lambda: self.save_image(image_url))
            image_menu.addAction(save_image_action)
            
            copy_image_action = QAction("Копировать изображение", image_menu)
            copy_image_action.triggered.connect(lambda: self.copy_image(image_url))
            image_menu.addAction(copy_image_action)
            
            copy_image_address_action = QAction("Копировать адрес изображения", image_menu)
            copy_image_address_action.triggered.connect(lambda: self.copy_link(image_url))
            image_menu.addAction(copy_image_address_action)
            
            menu.addMenu(image_menu)
            
        menu.addSeparator()
        
        # Масштабирование
        zoom_menu = QMenu("🔍 Масштаб", menu)
        
        zoom_in_action = QAction("Увеличить", zoom_menu)
        zoom_in_action.setShortcut(QKeySequence("Ctrl+="))
        zoom_in_action.triggered.connect(self.zoom_in)
        zoom_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Уменьшить", zoom_menu)
        zoom_out_action.setShortcut(QKeySequence("Ctrl+-"))
        zoom_out_action.triggered.connect(self.zoom_out)
        zoom_menu.addAction(zoom_out_action)
        
        zoom_reset_action = QAction("Сбросить", zoom_menu)
        zoom_reset_action.setShortcut(QKeySequence("Ctrl+0"))
        zoom_reset_action.triggered.connect(self.zoom_reset)
        zoom_menu.addAction(zoom_reset_action)
        
        menu.addMenu(zoom_menu)
        
        # Дополнительные действия
        menu.addSeparator()
        
        view_source_action = QAction("📄 Просмотреть код страницы", self)
        view_source_action.triggered.connect(self.view_source)
        menu.addAction(view_source_action)
        
        inspect_action = QAction("🔧 Инструменты разработчика", self)
        inspect_action.triggered.connect(self.inspect_element)
        menu.addAction(inspect_action)
        
        # Показываем меню
        menu.exec_(event.globalPos())
        
    def copy(self):
        """Копирует выделенный текст"""
        self.triggerPageAction(QWebEnginePage.Copy)
        
    def cut(self):
        """Вырезает выделенный текст"""
        self.triggerPageAction(QWebEnginePage.Cut)
        
    def paste(self):
        """Вставляет текст"""
        self.triggerPageAction(QWebEnginePage.Paste)
        
    def search_selection(self, selected_text):
        """Ищет выделенный текст в поисковике"""
        if selected_text and self.browser_window:
            search_engine = self.browser_window.get_search_engine()
            url = search_engine + selected_text.replace(" ", "+")
            self.setUrl(QUrl(url))
            
    def save_page(self):
        """Сохраняет страницу"""
        self.page().save()
        
    def print_page(self):
        """Печатает страницу"""
        self.page().print()
        
    def zoom_in(self):
        """Увеличивает масштаб"""
        self.setZoomFactor(self.zoomFactor() + 0.1)
        
    def zoom_out(self):
        """Уменьшает масштаб"""
        self.setZoomFactor(max(0.3, self.zoomFactor() - 0.1))
        
    def zoom_reset(self):
        """Сбрасывает масштаб"""
        self.setZoomFactor(1.0)
        
    def view_source(self):
        """Показывает исходный код страницы"""
        self.page().toHtml(lambda html: self.show_source_window(html))
        
    def show_source_window(self, html):
        """Показывает окно с исходным кодом"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Исходный код страницы")
        dialog.setGeometry(200, 200, 800, 600)
        
        # Применяем тему
        if self.browser_window:
            theme = self.browser_window.current_theme
            if hasattr(self.browser_window, 'theme_switcher'):
                dialog.setStyleSheet(self.browser_window.theme_switcher.get_dialog_style(theme))
        
        layout = QVBoxLayout(dialog)
        
        text_edit = QTextEdit()
        text_edit.setPlainText(html)
        text_edit.setFontFamily("Courier New")
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(dialog.close)
        close_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                border-radius: 5px;
                background-color: #1a73e8;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
        """)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        dialog.exec_()
        
    def inspect_element(self):
        """Открывает инструменты разработчика"""
        # Создаем отдельное окно для DevTools
        if not hasattr(self, 'dev_tools_window'):
            from PyQt5.QtWidgets import QMainWindow
            self.dev_tools_window = QMainWindow()
            self.dev_tools_window.setWindowTitle("Инструменты разработчика")
            self.dev_tools_window.setGeometry(300, 300, 800, 600)
            
            # Создаем виджет DevTools
            dev_tools = QWebEngineView()
            self.dev_tools_window.setCentralWidget(dev_tools)
            
            # Устанавливаем страницу DevTools
            self.page().setDevToolsPage(dev_tools.page())
            
        self.dev_tools_window.show()
        self.dev_tools_window.raise_()
        
    def open_link_in_new_tab(self, url):
        """Открывает ссылку в новой вкладке"""
        if self.browser_window:
            self.browser_window.add_new_tab(url)
            
    def copy_link(self, url):
        """Копирует адрес ссылки в буфер обмена"""
        clipboard = QGuiApplication.clipboard()
        if clipboard:
            clipboard.setText(url.toString())
            
    def save_image(self, url):
        """Сохраняет изображение"""
        if self.browser_window:
            from PyQt5.QtWidgets import QFileDialog
            
            # Показываем диалог сохранения
            file_name = os.path.basename(url.path())
            if not file_name:
                file_name = "image.jpg"
                
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить изображение",
                os.path.join(self.browser_window.get_download_folder(), file_name),
                "Изображения (*.png *.jpg *.jpeg *.gif *.bmp);;Все файлы (*.*)"
            )
            
            if file_path:
                try:
                    response = requests.get(url.toString(), stream=True)
                    if response.status_code == 200:
                        with open(file_path, 'wb') as f:
                            for chunk in response.iter_content(1024):
                                f.write(chunk)
                        QMessageBox.information(self, "Успех", "Изображение сохранено!")
                except Exception as e:
                    QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить изображение: {e}")
                    
    def copy_image(self, url):
        """Копирует изображение в буфер обмена (заглушка)"""
        QMessageBox.information(self, "Информация", 
                               "Копирование изображения в буфер обмена пока не реализовано")
        
    def download_link(self, url):
        """Загружает файл по ссылке"""
        if self.browser_window:
            self.setUrl(url)