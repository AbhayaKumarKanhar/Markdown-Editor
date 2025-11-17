import os
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QMimeData, QUrl

class FileHandler:

    def validate_drag(self, mime_data: QMimeData) -> bool:
        """Accept drag if it contains local .md files"""
        if mime_data.hasUrls():
            return any(
                url.isLocalFile() and url.toLocalFile().lower().endswith(('.md', '.markdown'))
                for url in mime_data.urls()
            )
        return False

    def extract_md_paths(self, mime_data: QMimeData) -> list[str]:
        """Extract validated .md file paths from drop data"""
        if not mime_data.hasUrls():
            return []
        
        paths = [
            url.toLocalFile() 
            for url in mime_data.urls() 
            if url.isLocalFile() and url.toLocalFile().lower().endswith(('.md', '.markdown'))
        ]
        
        return paths
    
    def handle_text_file_url(self, text: str) -> list[str]:
        """Handle case where the drop contains text that is a file URL"""
        file_path = self.convert_file_url_to_path(text)
        if file_path and os.path.exists(file_path) and file_path.lower().endswith(('.md', '.markdown')):
            return [file_path]
        return []
    
    def convert_file_url_to_path(self, url_str: str) -> str:
        """Convert a file:// URL to a local file path"""
        # Remove 'file:///' prefix
        path = url_str.replace('file:///', '')
        # Handle Windows paths (convert forward slashes to backslashes)
        path = path.replace('/', '\\')
        # Handle encoded spaces and special characters
        path = path.replace('%20', ' ')
        # Handle encoded parentheses and other special characters
        path = path.replace('%28', '(').replace('%29', ')')
        path = path.replace('%5B', '[').replace('%5D', ']')
        return path.strip()
    
    def load_file(self, file_path: str, editor_widget) -> bool:
        """Read file with UTF-8 encoding, handle FileNotFoundError and UnicodeDecodeError with user-friendly error popups, populate editor on success"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                editor_widget.setPlainText(content)
                return True
        except FileNotFoundError:
            QMessageBox.critical(None, "File Not Found", f"The file '{file_path}' could not be found.")
            return False
        except UnicodeDecodeError:
            QMessageBox.critical(None, "Encoding Error", f"The file '{file_path}' could not be decoded with UTF-8 encoding.")
            return False
        except Exception as e:
            QMessageBox.critical(None, "Error", f"An error occurred while opening the file: {str(e)}")
            return False
    
    def save_file(self, file_path: str, content: str) -> bool:
        """Write content with error handling and status messages"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
                return True
        except Exception as e:
            QMessageBox.critical(None, "Error", f"An error occurred while saving the file: {str(e)}")
            return False