from PyQt5.QtWidgets import QMenu, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

def setup_menu(main_window):
    """Setup the menu bar"""
    menubar = main_window.menuBar()
    
    # File menu
    file_menu = menubar.addMenu("&File")
    actions = [
        ("&New", QKeySequence.New, main_window.new_file),
        ("&Open...", QKeySequence.Open, main_window.open_file),
        None,  # Separator
        ("&Save", QKeySequence.Save, main_window.save_file),
        ("Save &As...", QKeySequence.SaveAs, main_window.save_file_as),
        None,
        ("Change &Image Save Location...", None, main_window.change_image_save_location),
        None,
        ("E&xit", QKeySequence.Quit, main_window.close)
    ]
    for item in actions:
        if item is None:
            file_menu.addSeparator()
        else:
            name, shortcut, callback = item
            action = QAction(name, main_window)
            if shortcut:
                action.setShortcut(shortcut)
            action.triggered.connect(callback)
            file_menu.addAction(action)
    
    # Edit menu
    edit_menu = menubar.addMenu("&Edit")
    edit_actions = [
        ("&Undo", QKeySequence.Undo, main_window.editor.undo),
        ("&Redo", QKeySequence.Redo, main_window.editor.redo),
        None,
        ("&Cut", QKeySequence.Cut, main_window.editor.cut),
        ("&Copy", QKeySequence.Copy, main_window.editor.copy),
        ("&Paste", QKeySequence.Paste, main_window.editor.paste),
        None,
        ("Select &All", QKeySequence.SelectAll, main_window.editor.selectAll),
    ]
    for item in edit_actions:
        if item is None:
            edit_menu.addSeparator()
        else:
            name, shortcut, callback = item
            action = QAction(name, main_window)
            if shortcut:
                action.setShortcut(shortcut)
            action.triggered.connect(callback)
            edit_menu.addAction(action)
    
    # View menu
    view_menu = menubar.addMenu("&View")
    refresh_action = QAction("&Refresh Preview", main_window)
    refresh_action.setShortcut("F5")
    refresh_action.triggered.connect(main_window.update_preview)
    view_menu.addAction(refresh_action)
    
    # Add night mode toggle
    main_window.night_mode_action = QAction("&Night Mode", main_window, checkable=True)
    main_window.night_mode_action.setChecked(main_window.night_mode)
    main_window.night_mode_action.triggered.connect(main_window.toggle_night_mode)
    view_menu.addAction(main_window.night_mode_action)