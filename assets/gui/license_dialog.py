# gui/license_dialog.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTextEdit, QCheckBox, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt

class LicenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("License Agreement")
        self.setMinimumSize(600, 400)
        self.layout = QVBoxLayout(self)

        license_text = """
        <h2>End-User License Agreement (EULA)</h2>
        <p>
        This software is licensed for personal, non-commercial use only. By using this software,
        you agree not to use it for any commercial purposes. Unauthorized commercial use of this
        software is strictly prohibited.
        </p>
        """

        self.license_label = QLabel(license_text, self)
        self.license_label.setWordWrap(True)

        self.accept_checkbox = QCheckBox("I have read and agree to the terms and conditions.", self)

        self.accept_button = QPushButton("Accept")
        self.accept_button.setEnabled(False)
        self.accept_button.clicked.connect(self.accept)

        self.reject_button = QPushButton("Decline")
        self.reject_button.clicked.connect(self.reject)

        self.accept_checkbox.stateChanged.connect(self.toggle_accept_button)

        self.layout.addWidget(self.license_label)
        self.layout.addWidget(self.accept_checkbox)
        self.layout.addWidget(self.accept_button)
        self.layout.addWidget(self.reject_button)

    def toggle_accept_button(self, state):
        self.accept_button.setEnabled(state == Qt.Checked)

    def accept(self):
        if self.accept_checkbox.isChecked():
            super().accept()
        else:
            QMessageBox.warning(
                self,
                "License Agreement",
                "You must agree to the terms and conditions to use this software."
            )