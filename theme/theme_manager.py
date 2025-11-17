from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QPainter, QPen, QFont, QPixmap, QIcon

class ThemeManager:
    """Manages application themes (light/dark modes)"""
    
    def __init__(self, main_window):
        self.main_window = main_window
    
    def apply_theme(self):
        """Apply the current theme (day/night) to the entire application"""
        if self.main_window.night_mode:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()
    
    def apply_dark_theme(self):
        """Apply dark theme to all UI components"""
        # Dark palette
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(45, 45, 48))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.AlternateBase, QColor(45, 45, 48))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(45, 45, 48))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        self.main_window.setPalette(dark_palette)
        
        # Apply stylesheets
        self._apply_dark_editor_style()
        self._apply_dark_toolbar_style()
        self._apply_dark_menubar_style()
        self._apply_dark_statusbar_style()
    
    def apply_light_theme(self):
        """Apply light theme to all UI components"""
        # Light palette - use default system palette
        self.main_window.setPalette(self.main_window.style().standardPalette())
        
        # Apply stylesheets
        self._apply_light_editor_style()
        self._apply_light_toolbar_style()
        self._apply_light_menubar_style()
        self._apply_light_statusbar_style()
    
    def _apply_dark_editor_style(self):
        """Apply dark theme to editor"""
        self.main_window.editor.setStyleSheet("""
            QPlainTextEdit {
                background-color: #2d2d30;
                color: #f1f1f1;
                selection-background-color: #264f78;
                border: 1px solid #3e3e42;
            }
        """)
    
    def _apply_light_editor_style(self):
        """Apply light theme to editor"""
        self.main_window.editor.setStyleSheet("""
            QPlainTextEdit {
                background-color: #ffffff;
                color: #333333;
                selection-background-color: #3399ff;
                border: 1px solid #ddd;
            }
        """)
    
    def _apply_dark_toolbar_style(self):
        """Apply dark theme to toolbar"""
        self.main_window.toolbar.setStyleSheet("""
            QToolBar {
                background-color: #3e3e42;
                border: 1px solid #555;
            }
            QToolButton {
                color: #f1f1f1;
                background-color: transparent;
                border: none;
                padding: 5px;
            }
            QToolButton:hover {
                background-color: #555;
            }
            QToolButton:checked {
                background-color: #264f78;
            }
        """)
    
    def _apply_light_toolbar_style(self):
        """Apply light theme to toolbar"""
        self.main_window.toolbar.setStyleSheet("""
            QToolBar {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
            }
            QToolButton {
                color: #333;
                background-color: transparent;
                border: none;
                padding: 5px;
            }
            QToolButton:hover {
                background-color: #e0e0e0;
            }
            QToolButton:checked {
                background-color: #3399ff;
                color: white;
            }
        """)
    
    def _apply_dark_menubar_style(self):
        """Apply dark theme to menu bar"""
        self.main_window.menuBar().setStyleSheet("""
            QMenuBar {
                background-color: #3e3e42;
                color: #f1f1f1;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #555;
            }
            QMenu {
                background-color: #3e3e42;
                color: #f1f1f1;
            }
            QMenu::item:selected {
                background-color: #555;
            }
        """)
    
    def _apply_light_menubar_style(self):
        """Apply light theme to menu bar"""
        self.main_window.menuBar().setStyleSheet("""
            QMenuBar {
                background-color: #f5f5f5;
                color: #333;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #e0e0e0;
            }
            QMenu {
                background-color: #f5f5f5;
                color: #333;
            }
            QMenu::item:selected {
                background-color: #e0e0e0;
            }
        """)
    
    def _apply_dark_statusbar_style(self):
        """Apply dark theme to status bar"""
        self.main_window.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #3e3e42;
                color: #f1f1f1;
            }
            QLabel {
                color: #f1f1f1;
            }
        """)
    
    def _apply_light_statusbar_style(self):
        """Apply light theme to status bar"""
        self.main_window.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #f5f5f5;
                color: #333;
            }
            QLabel {
                color: #333;
            }
        """)
    
    def set_app_icon(self):
        """Set application icon with theme awareness"""
        try:
            # Create a simple icon programmatically
            icon = QPixmap(32, 32)
            icon.fill(Qt.transparent)
            painter = QPainter(icon)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Draw a simple "M" for Markdown
            if self.main_window.night_mode:
                painter.setPen(QPen(Qt.white, 2))
                painter.setBrush(QColor(255, 255, 255))
            else:
                painter.setPen(QPen(Qt.black, 2))
                painter.setBrush(QColor(0, 0, 0))
            
            font = QFont("Arial", 20, QFont.Bold)
            painter.setFont(font)
            painter.drawText(icon.rect(), Qt.AlignCenter, "M")
            painter.end()
            
            self.main_window.setWindowIcon(QIcon(icon))
        except Exception as e:
            print(f"Failed to set app icon: {e}")
            # Fallback to default icon if drawing fails