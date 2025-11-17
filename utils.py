"""Utility functions for the markdown editor"""
import os
import platform

def get_default_image_folder():
    """Get the default image folder based on OS"""
    home_dir = os.path.expanduser("~")
    
    if platform.system() == "Windows":
        return os.path.join(home_dir, "Documents", "MarkdownImages")
    elif platform.system() == "Darwin":  # macOS
        return os.path.join(home_dir, "Documents", "MarkdownImages")
    else:  # Linux and others
        return os.path.join(home_dir, "Documents", "MarkdownImages")