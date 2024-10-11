# gui/resources.py

import os
from PyQt5.QtGui import QIcon

def load_icon(icon_name):
    """
    Loads an icon from the icons directory.

    Args:
        icon_name (str): The filename of the icon.

    Returns:
        QIcon: The loaded icon.
    """
    # Determine the absolute path to the icons directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    icons_dir = os.path.join(current_dir, '..', 'icons')
    icon_path = os.path.join(icons_dir, icon_name)

    # Check if the icon file exists
    if not os.path.exists(icon_path):
        raise FileNotFoundError(f"Icon file '{icon_path}' not found.")

    return QIcon(icon_path)
