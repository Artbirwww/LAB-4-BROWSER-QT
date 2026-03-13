import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('browser.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Создаем таблицу закладок
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookmarks
            (id INTEGER PRIMARY KEY, title TEXT, url TEXT)
        ''')

        # Создаем таблицу истории
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history
            (id INTEGER PRIMARY KEY, title TEXT, url TEXT,
             visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        ''')
        
        # Создаем таблицу настроек
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings
            (key TEXT PRIMARY KEY, value TEXT)
        ''')
        
        # Создаем таблицу загрузок
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS downloads
            (id INTEGER PRIMARY KEY, filename TEXT, url TEXT, 
             file_path TEXT, total_size INTEGER, downloaded INTEGER,
             status TEXT, start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
             finish_time TIMESTAMP)
        ''')
        
        self.conn.commit()

    def get_bookmarks(self, limit=10):
        self.cursor.execute("SELECT title, url FROM bookmarks ORDER BY title LIMIT ?", (limit,))
        return self.cursor.fetchall()

    def get_all_bookmarks(self):
        self.cursor.execute("SELECT title, url FROM bookmarks ORDER BY title")
        return self.cursor.fetchall()

    def add_bookmark(self, title, url):
        self.cursor.execute(
            "INSERT INTO bookmarks (title, url) VALUES (?, ?)",
            (title, url)
        )
        self.conn.commit()

    def delete_bookmark(self, url):
        self.cursor.execute("DELETE FROM bookmarks WHERE url = ?", (url,))
        self.conn.commit()

    def bookmark_exists(self, url):
        self.cursor.execute("SELECT id FROM bookmarks WHERE url = ?", (url,))
        return self.cursor.fetchone() is not None

    def get_history(self, limit=100):
        self.cursor.execute(
            "SELECT title, url, visit_time FROM history ORDER BY visit_time DESC LIMIT ?",
            (limit,)
        )
        return self.cursor.fetchall()

    def add_to_history(self, title, url):
        """Добавляет запись в историю (проверка на инкогнито должна быть на уровне окна)"""
        if url and url != "about:blank" and url != "https://ya.ru" and "Загрузка..." not in title:
            try:
                self.cursor.execute(
                    "INSERT INTO history (title, url) VALUES (?, ?)",
                    (title, url)
                )
                self.conn.commit()
            except Exception as e:
                print(f"Ошибка при добавлении в историю: {e}")

    def clear_history(self):
        self.cursor.execute("DELETE FROM history")
        self.conn.commit()

    def get_setting(self, key, default=None):
        self.cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        result = self.cursor.fetchone()
        return result[0] if result else default

    def save_setting(self, key, value):
        self.cursor.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, value)
        )
        self.conn.commit()

    def add_download(self, filename, url, file_path, total_size):
        """Добавляет запись о загрузке"""
        self.cursor.execute(
            "INSERT INTO downloads (filename, url, file_path, total_size, downloaded, status) VALUES (?, ?, ?, ?, 0, 'started')",
            (filename, url, file_path, total_size)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def update_download_progress(self, download_id, downloaded):
        """Обновляет прогресс загрузки"""
        self.cursor.execute(
            "UPDATE downloads SET downloaded = ? WHERE id = ?",
            (downloaded, download_id)
        )
        self.conn.commit()

    def finish_download(self, download_id, status='completed'):
        """Завершает загрузку"""
        self.cursor.execute(
            "UPDATE downloads SET status = ?, finish_time = CURRENT_TIMESTAMP WHERE id = ?",
            (status, download_id)
        )
        self.conn.commit()

    def get_downloads(self, limit=50):
        """Возвращает историю загрузок"""
        self.cursor.execute(
            "SELECT filename, url, file_path, total_size, downloaded, status, start_time, finish_time FROM downloads ORDER BY start_time DESC LIMIT ?",
            (limit,)
        )
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()