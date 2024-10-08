from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, QVBoxLayout, QPushButton,
    QHBoxLayout, QTextEdit, QCheckBox
)
from PyQt5.QtCore import Qt

class ConnectionConfigDialog(QDialog):
    def __init__(self, parent=None, connection_data=None):
        super().__init__(parent)
        self.setWindowTitle("Connection Configuration")
        self.setMinimumSize(600, 400)
        self.connection_data = connection_data

        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.name_input = QLineEdit(self)
        self.host_input = QLineEdit(self)
        self.port_input = QLineEdit(self)
        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.connection_type_combo = QComboBox(self)
        self.connection_type_combo.addItems(["SSH", "RDP"])
        self.ssh_options_input = QTextEdit(self)
        self.open_browser_checkbox = QCheckBox("Open browser after connection")

        self.form_layout.addRow("Name", self.name_input)
        self.form_layout.addRow("Host", self.host_input)
        self.form_layout.addRow("Port", self.port_input)
        self.form_layout.addRow("Username", self.username_input)
        self.form_layout.addRow("Password", self.password_input)
        self.form_layout.addRow("Connection Type", self.connection_type_combo)
        self.form_layout.addRow("SSH Options", self.ssh_options_input)
        self.form_layout.addRow("", self.open_browser_checkbox)

        self.layout.addLayout(self.form_layout)

        self.button_box = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.button_box.addWidget(self.save_button)
        self.button_box.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_box)

        if self.connection_data:
            self.load_connection_data()

    def load_connection_data(self):
        self.name_input.setText(self.connection_data.get('name', ''))
        self.host_input.setText(self.connection_data.get('host', ''))
        self.port_input.setText(str(self.connection_data.get('port', '')))
        self.username_input.setText(self.connection_data.get('username', ''))
        self.password_input.setText(self.connection_data.get('password', ''))
        self.connection_type_combo.setCurrentText(self.connection_data.get('type', 'SSH'))
        self.ssh_options_input.setPlainText('\n'.join(self.connection_data.get('ssh_options', [])))
        self.open_browser_checkbox.setChecked(self.connection_data.get('open_browser', False))

    def get_connection_data(self):
        return {
            "name": self.name_input.text(),
            "host": self.host_input.text(),
            "port": int(self.port_input.text()) if self.port_input.text().isdigit() else 22,
            "username": self.username_input.text(),
            "password": self.password_input.text(),
            "type": self.connection_type_combo.currentText(),
            "ssh_options": self.ssh_options_input.toPlainText().split('\n'),
            "open_browser": self.open_browser_checkbox.isChecked()
        }
