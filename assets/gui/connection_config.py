# gui/connection_config.py

from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt

class ConnectionConfigDialog(QDialog):
    def __init__(self, parent=None, connection_data=None):
        super().__init__(parent)
        self.setWindowTitle("Connection Configuration")
        self.setMinimumSize(300, 200)
        self.connection_data = connection_data or {}

        # Create form layout
        self.form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.host_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
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
        self.save_button.clicked.connect(self.validate_and_accept)
        self.cancel_button.clicked.connect(self.reject)

        # Layout for buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

    def validate_and_accept(self):
        # Basic validation to ensure no fields are empty
        if not self.name_input.text().strip():
            self.show_error("Name cannot be empty.")
            return
        if not self.host_input.text().strip():
            self.show_error("Host cannot be empty.")
            return
        if not self.username_input.text().strip():
            self.show_error("Username cannot be empty.")
            return
        # Password can be optional, depending on your requirements

        self.accept()

    def show_error(self, message):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.warning(self, "Input Error", message)

    def get_connection_data(self):
        return {
            'name': self.name_input.text().strip(),
            'host': self.host_input.text().strip(),
            'username': self.username_input.text().strip(),
            'password': self.password_input.text()  # Consider handling passwords securely
        }
