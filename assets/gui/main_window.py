# gui/main_window.py

from PyQt5.QtWidgets import QMainWindow, QSplitter, QWidget, QVBoxLayout, QPlainTextEdit
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Connection Manager")
        self.setGeometry(100, 100, 1200, 800)

        self.splitter = QSplitter(Qt.Horizontal)

        # Left pane: Placeholder for folder/connection tree
        self.left_pane = QWidget()
        self.splitter.addWidget(self.left_pane)

        # Right pane: Placeholder for terminal/connection area
        self.right_pane = QPlainTextEdit()
        self.right_pane.setReadOnly(True)
        self.splitter.addWidget(self.right_pane)

        layout = QVBoxLayout()
        layout.addWidget(self.splitter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
