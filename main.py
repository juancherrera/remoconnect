# main.py

import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from gui.license_dialog import LicenseDialog
from utils.settings_manager import SettingsManager

def main():
    # Initialize the settings manager
    settings_manager = SettingsManager()

    # Create the application
    app = QApplication(sys.argv)
    app.setApplicationName("Connection Manager")
    app.setWindowIcon(None)  # Set an icon if you have one

    # Check if the license has been accepted
    if not settings_manager.get_setting('license_accepted', False):
        license_dialog = LicenseDialog()
        if license_dialog.exec_() == license_dialog.Accepted:
            settings_manager.update_setting('license_accepted', True)
        else:
            # User declined the license agreement
            return  # Exit the application

    # Create and show the main window
    main_window = MainWindow()
    main_window.show()

    # Start the application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
