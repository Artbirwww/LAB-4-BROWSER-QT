from PyQt5.QtWidgets import QTabWidget, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class TabWidget(QTabWidget):
    def __init__(self, browser_window):
        super().__init__()
        self.browser_window = browser_window
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self.tab_changed)
        
    def add_new_tab(self, qurl=None):
        try:
            if qurl is None or isinstance(qurl, bool):
                qurl = QUrl("https://www.google.com")
            elif isinstance(qurl, str):
                qurl = QUrl(qurl)
                
            browser = QWebEngineView()
            browser.setUrl(qurl)
            
            browser.urlChanged.connect(
                lambda url, b=browser: self.browser_window.update_url_bar(url, b)
            )
            browser.loadFinished.connect(
                lambda ok, b=browser: self.update_title(b)
            )
            
            i = self.addTab(browser, "Загрузка...")
            self.setCurrentIndex(i)
            
            self.browser_window.database.add_to_history("Загрузка...", qurl.toString())
            
            print(f"Добавлена новая вкладка. Всего вкладок: {self.count()}")
            
        except Exception as e:
            print(f"Ошибка при создании вкладки: {e}")
            
    def current_browser(self):
        return self.currentWidget()
        
    def tab_changed(self, index):
        browser = self.widget(index)
        if browser:
            self.browser_window.update_url_bar(browser.url(), browser)
            
    def update_title(self, browser):
        try:
            index = self.indexOf(browser)
            if index >= 0:
                title = browser.page().title()
                if title:
                    short_title = title[:20] + "..." if len(title) > 20 else title
                    self.setTabText(index, short_title)
                    
                    self.browser_window.title_bar.update_title(short_title)
                    
                    self.browser_window.database.add_to_history(title, browser.url().toString())
        except Exception as e:
            print(f"Ошибка при обновлении заголовка: {e}")
            
    def close_tab(self, index):
        if self.count() > 1:
            self.removeTab(index)
        else:
            self.browser_window.close()