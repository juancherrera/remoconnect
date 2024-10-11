# main.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QListWidget, QTextEdit,
    QWidget, QHBoxLayout, QMenu, QAction, QInputDialog, QListWidgetItem
)
from PyQt5.QtCore import Qt, QPoint

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

    def show_context_menu(self, position):
        menu = QMenu()

        add_folder_action = QAction("Add Folder", self)
        add_folder_action.triggered.connect(self.add_folder)
        menu.addAction(add_folder_action)

        add_connection_action = QAction("Add Connection", self)
        add_connection_action.triggered.connect(self.add_connection)
        menu.addAction(add_connection_action)

        # Show the context menu at the cursor position
        menu.exec_(self.left_pane.viewport().mapToGlobal(position))

    def add_folder(self):
        folder_name, ok = QInputDialog.getText(self, "Add Folder", "Folder Name:")
        if ok and folder_name:
            item = QListWidgetItem(folder_name)
            item.setData(Qt.UserRole, {'type': 'folder'})
            self.left_pane.addItem(item)

    def add_connection(self):
        connection_name, ok = QInputDialog.getText(self, "Add Connection", "Connection Name:")
        if ok and connection_name:
            item = QListWidgetItem(connection_name)
            item.setData(Qt.UserRole, {'type': 'connection'})
            self.left_pane.addItem(item)

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
