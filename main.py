# main.py

import sys
import os

# Add the directory containing 'gui' to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from gui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
