# main.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QListWidget, QTextEdit, QWidget, QHBoxLayout
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Connection Manager")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Splitter to divide left and right panes
        splitter = QSplitter(Qt.Horizontal)

        # Left pane: list widget (for connections and folders)
        self.left_pane = QListWidget()
        splitter.addWidget(self.left_pane)

        # Right pane: text edit (for displaying connection outputs)
        self.right_pane = QTextEdit()
        self.right_pane.setReadOnly(True)
        splitter.addWidget(self.right_pane)

        # Add splitter to the main layout
        layout.addWidget(splitter)

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
