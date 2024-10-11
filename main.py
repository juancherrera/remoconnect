# main.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QTreeWidget, QTreeWidgetItem,
    QTextEdit, QWidget, QHBoxLayout, QMenu, QAction, QInputDialog
)
from PyQt5.QtGui import QIcon
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

        # Load icons
        self.folder_icon = QIcon.fromTheme("folder")  # Use a standard folder icon
        self.connection_icon = QIcon.fromTheme("network-workgroup")  # Use a standard network icon

    def show_context_menu(self, position):
        menu = QMenu()

        # Get the item at the clicked position
        selected_item = self.left_pane.itemAt(position)

        if selected_item:
            # Right-clicked on an item
            item_type = selected_item.data(0, Qt.UserRole)
            if item_type == 'folder':
                # Add Connection action
                add_connection_action = QAction("Add Connection", self)
                add_connection_action.triggered.connect(lambda: self.add_connection(selected_item))
                menu.addAction(add_connection_action)

                # Add Folder action
                add_folder_action = QAction("Add Folder", self)
                add_folder_action.triggered.connect(lambda: self.add_folder(selected_item))
                menu.addAction(add_folder_action)

                # Edit action
                edit_action = QAction("Edit Folder", self)
                edit_action.triggered.connect(lambda: self.edit_folder(selected_item))
                menu.addAction(edit_action)
            elif item_type == 'connection':
                # Edit action
                edit_action = QAction("Edit Connection", self)
                edit_action.triggered.connect(lambda: self.edit_connection(selected_item))
                menu.addAction(edit_action)
        else:
            # Right-clicked on empty space (root level)
            # Add Folder action
            add_folder_action = QAction("Add Folder", self)
            add_folder_action.triggered.connect(lambda: self.add_folder(None))
            menu.addAction(add_folder_action)

        # Show the context menu at the cursor position
        menu.exec_(self.left_pane.viewport().mapToGlobal(position))

    def add_folder(self, parent_item):
        folder_name, ok = QInputDialog.getText(self, "Add Folder", "Folder Name:")
        if ok and folder_name:
            item = QTreeWidgetItem([folder_name])
            item.setIcon(0, self.folder_icon)
            item.setData(0, Qt.UserRole, 'folder')
            if parent_item:
                parent_item.addChild(item)
            else:
                self.left_pane.addTopLevelItem(item)

    def add_connection(self, parent_item):
        if not parent_item or parent_item.data(0, Qt.UserRole) != 'folder':
            return  # Connections can only be added under folders

        connection_name, ok = QInputDialog.getText(self, "Add Connection", "Connection Name:")
        if ok and connection_name:
            item = QTreeWidgetItem([connection_name])
            item.setIcon(0, self.connection_icon)
            item.setData(0, Qt.UserRole, 'connection')
            parent_item.addChild(item)

    def edit_folder(self, item):
        folder_name, ok = QInputDialog.getText(self, "Edit Folder", "Folder Name:", text=item.text(0))
        if ok and folder_name:
            item.setText(0, folder_name)

    def edit_connection(self, item):
        connection_name, ok = QInputDialog.getText(self, "Edit Connection", "Connection Name:", text=item.text(0))
        if ok and connection_name:
            item.setText(0, connection_name)

    def open_connection(self, item, column):
        item_type = item.data(0, Qt.UserRole)
        if item_type == 'connection':
            connection_name = item.text(0)
            # Simulate connecting
            self.right_pane.append(f"Connecting to {connection_name}...")
            self.right_pane.append("Connected successfully!\n")
        else:
            # Do nothing on folder double-click or implement expand/collapse if desired
            pass

def main():
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
