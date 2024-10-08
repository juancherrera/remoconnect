from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
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

    # Create and show the main window
    main_window = MainWindow(log_manager, settings_manager)
    main_window.show()

    # Start the application event loop
    log_manager.log('info', 'Application started')
    app.exec_()

if __name__ == "__main__":
    main()
