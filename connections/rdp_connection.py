import subprocess

class RDPConnectionManager:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

    def connect(self):
        try:
            command = [
                'open',
                f'rdp://{self.username}:{self.password}@{self.hostname}'
            ]
            subprocess.Popen(command)
        except Exception as e:
            print(f"RDP connection failed: {e}")
