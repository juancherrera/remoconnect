# gui/main_window.py

from PyQt5.QtWidgets import (
    QMainWindow, QSplitter, QTreeWidget, QTreeWidgetItem,
    QTextEdit, QWidget, QHBoxLayout, QMenu, QAction, QInputDialog, QMessageBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from gui.connection_config import ConnectionConfigDialog

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

        # Left pane: tree widget (for hierarchical structure)
        self.left_pane = QTreeWidget()
        self.left_pane.setHeaderHidden(True)
        splitter.addWidget(self.left_pane)

        # Right pane: text edit (for displaying connection outputs)
        self.right_pane = QTextEdit()
        self.right_pane.setReadOnly(True)
        splitter.addWidget(self.right_pane)

        # Add splitter to the main layout
        layout.addWidget(splitter)

        # Set up context menu for left pane
        self.left_pane.setContextMenuPolicy(Qt.CustomContextMenu)
        self.left_pane.customContextMenuRequested.connect(self.show_context_menu)
        self.left_pane.itemDoubleClicked.connect(self.open_connection)

        # Load icons using QStyle
        self.folder_icon = self.style().standardIcon(getattr(QStyle, 'SP_DirIcon', QStyle.SP_DirClosedIcon))
        self.connection_icon = self.style().standardIcon(getattr(QStyle, 'SP_ComputerIcon', QStyle.SP_FileIcon))

    def show_context_menu(self, position):
        menu = QMenu()

        # Get the item at the clicked position
        item = self.left_pane.itemAt(position)

        if item:
            item_type = item.data(0, Qt.UserRole)
            if item_type == 'folder':
                # Add Connection action
                add_connection_action = QAction("Add Connection", self)
                add_connection_action.triggered.connect(lambda: self.add_connection(item))
                menu.addAction(add_connection_action)

                # Add Sub-Folder action
                add_folder_action = QAction("Add Sub-Folder", self)
                add_folder_action.triggered.connect(lambda: self.add_folder(item))
                menu.addAction(add_folder_action)

                # Edit Folder action
                edit_folder_action = QAction("Edit Folder", self)
                edit_folder_action.triggered.connect(lambda: self.edit_folder(item))
                menu.addAction(edit_folder_action)
            elif item_type == 'connection':
                # Edit Connection action
                edit_connection_action = QAction("Edit Connection", self)
                edit_connection_action.triggered.connect(lambda: self.edit_connection(item))
                menu.addAction(edit_connection_action)
        else:
            # Right-clicked on empty space (root level)
            add_folder_action = QAction("Add Folder", self)
            add_folder_action.triggered.connect(lambda: self.add_folder(None))
            menu.addAction(add_folder_action)

        # Show the context menu at the cursor position
        menu.exec_(self.left_pane.viewport().mapToGlobal(position))

    def add_folder(self, parent_item):
        folder_name, ok = QInputDialog.getText(self, "Add Folder", "Folder Name:")
        if ok and folder_name:
            folder_item = QTreeWidgetItem([folder_name])
            folder_item.setIcon(0, self.folder_icon)
            folder_item.setData(0, Qt.UserRole, 'folder')
            if parent_item:
                parent_item.addChild(folder_item)
                parent_item.setExpanded(True)
            else:
                self.left_pane.addTopLevelItem(folder_item)

    def add_connection(self, parent_item):
        if not parent_item or parent_item.data(0, Qt.UserRole) != 'folder':
            QMessageBox.warning(self, "Invalid Operation", "Connections can only be added under folders.")
            return

        dialog = ConnectionConfigDialog(self)
        if dialog.exec_() == ConnectionConfigDialog.Accepted:
            connection_data = dialog.get_connection_data()
            connection_item = QTreeWidgetItem([connection_data['name']])
            connection_item.setIcon(0, self.connection_icon)
            connection_item.setData(0, Qt.UserRole, 'connection')
            connection_item.setData(1, Qt.UserRole, connection_data)  # Store connection details
            parent_item.addChild(connection_item)
            parent_item.setExpanded(True)

    def edit_folder(self, item):
        current_name = item.text(0)
        folder_name, ok = QInputDialog.getText(self, "Edit Folder", "Folder Name:", text=current_name)
        if ok and folder_name:
            item.setText(0, folder_name)

    def edit_connection(self, item):
        connection_data = item.data(1, Qt.UserRole)
        dialog = ConnectionConfigDialog(self, connection_data)
        if dialog.exec_() == ConnectionConfigDialog.Accepted:
            updated_data = dialog.get_connection_data()
            item.setText(0, updated_data['name'])
            item.setData(1, Qt.UserRole, updated_data)

    def open_connection(self, item, column):
        item_type = item.data(0, Qt.UserRole)
        if item_type == 'connection':
            connection_data = item.data(1, Qt.UserRole)
            connection_name = connection_data.get('name', 'Unnamed Connection')
            host = connection_data.get('host', 'Unknown Host')
            username = connection_data.get('username', 'Unknown User')
            # Simulate connecting to the host
            self.right_pane.append(f"Connecting to {host} as {username}...")
            # Here you would implement the actual connection logic
            # For demonstration, we'll simulate a successful connection
            self.right_pane.append(f"Connected successfully to {host}!\n")
        else:
            # If it's a folder, you can toggle expansion
            item.setExpanded(not item.isExpanded())
