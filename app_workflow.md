# Pseudo-Code Overview: Markdown Editor Application

## 1. Application Structure
```
MARKDOWN_EDITOR/
├── main.py                 # Application entry point and main window
├── editor/
│   ├── markdown_text_edit.py  # Custom editor with image paste support
│   └── preview_handler.py     # Preview rendering component
├── handlers/
│   ├── file_handler.py        # File operations (open, save, drag/drop)
│   └── image_handler.py       # Image handling (save, insert, path management)
├── ui/
│   ├── toolbar.py            # Toolbar with formatting buttons
│   ├── menu.py               # Menu bar setup
│   └── statusbar.py          # Status bar with image settings display
├── theme/
│   └── theme_manager.py      # Light/dark theme management
├── converter/
│   └── markdown_converter.py # Markdown to HTML conversion
└── utils.py                  # Utility functions
```

## 2. Core Components

### 2.1 Main Application Entry Point
```
FUNCTION main():
    CREATE QApplication instance
    CREATE MainWindow instance
    SHOW main window
    EXECUTE application event loop
```

### 2.2 MainWindow Class
```
CLASS MainWindow:
    ATTRIBUTES:
        - current_file: path to currently open file
        - is_modified: boolean tracking unsaved changes
        - settings: QSettings for persistent storage
        - night_mode: boolean for theme setting
        - editor: MarkdownTextEdit instance
        - preview: HTML preview widget
        - file_handler: FileHandler instance
        - image_handler: ImageHandler instance
        - splitter: UI splitter between editor and preview
        
    METHODS:
        - __init__(): Initialize UI, handlers, and restore settings
        - init_ui(): Setup main window UI components
        - setup_menu(): Configure menu bar
        - setup_toolbar(): Configure formatting toolbar
        - setup_statusbar(): Configure status bar with image settings
        - apply_theme(): Apply light/dark theme throughout app
        - set_app_icon(): Generate and set application icon
        - restore_geometry(): Restore window position/size from settings
        - save_geometry(): Save window position/size to settings
        - dragEnterEvent(): Validate drag operations
        - dropEvent(): Handle file drops
        - on_text_changed(): Track modifications and trigger preview update
        - update_window_title(): Update window title with file name and status
        - new_file(): Create new document after checking for unsaved changes
        - open_file(): Show file dialog and load selected file
        - save_file()/save_file_as(): Save content to file
        - check_save(): Prompt user to save unsaved changes
        - update_preview(): Render markdown as HTML in preview pane
        - wrap_selection(before, after): Wrap selected text with markdown syntax
        - insert_link()/insert_image()/insert_list()/etc.: Insert common markdown elements
        - change_image_save_location()/change_name_prefix(): Configure image handling
        - toggle_night_mode(): Switch between light/dark themes
        - closeEvent(): Handle application closing (save geometry, check unsaved changes)
```

### 2.3 Editor Component
```
CLASS MarkdownTextEdit (extends QPlainTextEdit):
    METHODS:
        - insertFromMimeData(mime_data): 
            IF mime_data contains image:
                save image via image_handler
                insert markdown image syntax
            ELSE:
                default text paste behavior
```

### 2.4 File Handler
```
CLASS FileHandler:
    METHODS:
        - validate_drag(mime_data): Check if dragged content contains .md files
        - extract_md_paths(mime_data): Get valid markdown file paths from drop
        - load_file(file_path, editor): Read file content into editor with error handling
        - save_file(file_path, content): Write content to file with error handling
```

### 2.5 Image Handler
```
CLASS ImageHandler:
    ATTRIBUTES:
        - save_folder: Default folder for images
        - name_prefix: Prefix for image filenames
        - settings: QSettings reference
        
    METHODS:
        - save_clipboard_image(image):
            prompt user for image name
            generate unique filename with timestamp
            handle existing files (add counter suffix)
            save image to configured folder
            return relative path for markdown
            
        - prompt_for_name(base_name):
            show custom dialog with prefix display and name input
            
        - get_relative_image_path(image_path, current_file):
            convert absolute path to relative path when possible
            
        - change_folder(parent): Show dialog to select new default image folder
        - change_prefix(parent): Show dialog to change image name prefix
```

