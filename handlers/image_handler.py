import os
import time
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QInputDialog, QLabel, QLineEdit, QVBoxLayout, QDialog, QPushButton
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QImage

class ImageHandler:
    def __init__(self, settings: QSettings):
        self.settings = settings
        self.save_folder = self.settings.value("lastImageFolder", "")
        self.name_prefix = self.settings.value("namePrefix", "demo_")
        
        # Create the save folder if it doesn't exist
        if self.save_folder and not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder, exist_ok=True)
    
    def save_clipboard_image(self, image: QImage) -> str | None:
        """Save the clipboard image and return the path for markdown insertion"""
        # Generate timestamped base name
        timestamp = int(time.time())
        base_name = f"pasted_{timestamp}"
        
        # Prompt for name
        chosen_name = self.prompt_for_name(base_name)
        if chosen_name is None:
            return None
        
        # Determine save folder
        if not self.save_folder or not os.path.isdir(self.save_folder):
            # Ask for folder if not set
            folder = QFileDialog.getExistingDirectory(None, "Select Image Save Location")
            if not folder:
                return None
            self.save_folder = folder
            self.settings.setValue("lastImageFolder", self.save_folder)
        
        # Create full file path
        file_name = f"{self.name_prefix}{chosen_name}.png"
        file_path = os.path.join(self.save_folder, file_name)
        
        # Handle duplicates
        counter = 1
        original_path = file_path
        while os.path.exists(file_path):
            base, ext = os.path.splitext(original_path)
            file_path = f"{base}_{counter}{ext}"
            counter += 1
        
        # Save the image
        try:
            if not image.save(file_path, "PNG"):
                raise Exception("Failed to save image")
            
            # Return relative or absolute path for markdown
            return self.get_relative_image_path(file_path)
            
        except Exception as e:
            QMessageBox.critical(None, "Save Image Error", f"Could not save image:\n{str(e)}")
            return None
    
    def prompt_for_name(self, base_name: str) -> str | None:
        """Show a dialog to get the image name"""
        # Create a custom dialog
        dialog = QDialog()
        dialog.setWindowTitle("Save Image")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        # Prefix label (non-editable)
        prefix_label = QLabel(f"Prefix: {self.name_prefix}")
        layout.addWidget(prefix_label)
        
        # Name input
        name_label = QLabel("Name:")
        layout.addWidget(name_label)
        
        name_input = QLineEdit(base_name)
        layout.addWidget(name_input)
        
        # Buttons
        buttons_layout = QVBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(dialog.accept)
        buttons_layout.addWidget(save_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(dialog.reject)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        
        # Show dialog and get result
        if dialog.exec_() == QDialog.Accepted:
            return name_input.text()
        else:
            return None
    
    def get_relative_image_path(self, image_path: str, current_file: str = None) -> str:
        """Convert image path to relative if possible"""
        if current_file:
            try:
                md_dir = os.path.dirname(os.path.abspath(current_file))
                return os.path.relpath(image_path, md_dir)
            except:
                pass
        
        return image_path
    
    def change_folder(self, parent):
        """Open QFileDialog to select new save_folder; update status bar"""
        folder = QFileDialog.getExistingDirectory(
            parent, "Select New Default Image Location", self.save_folder
        )
        
        if folder:
            self.save_folder = folder
            self.settings.setValue("lastImageFolder", self.save_folder)
            os.makedirs(self.save_folder, exist_ok=True)
    
    def change_prefix(self, parent):
        """Open QInputDialog to edit name_prefix"""
        prefix, ok = QInputDialog.getText(
            parent, "Change Name Prefix", 
            "Enter new prefix (e.g., 'demo_' or 'project_'):", 
            text=self.name_prefix
        )
        
        if ok and prefix:
            self.name_prefix = prefix
            self.settings.setValue("namePrefix", self.name_prefix)