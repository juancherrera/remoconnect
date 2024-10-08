# utils/settings_manager.py

import json
import os

class SettingsManager:
    def __init__(self, settings_file='app_settings.json'):
        self.settings_file = settings_file
        self.settings = {}
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = {
                'connections': [],
                'folders': [],
                'background_color': '#000000',
                'font_color': '#00FF00',
                'license_accepted': False  # Add default license status
            }

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def update_setting(self, key, value):
        self.settings[key] = value
        self.save_settings()

    def get_setting(self, key, default=None):
        return self.settings.get(key, default)

    # Existing methods for managing connections and folders...
