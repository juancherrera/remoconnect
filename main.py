# main.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

def main():
    # Create the application
    app = QApplication(sys.argv)

    # Create the main window
    main_window = QMainWindow()
    main_window.setWindowTitle("Connection Manager")
    main_window.setGeometry(100, 100, 800, 600)  # x, y, width, height

    # Show the main window
    main_window.show()

    # Start the application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()