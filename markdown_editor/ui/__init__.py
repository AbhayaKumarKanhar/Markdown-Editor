def init_ui(self):
    """Initialize the main UI components"""
    self.setWindowTitle("Markdown Editor")
    self.setGeometry(100, 100, 1400, 900)
    
    self.splitter = QSplitter(Qt.Horizontal)
    
    # Left pane: Editor
    self.editor = MarkdownTextEdit(self)
    self.editor.setAcceptDrops(False)  # ADD THIS LINE
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