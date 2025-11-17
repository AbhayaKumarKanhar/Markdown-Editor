from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QTextBrowser

try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    WEB_ENGINE_AVAILABLE = True
except ImportError:
    WEB_ENGINE_AVAILABLE = False
    from PyQt5.QtWidgets import QTextBrowser

from pathlib import Path

class PreviewHandler:
    """Handles the preview pane functionality"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.create_widget()
        
    def create_widget(self):
        """Create the preview widget based on available libraries"""
        if WEB_ENGINE_AVAILABLE:
            self.widget = QWebEngineView()
        else:
            self.widget = QTextBrowser()
            self.widget.setOpenExternalLinks(True)
    
    def update_preview(self, markdown_text):
        """Update the preview pane with rendered HTML"""
        if not markdown_text.strip():
            html = self.main_window.converter.get_preview_template("Preview will appear here...")
        else:
            html = self.main_window.converter.convert_markdown_to_html(markdown_text)
        
        if WEB_ENGINE_AVAILABLE:
            self.widget.setHtml(html, baseUrl=QUrl.fromLocalFile(str(Path.cwd())))
        else:
            self.widget.setHtml(html)