import os  # Added missing import
from PyQt5.QtWidgets import QStatusBar, QLabel

def setup_statusbar(main_window):
    """Setup the status bar"""
    main_window.status_bar = QStatusBar()
    main_window.setStatusBar(main_window.status_bar)
    
    # Add permanent widgets for image folder and prefix
    main_window.folder_label = QLabel()
    main_window.prefix_label = QLabel()
    main_window.status_bar.addPermanentWidget(main_window.folder_label)
    main_window.status_bar.addPermanentWidget(main_window.prefix_label)
    
    # Show current image folder
    update_status_bar(main_window)

def update_status_bar(main_window):
    """Update status bar with current settings"""
    folder_msg = main_window.image_handler.save_folder or "No default folder set"
    folder_text = f"📁 {os.path.basename(folder_msg)}"
    main_window.folder_label.setText(folder_text)
    main_window.folder_label.setToolTip(f"Image folder: {folder_msg}")
    
    prefix_text = f"🏷️ {main_window.image_handler.name_prefix}"
    main_window.prefix_label.setText(prefix_text)
    main_window.prefix_label.setToolTip(f"Image name prefix: {main_window.image_handler.name_prefix}")
    
    # Show temporary message
    main_window.status_bar.showMessage("Ready", 3000)