# main.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QListWidget, QTextEdit,
    QWidget, QHBoxLayout
)
from PyQt5.QtCore import Qt

def main():
    # Create the application
    app = QApplication(sys.argv)

    # Create the main window
    main_window = QMainWindow()
    main_window.setWindowTitle("Connection Manager")
    main_window.setGeometry(100, 100, 800, 600)  # x, y, width, height

    # Create central widget and layout
    central_widget = QWidget()
    main_window.setCentralWidget(central_widget)
    layout = QHBoxLayout(central_widget)

    # Create a splitter
    splitter = QSplitter(Qt.Horizontal)

    # Left pane: list widget (will be used for connections and folders)
    left_pane = QListWidget()
    splitter.addWidget(left_pane)

    # Right pane: text edit (will be used for displaying connection output)
    right_pane = QTextEdit()
    right_pane.setReadOnly(True)
    splitter.addWidget(right_pane)

    # Add splitter to layout
    layout.addWidget(splitter)

    # Show the main window
    main_window.show()

    # Start the application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
