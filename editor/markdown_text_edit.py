from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QFont

class MarkdownTextEdit(QPlainTextEdit):
    """Custom text edit that handles image pasting"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        
        # Set up editor styling
        self.setPlaceholderText("Start writing your markdown here...\n"
                               "Drag and drop .md files to open them.\n"
                               "Paste images directly from clipboard!")
        
        font = QFont()
        font.setPointSize(11)
        font.setFamily("Consolas, Monaco, 'Courier New', monospace")
        self.setFont(font)

    def insertFromMimeData(self, mime_data):
        """Override paste to handle images"""
        if mime_data.hasImage():
            image = mime_data.imageData()
            if not image.isNull():
                # Save image and insert markdown
                saved_path = self.parent_window.image_handler.save_clipboard_image(image)
                if saved_path:
                    alt_name = os.path.splitext(os.path.basename(saved_path))[0]
                    markdown_image = f"![{alt_name}]({saved_path})\n"
                    self.textCursor().insertText(markdown_image)
                return
        
        # Default text paste behavior
        super().insertFromMimeData(mime_data)