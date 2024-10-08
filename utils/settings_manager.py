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
                'font_color': '#00FF00'
            }

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def update_setting(self, key, value):
        self.settings[key] = value
        self.save_settings()

    def get_setting(self, key, default=None):
        return self.settings.get(key, default)

    def add_connection(self, connection_data):
        self.settings['connections'].append(connection_data)
        self.save_settings()

    def update_connection(self, connection_data):
        for i, conn in enumerate(self.settings['connections']):
            if conn['name'] == connection_data['name']:
                self.settings['connections'][i] = connection_data
                break
        self.save_settings()

    def get_all_connections(self):
        return self.settings.get('connections', [])

    def add_folder(self, folder_name):
        self.settings['folders'].append(folder_name)
        self.save_settings()

    def update_folder(self, old_name, new_name):
        folders = self.settings.get('folders', [])
        if old_name in folders:
            index = folders.index(old_name)
            folders[index] = new_name
            self.save_settings()
