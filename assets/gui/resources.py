# gui/resources.py

import os
from PyQt5.QtGui import QIcon

def load_icon(icon_name):
    icons_dir = os.path.join(os.path.dirname(__file__), '..', 'icons')
    icon_path = os.path.join(icons_dir, icon_name)
    return QIcon(icon_path)
