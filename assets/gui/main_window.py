# gui/main_window.py

from PyQt5.QtWidgets import (
    QMainWindow, QSplitter, QTreeWidget, QTreeWidgetItem, QTextEdit, QWidget,
    QHBoxLayout, QMenu, QAction, QInputDialog
)
from PyQt5.QtCore import Qt
from gui.resources import load_icon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_icons()
        self.connect_signals()

    def setup_ui(self):
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

    def load_icons(self):
        """
        Loads icons for folders and connections.
        """
        self.folder_icon = load_icon('folder.png')
        self.connection_icon = load_icon('gear.png')

    def connect_signals(self):
        """
        Connects signals to their respective slots.
        """
        # Set up context menu
        self.left_pane.setContextMenuPolicy(Qt.CustomContextMenu)
        self.left_pane.customContextMenuRequested.connect(self.show_context_menu)

        # Connect double-click signal
        self.left_pane.itemDoubleClicked.connect(self.open_connection)

    def show_context_menu(self, position):
        """
        Displays the context menu based on the clicked item.
        """
        menu = QMenu()

        # Get the item at the clicked position
        selected_item = self.left_pane.itemAt(position)

        if selected_item:
            item_type = selected_item.data(0, Qt.UserRole)
            if item_type == 'folder':
                self.add_folder_actions(menu, selected_item)
            elif item_type == 'connection':
                self.add_connection_actions(menu, selected_item)
        else:
            # Right-clicked on empty space (root level)
            add_folder_action = QAction("Add Folder", self)
            add_folder_action.triggered.connect(lambda: self.add_folder(None))
            menu.addAction(add_folder_action)

        # Show the context menu
        menu.exec_(self.left_pane.viewport().mapToGlobal(position))

    def add_folder_actions(self, menu, parent_item):
        """
        Adds actions related to folders to the context menu.
        """
        add_folder_action = QAction("Add Folder", self)
        add_folder_action.triggered.connect(lambda: self.add_folder(parent_item))
        menu.addAction(add_folder_action)

        add_connection_action = QAction("Add Connection", self)
        add_connection_action.triggered.connect(lambda: self.add_connection(parent_item))
        menu.addAction(add_connection_action)

        edit_folder_action = QAction("Edit Folder", self)
        edit_folder_action.triggered.connect(lambda: self.edit_folder(parent_item))
        menu.addAction(edit_folder_action)

    def add_connection_actions(self, menu, item):
        """
        Adds actions related to connections to the context menu.
        """
        edit_connection_action = QAction("Edit Connection", self)
        edit_connection_action.triggered.connect(lambda: self.edit_connection(item))
        menu.addAction(edit_connection_action)

    def add_folder(self, parent_item):
        """
        Adds a new folder under the specified parent item.
        """
        folder_name, ok = QInputDialog.getText(self, "Add Folder", "Folder Name:")
        if ok and folder_name.strip():
            item = QTreeWidgetItem([folder_name.strip()])
            item.setIcon(0, self.folder_icon)
            item.setData(0, Qt.UserRole, 'folder')
            if parent_item:
                parent_item.addChild(item)
                parent_item.setExpanded(True)
            else:
                self.left_pane.addTopLevelItem(item)

    def add_connection(self, parent_item):
        """
        Adds a new connection under the specified parent folder.
        """
        if not parent_item or parent_item.data(0, Qt.UserRole) != 'folder':
            return  # Connections can only be added under folders

        connection_name, ok = QInputDialog.getText(self, "Add Connection", "Connection Name:")
        if ok and connection_name.strip():
            item = QTreeWidgetItem([connection_name.strip()])
            item.setIcon(0, self.connection_icon)
            item.setData(0, Qt.UserRole, 'connection')
            parent_item.addChild(item)
            parent_item.setExpanded(True)

    def edit_folder(self, item):
        """
        Edits the name of the specified folder.
        """
        current_name = item.text(0)
        new_name, ok = QInputDialog.getText(self, "Edit Folder", "Folder Name:", text=current_name)
        if ok and new_name.strip():
            item.setText(0, new_name.strip())

    def edit_connection(self, item):
        """
        Edits the name of the specified connection.
        """
        current_name = item.text(0)
        new_name, ok = QInputDialog.getText(self, "Edit Connection", "Connection Name:", text=current_name)
        if ok and new_name.strip():
            item.setText(0, new_name.strip())

    def open_connection(self, item, column):
        """
        Simulates opening a connection when a connection item is double-clicked.
        """
        item_type = item.data(0, Qt.UserRole)
        if item_type == 'connection':
            connection_name = item.text(0)
            self.right_pane.append(f"Connecting to {connection_name}...")
            # Simulate a successful connection
            self.right_pane.append("Connected successfully!\n")
        # If it's a folder, do nothing or implement expand/collapse behavior

