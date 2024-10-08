import json
import os

class ConnectionManager:
    def __init__(self, connections_file='connections.json'):
        self.connections_file = connections_file
        self.connections = []
        self.load_connections()

    def load_connections(self):
        if os.path.exists(self.connections_file):
            with open(self.connections_file, 'r') as f:
                self.connections = json.load(f)
        else:
            self.connections = []

    def save_connections(self):
        with open(self.connections_file, 'w') as f:
            json.dump(self.connections, f, indent=4)

    def add_folder(self, folder_name):
        folder = {'name': folder_name, 'type': 'folder', 'children': []}
        self.connections.append(folder)
        self.save_connections()

    def add_connection(self, connection_details):
        connection = {
            'name': connection_details['name'],
            'type': 'connection',
            'details': connection_details
        }
        # Add to the current folder (in a real app, you'd track which folder is selected)
        if self.connections:
            self.connections[-1]['children'].append(connection)
        self.save_connections()
