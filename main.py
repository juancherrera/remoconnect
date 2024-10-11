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
        layout.addWidget(splitter)

        # Add context menu to left pane
        self.left_pane.setContextMenuPolicy(Qt.CustomContextMenu)
        self.left_pane.customContextMenuRequested.connect(self.show_context_menu)
        self.left_pane.itemDoubleClicked.connect(self.open_connection)

    def show_context_menu(self, position):
        menu = QMenu()

        add_folder_action = QAction("Add Folder", self)
        add_folder_action.triggered.connect(self.add_folder)
        menu.addAction(add_folder_action)

        add_connection_action = QAction("Add Connection", self)
        add_connection_action.triggered.connect(self.add_connection)
        menu.addAction(add_connection_action)

        # Get the item at the clicked position
        item = self.left_pane.itemAt(position)

        if item:
            edit_action = QAction("Edit", self)
            edit_action.triggered.connect(lambda: self.edit_item(item))
            menu.addAction(edit_action)

        # Show the context menu at the cursor position
        menu.exec_(self.left_pane.viewport().mapToGlobal(position))

    def add_folder(self):
        folder_name, ok = QInputDialog.getText(self, "Add Folder", "Folder Name:")
        if ok and folder_name:
            item = QListWidgetItem(folder_name)
            item.setData(Qt.UserRole, {'type': 'folder'})
            self.left_pane.addItem(item)

    def add_connection(self):
        dialog = ConnectionConfigDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            connection_data = dialog.get_connection_data()
            item = QListWidgetItem(connection_data['name'])
            item.setData(Qt.UserRole, {'type': 'connection', 'data': connection_data})
            self.left_pane.addItem(item)

    def edit_item(self, item):
        item_data = item.data(Qt.UserRole)
        if item_data['type'] == 'connection':
            connection_data = item_data['data']
            dialog = ConnectionConfigDialog(self, connection_data)
            if dialog.exec_() == QDialog.Accepted:
                updated_data = dialog.get_connection_data()
                item.setText(updated_data['name'])
                item.setData(Qt.UserRole, {'type': 'connection', 'data': updated_data})
        elif item_data['type'] == 'folder':
            folder_name, ok = QInputDialog.getText(self, "Edit Folder", "Folder Name:", text=item.text())
            if ok and folder_name:
                item.setText(folder_name)

    def open_connection(self, item):
        item_data = item.data(Qt.UserRole)
        if item_data['type'] == 'connection':
            connection_data = item_data['data']
            # Simulate connecting to the host
            self.right_pane.append(f"Connecting to {connection_data['host']} as {connection_data['username']}...")
            # Here you would implement the actual connection logic
            # For now, we'll just simulate a successful connection
            self.right_pane.append("Connected successfully!\n")
        else:
            # If it's a folder, do nothing or expand/collapse if using a tree structure
            pass

def main():
    # Create the application
    app = QApplication(sys.argv)

    # Create and show the main window
    main_window = MainWindow()
    main_window.show()

    # Start the application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
