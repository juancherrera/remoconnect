# main.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QListWidget, QTextEdit,
    QWidget, QHBoxLayout, QMenu, QAction, QInputDialog, QListWidgetItem,
    QDialog, QLabel, QLineEdit, QPushButton, QFormLayout, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QPoint

class ConnectionConfigDialog(QDialog):
    def __init__(self, parent=None, connection_data=None):
        super().__init__(parent)
        self.setWindowTitle("Connection Configuration")
        self.setMinimumSize(300, 200)
        self.connection_data = connection_data or {}

        # Create form layout
        self.form_layout = QFormLayout()

        self.name_input = QLineEdit(self)
        self.host_input = QLineEdit(self)
        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.form_layout.addRow("Name:", self.name_input)
        self.form_layout.addRow("Host:", self.host_input)
        self.form_layout.addRow("Username:", self.username_input)
        self.form_layout.addRow("Password:", self.password_input)

        # Load existing data if editing
        if self.connection_data:
            self.name_input.setText(self.connection_data.get('name', ''))
            self.host_input.setText(self.connection_data.get('host', ''))
            self.username_input.setText(self.connection_data.get('username', ''))
            self.password_input.setText(self.connection_data.get('password', ''))

        # Buttons
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # Layout
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

    def get_connection_data(self):
        return {
            'name': self.name_input.text(),
            'host': self.host_input.text(),
            'username': self.username_input.text(),
            'password': self.password_input.text()
        }

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Connection Manager")
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Create a splitter
        splitter = QSplitter(Qt.Horizontal)

        # Left pane: list widget (will be used for connections and folders)
        self.left_pane = QListWidget()
        splitter.addWidget(self.left_pane)

        # Right pane: text edit (will be used for displaying connection output)
        self.right_pane = QTextEdit()
        self.right_pane.setReadOnly(True)
        splitter.addWidget(self.right_pane)

        # Add splitter to layout
        layout.addWidget(spli
