import os
import sys
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QSplitter, QMessageBox, QApplication, QFileDialog, QInputDialog
from PyQt5.QtCore import Qt, QTimer, QSettings
from PyQt5.QtGui import QIcon, QPalette, QColor, QPainter, QPen, QFont, QKeySequence

# Local imports
from editor.markdown_text_edit import MarkdownTextEdit
from editor.preview_handler import PreviewHandler
from handlers.file_handler import FileHandler
from handlers.image_handler import ImageHandler
from ui.toolbar import setup_toolbar
from ui.menu import setup_menu
from ui.statusbar import setup_statusbar, update_status_bar
from theme.theme_manager import ThemeManager
from converter.markdown_converter import MarkdownConverter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.is_modified = False
        self.settings = QSettings("MyApp", "Markdown Editor")
        self.night_mode = self.settings.value("nightMode", False, type=bool)
        
        # Initialize handlers
        self.file_handler = FileHandler()
        self.image_handler = ImageHandler(self.settings)
        self.theme_manager = ThemeManager(self)
        self.converter = MarkdownConverter(self)
        
        self.init_ui()
        setup_menu(self)
        setup_toolbar(self)
        setup_statusbar(self)
        self.theme_manager.apply_theme()
        
        # Restore window geometry and splitter state
        self.restore_geometry()
        # Set application icon
        self.set_app_icon()

    def init_ui(self):
        """Initialize the main UI components"""
        self.setWindowTitle("Markdown Editor")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create splitter for resizable panes
        self.splitter = QSplitter(Qt.Horizontal)
        
        # Left pane: Editor
        self.editor = MarkdownTextEdit(self)
        self.editor.textChanged.connect(self.on_text_changed)
        
        # Right pane: Preview
        self.preview_handler = PreviewHandler(self)
        self.preview = self.preview_handler.widget
        
        # Add to splitter
        self.splitter.addWidget(self.editor)
        self.splitter.addWidget(self.preview)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setSizes([700, 700])
        
        self.setCentralWidget(self.splitter)
        self.setAcceptDrops(True)
        
        # Auto-refresh timer (debounced)
        self.preview_timer = QTimer()
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self.update_preview)

    def restore_geometry(self):
        """Restore window geometry and splitter state"""
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        
        splitter_state = self.settings.value("splitterState")
        if splitter_state:
            self.splitter.restoreState(splitter_state)

    def save_geometry(self):
        """Save window geometry and splitter state"""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("splitterState", self.splitter.saveState())

    def dragEnterEvent(self, event):
        """Accept drag events containing .md files"""
        if self.file_handler.validate_drag(event.mimeData()):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Handle file drop - load first valid .md file after save check"""
        paths = self.file_handler.extract_md_paths(event.mimeData())
        if paths and self.check_save():
            self.load_file(paths[0])
        event.acceptProposedAction()  # Always accept to prevent OS default

    def on_text_changed(self):
        """Track modifications and update preview"""
        if not self.is_modified:
            self.is_modified = True
            self.update_window_title()
        
        # Debounce preview updates
        self.preview_timer.stop()
        self.preview_timer.start(300)

    def update_window_title(self):
        """Show current file and modification status"""
        title = "Markdown Editor"
        if self.current_file:
            title += f" - {os.path.basename(self.current_file)}"
        if self.is_modified:
            title += " •"
        self.setWindowTitle(title)

    def new_file(self):
        """Create new document"""
        if self.check_save():
            self.editor.clear()
            self.current_file = None
            self.is_modified = False
            self.update_window_title()
            self.update_preview()

    def open_file(self):
        """Open file dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Markdown File", "",
            "Markdown Files (*.md *.markdown);;Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path):
        """Load file into editor"""
        if self.file_handler.load_file(file_path, self.editor):
            self.current_file = file_path
            self.is_modified = False
            self.update_window_title()
            self.update_preview()
            self.status_bar.showMessage(f"Loaded: {os.path.basename(file_path)}", 3000)

    def save_file(self):
        """Save current file"""
        if self.current_file:
            self.write_file(self.current_file)
        else:
            self.save_file_as()

    def save_file_as(self):
        """Save with new filename"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Markdown File", "",
            "Markdown Files (*.md);;All Files (*)"
        )
        if file_path:
            if not file_path.endswith(('.md', '.markdown')):
                file_path += '.md'
            self.write_file(file_path)

    def write_file(self, file_path):
        """Write content to file"""
        if self.file_handler.save_file(file_path, self.editor.toPlainText()):
            self.current_file = file_path
            self.is_modified = False
            self.update_window_title()
            self.status_bar.showMessage(f"Saved: {os.path.basename(file_path)}", 3000)

    def check_save(self) -> bool:
        """Prompt to save if modified"""
        if not self.is_modified:
            return True
        
        filename = os.path.basename(self.current_file) if self.current_file else 'Untitled'
        reply = QMessageBox.question(
            self, "Save Changes?",
            f"The document '{filename}' has been modified.\nSave changes?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        )
        
        if reply == QMessageBox.Save:
            self.save_file()
            return True
        return reply == QMessageBox.Discard

    def update_preview(self):
        """Render markdown to HTML"""
        self.preview_handler.update_preview(self.editor.toPlainText())

    def wrap_selection(self, before: str, after: str):
        """Wrap selected text with markdown syntax"""
        cursor = self.editor.textCursor()
        selected = cursor.selectedText()
        if selected:
            cursor.insertText(f"{before}{selected}{after}")
        else:
            cursor.insertText(f"{before}{after}")
            # Move cursor between markers
            for _ in range(len(after)):
                cursor.movePosition(cursor.Left)
            self.editor.setTextCursor(cursor)

    def insert_text(self, text: str):
        """Insert text at cursor"""
        self.editor.textCursor().insertText(text)

    def insert_link(self):
        """Insert link markdown"""
        cursor = self.editor.textCursor()
        selected = cursor.selectedText()
        if selected:
            cursor.insertText(f"[{selected}](https://)")
        else:
            cursor.insertText("[link text](https://)")
        self.editor.setFocus()

    def insert_image(self):
        """Insert image markdown via file dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.gif *.svg)"
        )
        if file_path:
            # Make path relative if possible
            saved_path = self.image_handler.get_relative_image_path(file_path, self.current_file)
            alt = os.path.splitext(os.path.basename(saved_path))[0]
            self.insert_text(f"![{alt}]({saved_path})\n")

    def insert_list(self):
        """Insert bulleted list"""
        self.insert_text("- Item 1\n- Item 2\n- Item 3\n")

    def insert_numbered_list(self):
        """Insert numbered list"""
        self.insert_text("1. Item 1\n2. Item 2\n3. Item 3\n")

    def insert_quote(self):
        """Insert blockquote"""
        cursor = self.editor.textCursor()
        selected = cursor.selectedText()
        if selected:
            # Quote each line
            quoted = "\n".join(f"> {line}" for line in selected.split("\n"))
            cursor.insertText(quoted)
        else:
            self.insert_text("> Quote text here\n")

    def change_image_save_location(self):
        """Change the default image save folder"""
        self.image_handler.change_folder(self)
        update_status_bar(self)

    def change_name_prefix(self):
        """Change the image name prefix"""
        self.image_handler.change_prefix(self)
        update_status_bar(self)

    def toggle_night_mode(self):
        """Toggle between day and night mode"""
        self.night_mode = not self.night_mode
        self.settings.setValue("nightMode", self.night_mode)
        self.night_mode_action.setChecked(self.night_mode)
        self.night_mode_toolbar_action.setChecked(self.night_mode)
        
        # Update toolbar icon
        self.night_mode_toolbar_action.setText("☀️" if self.night_mode else "🌙")
        
        self.theme_manager.apply_theme()
        self.update_preview()

    def set_app_icon(self):
        """Set application icon"""
        self.theme_manager.set_app_icon()

    def closeEvent(self, event):
        """Handle application close"""
        if self.check_save():
            self.save_geometry()
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()