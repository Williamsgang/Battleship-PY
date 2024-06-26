# server/logger.py
# Logger for the Battleship server.

import logging

class Logger:
    def __init__(self, log_file):
        self.logger = logging.getLogger('BattleshipServer')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def log(self, message):
        self.logger.info(message)

    # TODO: Add methods for logging various events and actions.
