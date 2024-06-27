# server/logger.py
# Logger for the Battleship server.

import logging
import os


class ServerLogger:
    def __init__(self, log_file):
        self.loggers = {}

        self.log_file = log_file
        self.setup_logger('BattleshipServer')
        self.setup_logger('Network')
        self.setup_logger('PlayerManager')
        self.setup_logger('BattleshipServerGUI')
        self.setup_logger('GameLogic')

    def setup_logger(self, name):
        pwd = os.getcwd()
        cwd = os.path.join(pwd, 'logs')
        print(f'Current working directory is: {cwd}')

        if not cwd:
            os.makedirs(cwd)
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        if not logger.handlers:
            fh = logging.FileHandler(self.log_file)
            fh.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            logger.addHandler(fh)
            logger.addHandler(ch)
        
        self.loggers[name] = logger

    def get_logger(self, name):
        return self.loggers.get(name, None)

    def log_info(self, name, message):
        logger = self.get_logger(name)
        if logger:
            logger.info(message)

    def log_error(self, name, message):
        logger = self.get_logger(name)
        if logger:
            logger.error(message)

    def log_warning(self, name, message):
        logger = self.get_logger(name)
        if logger:
            logger.warning(message)

    # TODO: Add methods for logging various events and actions.
