# gui/main_window.py

from PyQt5.QtWidgets import (
    QMainWindow, QSplitter, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget,
    QPlainTextEdit, QMenu, QAction, QColorDialog, QMessageBox, QInputDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from gui.connection_config import ConnectionConfigDialog
from gui.customizations import Customizations
from connections.ssh_connection import SSHConnectionManager
from connections.rdp_connection import RDPConnectionManager
from utils.settings_manager import SettingsManager
import webbrowser

class MainWindow(QMainWindow):
    def __init__(self, log_manager, settings_manager):
        super().__init__()

        self.log_manager = log_manager
        self.settings_manager = settings_manager

        self.setWindowTitle("Connection Manager")
        self.setGeometry(100, 100, 1200, 800)

        self.customizations = Customizations(self.settings_manager)
        self.apply_customizations()

        self.splitter = QSplitter(Qt.Horizontal)

        # Left pane: Tree widget for folders and connections
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.tree_widget.itemDoubleClicked.connect(self.open_connection)
        self.tree_widget.setToolTipDuration(5000)
        self.load_connections()

        self.splitter.addWidget(self.tree_widget)

        # Right pane: Terminal/Connection area
        self.terminal_area = QPlainTextEdit()
        self.terminal_area.setReadOnly(True)
        self.terminal_area.setFont(QFont('Courier', 10))
        # Set default background and font colors
        bg_color = self.customizations.get_background_color()
        font_color = self.customizations.get_font_color()
        self.terminal_area.setStyleSheet(f"background-color: {bg_color}; color: {font_color};")

        self.splitter.addWidget(self.terminal_area)

        layout = QVBoxLayout()
        layout.addWidget(self.splitter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.create_menus()

    def apply_customizations(self):
        # Apply background and font color customizations
        bg_color = self.customizations.get_background_color()
        font_color = self.customizations.get_font_color()
        self.setStyleSheet(f"background-color: {bg_color}; color: {font_color};")

    def create_menus(self):
        # Create menu bar and actions
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        help_menu = menu_bar.addMenu('Help')

        customize_action = QAction('Customize Appearance', self)
        customize_action.triggered.connect(self.customize_appearance)
        file_menu.addAction(customize_action)

        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def show_context_menu(self, position):
        selected_item = self.tree_widget.itemAt(position)
        menu = QMenu()

        add_folder_action = QAction("Add Folder", self)
        add_folder_action.triggered.connect(self.add_folder)
        menu.addAction(add_folder_action)

        add_connection_action = QAction("Add Connection", self)
        add_connection_action.triggered.connect(self.add_connection)
        menu.addAction(add_connection_action)

        if selected_item:
            edit_action = QAction("Edit", self)
            edit_action.triggered.connect(self.edit_item)
            menu.addAction(edit_action)

        menu.exec_(self.tree_widget.viewport().mapToGlobal(position))

    def add_folder(self):
        folder_name, ok = QInputDialog.getText(self, "New Folder", "Enter folder name:")
        if ok and folder_name:
            folder_item = QTreeWidgetItem([folder_name])
            folder_item.setData(0, Qt.UserRole, {'type': 'folder', 'name': folder_name})
            self.tree_widget.addTopLevelItem(folder_item)
            self.log_manager.log('info', f"Folder added: {folder_name}")
            # Save the folder to settings
            self.settings_manager.add_folder({'name': folder_name})

    def add_connection(self):
        selected_item = self.tree_widget.currentItem()
        dialog = ConnectionConfigDialog(self)
        if dialog.exec_() == dialog.Accepted:
            connection_data = dialog.get_connection_data()
            connection_item = QTreeWidgetItem([connection_data['name']])
            connection_item.setData(0, Qt.UserRole, connection_data)
            connection_item.setToolTip(0, self.get_connection_tooltip(connection_data))
            if selected_item and selected_item.data(0, Qt.UserRole)['type'] == 'folder':
                selected_item.addChild(connection_item)
            else:
                self.tree_widget.addTopLevelItem(connection_item)
            self.log_manager.log('info', f"Connection added: {connection_data['name']}")
            # Save the connection to settings
            self.settings_manager.add_connection(connection_data)

    def edit_item(self):
        selected_item = self.tree_widget.currentItem()
        if selected_item:
            data = selected_item.data(0, Qt.UserRole)
            if data['type'] == 'connection':
                # Edit connection
                dialog = ConnectionConfigDialog(self, data)
                if dialog.exec_() == dialog.Accepted:
                    connection_data = dialog.get_connection_data()
                    selected_item.setText(0, connection_data['name'])
                    selected_item.setData(0, Qt.UserRole, connection_data)
                    selected_item.setToolTip(0, self.get_connection_tooltip(connection_data))
                    self.log_manager.log('info', f"Connection edited: {connection_data['name']}")
                    # Update the connection in settings
                    self.settings_manager.update_connection(connection_data)
            elif data['type'] == 'folder':
                # Edit folder
                folder_name, ok = QInputDialog.getText(self, "Edit Folder", "Enter new folder name:", text=data['name'])
                if ok and folder_name:
                    selected_item.setText(0, folder_name)
                    data['name'] = folder_name
                    selected_item.setData(0, Qt.UserRole, data)
                    self.log_manager.log('info', f"Folder renamed to: {folder_name}")
                    # Update the folder in settings
                    self.settings_manager.update_folder(data)

    def customize_appearance(self):
        bg_color = QColorDialog.getColor().name()
        font_color = QColorDialog.getColor().name()
        self.customizations.set_background_color(bg_color)
        self.customizations.set_font_color(font_color)
        self.apply_customizations()

    def open_connection(self, item, column):
        data = item.data(0, Qt.UserRole)
        if data and data['type'] == 'connection':
            connection_type = data.get('connection_type')
            if connection_type == 'SSH':
                ssh_manager = SSHConnectionManager(
                    hostname=data['host'],
                    username=data['username'],
                    password=data['password'],
                    port=data.get('port', 22),
                    ssh_options=data.get('ssh_options', [])
                )
                if ssh_manager.connect():
                    self.terminal_area.appendPlainText(f"Connected to {data['host']}")
                    # Optionally open browser after SSH connection
                    if data.get('open_browser'):
                        self.open_browser()
                else:
                    self.terminal_area.appendPlainText(f"Failed to connect to {data['host']}")
            elif connection_type == 'RDP':
                rdp_manager = RDPConnectionManager(
                    hostname=data['host'],
                    username=data['username'],
                    password=data['password']
                )
                rdp_manager.connect()
        else:
            # It's a folder or has no data
            pass

    def load_connections(self):
        # Load connections and folders from settings
        items = self.settings_manager.get_all_items()
        for item_data in items:
            item = self.create_tree_item(item_data)
            self.tree_widget.addTopLevelItem(item)

    def create_tree_item(self, item_data):
        item = QTreeWidgetItem([item_data['name']])
        item.setData(0, Qt.UserRole, item_data)
        if item_data['type'] == 'connection':
            item.setToolTip(0, self.get_connection_tooltip(item_data))
        elif item_data['type'] == 'folder':
            for child_data in item_data.get('children', []):
                child_item = self.create_tree_item(child_data)
                item.addChild(child_item)
        return item

    def get_connection_tooltip(self, connection_data):
        tooltip = f"Host: {connection_data['host']}\n"
        tooltip += f"Username: {connection_data['username']}\n"
        tooltip += f"Type: {connection_data['connection_type']}\n"
        if connection_data['connection_type'] == 'SSH':
            tooltip += f"SSH Options: {' '.join(connection_data.get('ssh_options', []))}\n"
        return tooltip

    def open_browser(self):
        # Open default browser to localhost or specified URL
        webbrowser.open('http://localhost')

    def show_about_dialog(self):
        about_text = """
        <h2>Connection Manager</h2>
        <p>
        Version: 1.0.0<br>
        This software is licensed for personal, non-commercial use only.
        </p>
        """
        QMessageBox.about(self, "About Connection Manager", about_text)
