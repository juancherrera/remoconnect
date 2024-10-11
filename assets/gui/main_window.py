# gui/main_window.py

from PyQt5.QtWidgets import (
    QMainWindow, QSplitter, QListWidget, QTextEdit, QWidget, QHBoxLayout,
    QMenu, QAction, QInputDialog, QListWidgetItem
)
from PyQt5.QtCore import Qt, QPoint
from gui.connection_config import ConnectionConfigDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Connection Manager")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Create a splitter
        splitter = QSplitter(Qt.Horizontal)

        # Left pane: list widget
        self.left_pane = QListWidget()
        splitter.addWidget(self.left_pane)

        # Right pane: text edit
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

        menu.exec_(self.left_pane.viewport().mapToGlobal(position))

    def add_folder(self):
        folder_name, ok = QInputDialog.getText(self, "Add Folder", "Folder Name:")
        if ok and folder_name:
            item = QListWidgetItem(folder_name)
            item.setData(Qt.UserRole, {'type': 'folder'})
            self.left_pane.addItem(item)

    def add_connection(self):
        dialog = ConnectionConfigDialog(self)
        if dialog.exec_() == dialog.Accepted:
            connection_data = dialog.get_connection_data()
            item = QListWidgetItem(connection_data['name'])
            item.setData(Qt.UserRole, {'type': 'connection', 'data': connection_data})
            self.left_pane.addItem(item)

    def edit_item(self, item):
        item_data = item.data(Qt.UserRole)
        if item_data['type'] == 'connection':
            connection_data = item_data['data']
            dialog = ConnectionConfigDialog(self, connection_data)
            if dialog.exec_() == dialog.Accepted:
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
            # Simulated successful connection
            self.right_pane.append("Connected successfully!\n")
        else:
            # Handle folder double-click if necessary
            pass
