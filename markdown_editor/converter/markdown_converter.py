import os
from pathlib import Path
from PyQt5.QtWidgets import QMessageBox

try:
    import pypandoc
    PANDOC_AVAILABLE = True
except ImportError:
    PANDOC_AVAILABLE = False

try:
    from markdown import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

class MarkdownConverter:
    """Handles conversion of markdown to HTML with proper theming"""
    
    def __init__(self, main_window):
        self.main_window = main_window
    
    def convert_markdown_to_html(self, text):
        """Convert markdown to HTML using available converters"""
        # Try pypandoc first (more powerful)
        if PANDOC_AVAILABLE:
            try:
                html = pypandoc.convert_text(
                    text, 'html5',
                    format='markdown',
                    extra_args=['--standalone', '--mathjax', '--syntax-highlighting=pygments']
                )
                # Apply theme
                if self.main_window.night_mode:
                    return self.wrap_with_dark_theme(html)
                else:
                    return self.wrap_with_light_theme(html)
            except Exception as e:
                print(f"Pandoc conversion failed: {e}")
        
        # Fall back to python-markdown
        if MARKDOWN_AVAILABLE:
            try:
                extensions = [
                    'fenced_code', 'codehilite', 'tables', 'toc',
                    'footnotes', 'meta', 'sane_lists', 'smarty',
                    'nl2br', 'attr_list', 'def_list', 'abbr', 'md_in_html'
                ]
                html = markdown(text, extensions=extensions, output_format='html5')
                # Apply theme
                if self.main_window.night_mode:
                    return self.wrap_with_dark_theme(html)
                else:
                    return self.wrap_with_light_theme(html)
            except Exception as e:
                return self.get_error_template(f"Markdown conversion error: {e}")
        
        return self.get_error_template("No markdown converter available! Install 'markdown' or 'pypandoc'")
    
    def get_light_theme_css(self):
        """Get CSS for light theme"""
        return """
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3, h4, h5, h6 {
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
        }
        h1 { font-size: 2em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
        h2 { font-size: 1.5em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
        h3 { font-size: 1.25em; }
        h4 { font-size: 1em; }
        h5 { font-size: 0.875em; }
        h6 { font-size: 0.85em; color: #6a737d; }
        p { margin-bottom: 16px; }
        a {
            color: #0366d6;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        blockquote {
            padding: 0 1em;
            color: #6a737d;
            border-left: 0.25em solid #dfe2e5;
            margin: 0 0 16px 0;
        }
        code {
            padding: 0.2em 0.4em;
            margin: 0;
            font-size: 85%;
            background-color: rgba(27, 31, 35, 0.05);
            border-radius: 3px;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        }
        pre {
            padding: 16px;
            overflow: auto;
            font-size: 85%;
            line-height: 1.45;
            background-color: #f6f8fa;
            border-radius: 6px;
            margin-bottom: 16px;
        }
        pre code {
            padding: 0;
            margin: 0;
            font-size: 100%;
            background-color: transparent;
            border-radius: 0;
        }
        table {
            border-spacing: 0;
            border-collapse: collapse;
            margin-bottom: 16px;
            width: 100%;
        }
        table th, table td {
            padding: 6px 13px;
            border: 1px solid #dfe2e5;
        }
        table th {
            font-weight: 600;
            background-color: #f6f8fa;
        }
        table tr:nth-child(2n) {
            background-color: #f6f8fa;
        }
        img {
            max-width: 100%;
            height: auto;
            box-shadow: 0 1px 5px rgba(0,0,0,0.1);
            border-radius: 4px;
            margin: 10px 0;
        }
        hr {
            height: 0.25em;
            padding: 0;
            margin: 24px 0;
            background-color: #e1e4e8;
            border: 0;
        }
        ul, ol {
            padding-left: 2em;
            margin-bottom: 16px;
        }
        li {
            margin-bottom: 0.25em;
        }
        .task-list-item {
            list-style-type: none;
        }
        .task-list-item input {
            margin-right: 0.5em;
        }
        """
    
    def get_dark_theme_css(self):
        """Get CSS for dark theme"""
        return """
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #e1e4e8;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #24292e;
        }
        h1, h2, h3, h4, h5, h6 {
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
            color: #f0f6fc;
        }
        h1 { font-size: 2em; border-bottom: 1px solid #373e47; padding-bottom: 0.3em; }
        h2 { font-size: 1.5em; border-bottom: 1px solid #373e47; padding-bottom: 0.3em; }
        h3 { font-size: 1.25em; }
        h4 { font-size: 1em; }
        h5 { font-size: 0.875em; }
        h6 { font-size: 0.85em; color: #8b949e; }
        p { margin-bottom: 16px; }
        a {
            color: #58a6ff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        blockquote {
            padding: 0 1em;
            color: #8b949e;
            border-left: 0.25em solid #3b434b;
            margin: 0 0 16px 0;
        }
        code {
            padding: 0.2em 0.4em;
            margin: 0;
            font-size: 85%;
            background-color: rgba(110, 118, 129, 0.4);
            border-radius: 3px;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        }
        pre {
            padding: 16px;
            overflow: auto;
            font-size: 85%;
            line-height: 1.45;
            background-color: #2d333b;
            border-radius: 6px;
            margin-bottom: 16px;
        }
        pre code {
            padding: 0;
            margin: 0;
            font-size: 100%;
            background-color: transparent;
            border-radius: 0;
        }
        table {
            border-spacing: 0;
            border-collapse: collapse;
            margin-bottom: 16px;
            width: 100%;
        }
        table th, table td {
            padding: 6px 13px;
            border: 1px solid #3b434b;
        }
        table th {
            font-weight: 600;
            background-color: #2d333b;
        }
        table tr:nth-child(2n) {
            background-color: #2d333b;
        }
        img {
            max-width: 100%;
            height: auto;
            box-shadow: 0 1px 5px rgba(0,0,0,0.3);
            border-radius: 4px;
            margin: 10px 0;
            background-color: #fff;
        }
        hr {
            height: 0.25em;
            padding: 0;
            margin: 24px 0;
            background-color: #3b434b;
            border: 0;
        }
        ul, ol {
            padding-left: 2em;
            margin-bottom: 16px;
        }
        li {
            margin-bottom: 0.25em;
        }
        .task-list-item {
            list-style-type: none;
        }
        .task-list-item input {
            margin-right: 0.5em;
        }
        """
    
    def wrap_with_light_theme(self, html):
        """Wrap HTML with light theme CSS"""
        return f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                {self.get_light_theme_css()}
                /* Code highlighting */
                .highlight {{
                    margin-bottom: 16px;
                }}
                .highlight pre {{
                    margin-bottom: 0;
                    word-wrap: normal;
                }}
                .highlight .c {{ color: #999988; font-style: italic }}
                .highlight .err {{ color: #a61717; background-color: #e3d2d2 }}
                .highlight .k {{ color: #000000; font-weight: bold }}
                .highlight .o {{ color: #000000; font-weight: bold }}
                .highlight .cm {{ color: #999988; font-style: italic }}
                .highlight .cp {{ color: #999999; font-weight: bold }}
                .highlight .c1 {{ color: #999988; font-style: italic }}
                .highlight .cs {{ color: #999999; font-weight: bold; font-style: italic }}
                .highlight .gd {{ color: #000000; background-color: #ffdddd }}
                .highlight .ge {{ color: #000000; font-style: italic }}
                .highlight .gr {{ color: #aa0000 }}
                .highlight .gh {{ color: #999999 }}
                .highlight .gi {{ color: #000000; background-color: #ddffdd }}
                .highlight .go {{ color: #888888 }}
                .highlight .gp {{ color: #555555 }}
                .highlight .gs {{ font-weight: bold }}
                .highlight .gu {{ color: #aaaaaa }}
                .highlight .gt {{ color: #aa0000 }}
                .highlight .kc {{ color: #000000; font-weight: bold }}
                .highlight .kd {{ color: #000000; font-weight: bold }}
                .highlight .kn {{ color: #000000; font-weight: bold }}
                .highlight .kp {{ color: #000000; font-weight: bold }}
                .highlight .kr {{ color: #000000; font-weight: bold }}
                .highlight .kt {{ color: #445588; font-weight: bold }}
                .highlight .m {{ color: #009999 }}
                .highlight .s {{ color: #d14 }}
                .highlight .na {{ color: #008080 }}
                .highlight .nb {{ color: #0086B3 }}
                .highlight .nc {{ color: #445588; font-weight: bold }}
                .highlight .no {{ color: #008080 }}
                .highlight .ni {{ color: #800080 }}
                .highlight .ne {{ color: #990000; font-weight: bold }}
                .highlight .nf {{ color: #990000; font-weight: bold }}
                .highlight .nn {{ color: #555555 }}
                .highlight .nt {{ color: #000080 }}
                .highlight .nv {{ color: #008080 }}
                .highlight .ow {{ color: #000000; font-weight: bold }}
                .highlight .w {{ color: #bbbbbb }}
                .highlight .mf {{ color: #009999 }}
                .highlight .mh {{ color: #009999 }}
                .highlight .mi {{ color: #009999 }}
                .highlight .mo {{ color: #009999 }}
                .highlight .sb {{ color: #d14 }}
                .highlight .sc {{ color: #d14 }}
                .highlight .sd {{ color: #d14 }}
                .highlight .s2 {{ color: #d14 }}
                .highlight .se {{ color: #d14 }}
                .highlight .sh {{ color: #d14 }}
                .highlight .si {{ color: #d14 }}
                .highlight .sx {{ color: #d14 }}
                .highlight .sr {{ color: #009926 }}
                .highlight .s1 {{ color: #d14 }}
                .highlight .ss {{ color: #990073 }}
                .highlight .bp {{ color: #999999 }}
                .highlight .vc {{ color: #008080 }}
                .highlight .vg {{ color: #008080 }}
                .highlight .vi {{ color: #008080 }}
                .highlight .il {{ color: #009999 }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
    
    def wrap_with_dark_theme(self, html):
        """Wrap HTML with dark theme CSS"""
        return f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                {self.get_dark_theme_css()}
                /* Code highlighting for dark theme */
                .highlight {{
                    margin-bottom: 16px;
                }}
                .highlight pre {{
                    margin-bottom: 0;
                    word-wrap: normal;
                }}
                .highlight .c {{ color: #6a737d }}
                .highlight .err {{ color: #f85149 }}
                .highlight .k {{ color: #ff7b72 }}
                .highlight .o {{ color: #ff7b72 }}
                .highlight .cm {{ color: #6a737d }}
                .highlight .cp {{ color: #ff7b72 }}
                .highlight .c1 {{ color: #6a737d }}
                .highlight .cs {{ color: #6a737d }}
                .highlight .gd {{ color: #ffd7d5 }}
                .highlight .ge {{ font-style: italic }}
                .highlight .gr {{ color: #f85149 }}
                .highlight .gh {{ color: #79c0ff }}
                .highlight .gi {{ color: #56d364 }}
                .highlight .go {{ color: #8b949e }}
                .highlight .gp {{ color: #8b949e }}
                .highlight .gs {{ font-weight: bold }}
                .highlight .gu {{ color: #79c0ff }}
                .highlight .gt {{ color: #f85149 }}
                .highlight .kc {{ color: #ff7b72 }}
                .highlight .kd {{ color: #ff7b72 }}
                .highlight .kn {{ color: #ff7b72 }}
                .highlight .kp {{ color: #ff7b72 }}
                .highlight .kr {{ color: #ff7b72 }}
                .highlight .kt {{ color: #ff7b72 }}
                .highlight .m {{ color: #79c0ff }}
                .highlight .s {{ color: #a5d6ff }}
                .highlight .na {{ color: #ffa657 }}
                .highlight .nb {{ color: #ffa657 }}
                .highlight .nc {{ color: #d2a8ff }}
                .highlight .no {{ color: #ffa657 }}
                .highlight .nd {{ color: #d2a8ff }}
                .highlight .ni {{ color: #ffa657 }}
                .highlight .ne {{ color: #f85149 }}
                .highlight .nf {{ color: #d2a8ff }}
                .highlight .nl {{ color: #ffa657 }}
                .highlight .nn {{ color: #ff7b72 }}
                .highlight .nt {{ color: #7ee787 }}
                .highlight .nv {{ color: #ffa657 }}
                .highlight .ow {{ color: #ff7b72 }}
                .highlight .w {{ color: #6e7681 }}
                .highlight .mf {{ color: #79c0ff }}
                .highlight .mh {{ color: #79c0ff }}
                .highlight .mi {{ color: #79c0ff }}
                .highlight .mo {{ color: #79c0ff }}
                .highlight .sb {{ color: #a5d6ff }}
                .highlight .sc {{ color: #a5d6ff }}
                .highlight .sd {{ color: #6e7681 }}
                .highlight .s2 {{ color: #a5d6ff }}
                .highlight .se {{ color: #ffa657 }}
                .highlight .sh {{ color: #a5d6ff }}
                .highlight .si {{ color: #ffa657 }}
                .highlight .sx {{ color: #a5d6ff }}
                .highlight .sr {{ color: #7ee787 }}
                .highlight .s1 {{ color: #a5d6ff }}
                .highlight .ss {{ color: #7ee787 }}
                .highlight .bp {{ color: #ffa657 }}
                .highlight .vc {{ color: #ffa657 }}
                .highlight .vg {{ color: #ffa657 }}
                .highlight .vi {{ color: #ffa657 }}
                .highlight .il {{ color: #79c0ff }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
    
    def get_preview_template(self, message):
        """Get basic HTML template for messages"""
        if self.main_window.night_mode:
            return f"""
            <html>
            <head>
                <style>
                    body {{ 
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        padding: 20px; 
                        color: #e1e4e8;
                        background-color: #24292e;
                    }}
                </style>
            </head>
            <body><p>{message}</p></body>
            </html>
            """
        else:
            return f"""
            <html>
            <head>
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                           padding: 20px; color: #666; }}
                </style>
            </head>
            <body><p>{message}</p></body>
            </html>
            """
    
    def get_error_template(self, error):
        """Get error HTML template"""
        if self.main_window.night_mode:
            return f"""
            <html>
            <head>
                <style>
                    body {{ 
                        font-family: sans-serif; 
                        padding: 20px;
                        color: #e1e4e8;
                        background-color: #24292e;
                    }}
                    .error {{ 
                        color: #f85149; 
                        background: #3d2228; 
                        padding: 10px; 
                        border-radius: 4px; 
                    }}
                </style>
            </head>
            <body>
                <div class="error"><strong>Error:</strong> {error}</div>
            </body>
            </html>
            """
        else:
            return f"""
            <html>
            <head>
                <style>
                    body {{ font-family: sans-serif; padding: 20px; }}
                    .error {{ color: #d73a49; background: #ffeef0; padding: 10px; border-radius: 4px; }}
                </style>
            </head>
            <body>
                <div class="error"><strong>Error:</strong> {error}</div>
            </body>
            </html>
            """