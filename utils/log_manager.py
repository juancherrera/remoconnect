import logging
from logging.handlers import TimedRotatingFileHandler
import os

class LogManager:
    def __init__(self, log_file='logs/app.log', when="D", interval=1, backup_count=7):
        if not os.path.exists('logs'):
            os.makedirs('logs')
        self.logger = logging.getLogger("ConnectionManager")
        self.logger.setLevel(logging.DEBUG)
        handler = TimedRotatingFileHandler(
            log_file, when=when, interval=interval, backupCount=backup_count
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log(self, level, message):
        if level == 'info':
            self.logger.info(message)
        elif level == 'error':
            self.logger.error(message)
        else:
            self.logger.debug(message)
