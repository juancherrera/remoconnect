from PyQt5.QtWidgets import (
    QMainWindow, QSplitter, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget,
    QPlainTextEdit, QMenu, QAction, QColorDialog, QFileDialog
)
from PyQt5.QtCore import Qt
from gui.connection_config import ConnectionConfigDialog
from gui.customizations import Customizations
from connections.ssh_connection import SSHConnectionManager
from connections.rdp_connection import RDPConnectionManager

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

        # Left pane: Folder/connection tree
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
        self.terminal_area.setStyleSheet("background-color: black; color: green;")
        self.splitter.addWidget(self.terminal_area)

        layout = QVBoxLayout()
        layout.addWidget(self.splitter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def apply_customizations(self):
        bg_color = self.customizations.get_background_color()
        font_color = self.customizations.get_font_color()
        self.setStyleSheet(f"background-color: {bg_color}; color: {font_color};")

    def show_context_menu(self, position):
        menu = QMenu()
        add_folder_action = QAction("Add Folder", self)
        add_folder_action.triggered.connect(self.add_folder)
        add_connection_action = QAction("Add Connection", self)
        add_connection_action.triggered.connect(self.add_connection)
        edit_action = QAction("Edit", self)
        edit_action.triggered.connect(self.edit_item)
        customize_action = QAction("Customize Appearance", self)
        customize_action.triggered.connect(self.customize_appearance)

        menu.addAction(add_folder_action)
        menu.addAction(add_connection_action)
        menu.addAction(edit_action)
        menu.addSeparator()
        menu.addAction(customize_action)
        menu.exec_(self.tree_widget.viewport().mapToGlobal(position))

    def add_folder(self):
        folder_name, ok = QFileDialog.getSaveFileName(self, "New Folder", "", "Folder (*)")
        if ok and folder_name:
            folder_item = QTreeWidgetItem([folder_name])
            self.tree_widget.addTopLevelItem(folder_item)
            self.log_manager.log('info', f"Folder added: {folder_name}")
            # Save the folder to settings
            self.settings_manager.add_folder(folder_name)

    def add_connection(self):
        selected_item = self.tree_widget.currentItem()
        dialog = ConnectionConfigDialog(self)
        if dialog.exec_() == dialog.Accepted:
            connection_data = dialog.get_connection_data()
            connection_item = QTreeWidgetItem([connection_data['name']])
            connection_item.setData(0, Qt.UserRole, connection_data)
            connection_item.setToolTip(0, str(connection_data))
            if selected_item:
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
            if data:
                # It's a connection
                dialog = ConnectionConfigDialog(self, data)
                if dialog.exec_() == dialog.Accepted:
                    connection_data = dialog.get_connection_data()
                    selected_item.setText(0, connection_data['name'])
                    selected_item.setData(0, Qt.UserRole, connection_data)
                    selected_item.setToolTip(0, str(connection_data))
                    self.log_manager.log('info', f"Connection edited: {connection_data['name']}")
                    # Update the connection in settings
                    self.settings_manager.update_connection(connection_data)
            else:
                # It's a folder
                folder_name, ok = QFileDialog.getSaveFileName(self, "Edit Folder", "", "Folder (*)")
                if ok and folder_name:
                    selected_item.setText(0, folder_name)
                    self.log_manager.log('info', f"Folder renamed to: {folder_name}")
                    # Update the folder in settings
                    self.settings_manager.update_folder(selected_item.text(0), folder_name)

    def customize_appearance(self):
        bg_color = QColorDialog.getColor().name()
        font_color = QColorDialog.getColor().name()
        self.customizations.set_background_color(bg_color)
        self.customizations.set_font_color(font_color)
        self.apply_customizations()

    def open_connection(self, item, column):
        data = item.data(0, Qt.UserRole)
        if data:
            connection_type = data.get('type')
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
        connections = self.settings_manager.get_all_connections()
        for conn in connections:
            connection_item = QTreeWidgetItem([conn['name']])
            connection_item.setData(0, Qt.UserRole, conn)
            connection_item.setToolTip(0, str(conn))
            self.tree_widget.addTopLevelItem(connection_item)

    def open_browser(self):
        import webbrowser
        webbrowser.open('http://localhost')

