# main.py

import sys
import subprocess

REQUIRED_PACKAGES = ['PyQt5==5.15.6', 'paramiko==2.11.0', 'pywinrm==0.4.2']

def install_missing_packages(missing_packages):
    try:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
        print("Installation complete. Please restart the application.")
        sys.exit(0)
    except Exception as e:
        print(f"Failed to install packages: {e}")
        sys.exit(1)

def check_and_install_packages():
    missing_packages = []
    for package in REQUIRED_PACKAGES:
        package_name = package.split('==')[0]
        try:
            __import__(package_name)
        except ImportError:
            missing_packages.append(package)
    if missing_packages:
        print(f"The following packages are missing: {', '.join(missing_packages)}")
        install_missing_packages(missing_packages)

# Check and install packages before importing other modules
check_and_install_packages()

from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from gui.license_dialog import LicenseDialog
from utils.log_manager import LogManager
from utils.settings_manager import SettingsManager

def main():
    # Initialize the log manager
    log_manager = LogManager()

    # Initialize the settings manager
    settings_manager = SettingsManager()

    # Create the application
    app = QApplication([])

    # Set application name and icon for macOS dock
    app.setApplicationName("Connection Manager")
    app.setWindowIcon(None)  # You can set an icon file here if you have one

    # Check if the license has been accepted
    if not settings_manager.get_setting('license_accepted', False):
        license_dialog = LicenseDialog()
        if license_dialog.exec_() == license_dialog.Accepted:
            settings_manager.update_setting('license_accepted', True)
        else:
            # User declined the license agreement
            return  # Exit the application

    # Create and show the main window
    main_window = MainWindow(log_manager, settings_manager)
    main_window.show()

    # Start the application event loop
    log_manager.log('info', 'Application started')
    app.exec_()

if __name__ == "__main__":
    main()
