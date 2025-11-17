from PyQt5.QtWidgets import QToolBar
from PyQt5.QtCore import QSize

def setup_toolbar(main_window):
    """Setup the toolbar with markdown shortcuts"""
    main_window.toolbar = QToolBar("Markdown Tools")
    main_window.toolbar.setIconSize(QSize(16, 16))
    main_window.addToolBar(main_window.toolbar)
    
    # Format actions
    format_actions = [
        ("B", "Bold (Ctrl+B)", lambda: main_window.wrap_selection("**", "**")),
        ("I", "Italic (Ctrl+I)", lambda: main_window.wrap_selection("*", "*")),
        ("`", "Code", lambda: main_window.wrap_selection("`", "`")),
    ]
    for label, tooltip, callback in format_actions:
        action = main_window.toolbar.addAction(label)
        action.setToolTip(tooltip)
        action.triggered.connect(callback)
    
    main_window.toolbar.addSeparator()
    
    # Insert actions
    insert_actions = [
        ("🔗 Link", main_window.insert_link),
        ("🖼️ Image", main_window.insert_image),
        ("• List", main_window.insert_list),
        ("1. Num List", main_window.insert_numbered_list),
        ("> Quote", main_window.insert_quote),
        ("--- Rule", lambda: main_window.insert_text("\n---\n")),
    ]
    for label, callback in insert_actions:
        action = main_window.toolbar.addAction(label)
        action.triggered.connect(callback)
    
    main_window.toolbar.addSeparator()
    
    # Add image folder action with icon
    folder_action = main_window.toolbar.addAction("📁 Image Folder")
    folder_action.setToolTip("Change Default Image Save Location")
    folder_action.triggered.connect(main_window.change_image_save_location)
    
    # Add name prefix action
    prefix_action = main_window.toolbar.addAction("🏷️ Name Prefix")
    prefix_action.setToolTip("Change Image Name Prefix")
    prefix_action.triggered.connect(main_window.change_name_prefix)
    
    # Add night mode toggle with dynamic icon
    main_window.night_mode_toolbar_action = main_window.toolbar.addAction("🌙")
    main_window.night_mode_toolbar_action.setCheckable(True)
    main_window.night_mode_toolbar_action.setChecked(main_window.night_mode)
    main_window.night_mode_toolbar_action.setToolTip("Toggle Night Mode")
    main_window.night_mode_toolbar_action.triggered.connect(main_window.toggle_night_mode)