from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

class ThemeManager:
    THEMES = {
        "light": {
            "name": "☀️ Светлая",
            "bg": "#f0f0f0",
            "fg": "#000000",
            "button": "#e0e0e0",
            "button_hover": "#d0d0d0",
            "button_pressed": "#c0c0c0",
            "border": "#b0b0b0",
            "input_bg": "#ffffff",
            "tab_selected": "#ffffff",
            "menu_bg": "#f0f0f0"
        },
        "dark": {
            "name": "🌙 Темная",
            "bg": "#2d2d2d",
            "fg": "#ffffff",
            "button": "#3d3d3d",
            "button_hover": "#4d4d4d",
            "button_pressed": "#5d5d5d",
            "border": "#555555",
            "input_bg": "#3d3d3d",
            "tab_selected": "#2d2d2d",
            "menu_bg": "#3d3d3d"
        },
        "blue": {
            "name": "💙 Синяя",
            "bg": "#e6f0ff",
            "fg": "#003366",
            "button": "#cce0ff",
            "button_hover": "#b8d4ff",
            "button_pressed": "#99bbff",
            "border": "#99bbff",
            "input_bg": "#ffffff",
            "tab_selected": "#ffffff",
            "menu_bg": "#e6f0ff"
        },
        "green": {
            "name": "💚 Зеленая",
            "bg": "#e8f5e8",
            "fg": "#006633",
            "button": "#c8e6c8",
            "button_hover": "#b8dbb8",
            "button_pressed": "#99cc99",
            "border": "#99cc99",
            "input_bg": "#ffffff",
            "tab_selected": "#ffffff",
            "menu_bg": "#e8f5e8"
        },
        "purple": {
            "name": "💜 Фиолетовая",
            "bg": "#f3e8ff",
            "fg": "#660066",
            "button": "#e6ccff",
            "button_hover": "#d9b3ff",
            "button_pressed": "#cc99ff",
            "border": "#cc99ff",
            "input_bg": "#ffffff",
            "tab_selected": "#ffffff",
            "menu_bg": "#f3e8ff"
        }
    }
    
    @classmethod
    def get_theme_names(cls):
        return list(cls.THEMES.keys())
    
    @classmethod
    def get_theme_style(cls, theme_name):
        theme = cls.THEMES.get(theme_name, cls.THEMES["light"])
        
        # Красивый современный шрифт
        font_family = "Segoe UI, 'Microsoft YaHei', sans-serif"

        return f"""
            QMainWindow {{
                background-color: {theme['bg']};
            }}
            QWidget {{
                background-color: {theme['bg']};
                color: {theme['fg']};
                font-family: {font_family};
                font-size: 13px;
            }}
            QPushButton {{
                background-color: {theme['button']};
                border: 1px solid {theme['border']};
                border-radius: 3px;
                padding: 3px;
                color: {theme['fg']};
            }}
            QPushButton:hover {{
                background-color: {theme['button_hover']};
            }}
            QPushButton:pressed {{
                background-color: {theme['button_pressed']};
            }}
            QLineEdit {{
                background-color: {theme['input_bg']};
                border: 1px solid {theme['border']};
                border-radius: 3px;
                padding: 3px;
                color: {theme['fg']};
            }}
            QTabWidget::pane {{
                border: 1px solid {theme['border']};
                background-color: {theme['input_bg']};
            }}
            QTabBar::tab {{
                background-color: {theme['button']};
                border: 1px solid {theme['border']};
                padding: 5px;
                color: {theme['fg']};
            }}
            QTabBar::tab:selected {{
                background-color: {theme['tab_selected']};
            }}
            QTabBar::tab:hover {{
                background-color: {theme['button_hover']};
            }}
            QMenu {{
                background-color: {theme['menu_bg']};
                color: {theme['fg']};
                border: 1px solid {theme['border']};
            }}
            QMenu::item:selected {{
                background-color: {theme['button_hover']};
            }}
            QLabel {{
                color: {theme['fg']};
            }}
            QDialog {{
                background-color: {theme['bg']};
            }}
        """
    
    @classmethod
    def get_dialog_style(cls, theme_name):
        theme = cls.THEMES.get(theme_name, cls.THEMES["light"])
        return f"background-color: {theme['bg']}; color: {theme['fg']};"