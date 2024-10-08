import paramiko
import threading
import subprocess

class SSHConnectionManager:
    def __init__(self, hostname, username, password, port=22, ssh_options=None):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.ssh_options = ssh_options if ssh_options else []
        self.client = None

    def connect(self):
        command = [
            'ssh',
            f'{self.username}@{self.hostname}',
            '-p', str(self.port)
        ] + self.ssh_options
        try:
            subprocess.Popen(command)
            return True
        except Exception as e:
            print(f"SSH connection failed: {e}")
            return False