### 2.6 Preview Handler
```
CLASS PreviewHandler:
    METHODS:
        - create_widget(): Initialize preview widget (WebEngineView or QTextBrowser)
        - update_preview(markdown_text): Convert markdown to HTML and display
```

### 2.7 Markdown Converter
```
CLASS MarkdownConverter:
    METHODS:
        - convert_markdown_to_html(text):
            TRY pypandoc (preferred):
                convert with syntax highlighting and math support
            EXCEPT:
                TRY python-markdown library:
                    convert with common extensions
                EXCEPT:
                    return error message
                    
        - wrap_with_light_theme(html)/wrap_with_dark_theme(html):
            wrap HTML content with theme-appropriate CSS
            
        - get_light_theme_css()/get_dark_theme_css():
            return CSS strings for respective themes
            
        - get_preview_template(message)/get_error_template(error):
            return simple HTML templates for messages/errors
```

### 2.8 Theme Manager
```
CLASS ThemeManager:
    METHODS:
        - apply_theme(): Apply current theme (light/dark) to all UI elements
        - apply_dark_theme()/apply_light_theme(): Set specific theme
        - _apply_*_theme() methods: Apply theme to individual UI components
```

## 3. Application Flow

### 3.1 Startup Sequence
```
1. Application initializes
2. MainWindow constructor:
   - Loads settings (theme, geometry, image folder, prefix)
   - Creates handlers (file, image)
   - Initializes UI components
   - Sets up event connections
   - Applies theme
   - Restores window geometry
3. Main window displayed
```

### 3.2 Editing Workflow
```
1. User types in editor
2. Text change detected:
   - Mark document as modified
   - Update window title
   - Start debounce timer for preview update
3. Timer expires:
   - Convert markdown to HTML with current theme
   - Update preview pane
4. User can:
   - Use toolbar/menu to insert formatting
   - Paste images directly
   - Drag/drop markdown files
5. When saving:
   - Prompt if unsaved changes exist
   - Save to existing file or prompt for new filename
```

### 3.3 Image Handling Flow
```
WHEN user pastes image:
1. Override default paste behavior
2. Save image to configured folder with dialog:
   - Show prefix
   - Prompt for name
   - Generate unique filename
3. Insert markdown image syntax with path:
   - Use relative path when possible
   - Default to absolute path
```

### 3.4 Drag & Drop Flow
```
WHEN file dragged over window:
1. Validate if it's a markdown file
2. Accept or reject drag operation
WHEN file dropped:
1. Extract valid markdown file paths
2. Check for unsaved changes
3. Load first valid file into editor
```

## 4. Key Dependencies & Requirements

```
REQUIRED QT MODULES:
- QtWidgets (QMainWindow, QPlainTextEdit, etc.)
- QtCore (QTimer, QSettings, etc.)
- QtGui (QImage, QFont, etc.)
- QtWebEngineWidgets (optional, for better preview)

OPTIONAL PYTHON PACKAGES:
- pypandoc (preferred markdown converter)
- markdown (fallback converter)
```

## 5. Data Flow Diagram

```
+-------------+     +-------------+     +--------------+
|   User UI   |<--->|  MainWindow |<--->| FileHandler  |
+-------------+     +-------------+     +--------------+
      ^                   |                   |
      |                   v                   v
+-------------+     +-------------+     +--------------+
| Image Paste |<--->| ImageHandler|     |   Settings   |
+-------------+     +-------------+     +--------------+
      |
      v
+-------------+     +-------------+     +--------------+
|   Editor    |<--->| PreviewPane |<--->| MarkdownConv |
+-------------+     +-------------+     +--------------+
```

This pseudo-code provides a comprehensive overview of the application architecture, key components, and workflows to guide further development. The modular structure separates concerns clearly, making it easier to extend functionality or fix issues in specific areas without affecting the entire application.