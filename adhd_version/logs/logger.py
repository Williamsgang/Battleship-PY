# logs/log.py
# Logs all information that goes on

import logging
import os


class Logger:
    def __init__(self, class_name):
        self.class_name = class_name
        log_directory = os.path.join(os.path.dirname(__file__), 'logs')
        os.makedirs(log_directory, exist_ok=True)
        self.log_file = os.path.join(log_directory, f"{self.class_name}.log")
        self.setup_logger()

    def setup_logger(self):
        self.logger = logging.getLogger(self.class_name)
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            fh = logging.FileHandler(self.log_file)
            fh.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger

    def log_info(self, method_name, message):
        self.logger.info(f'{self.class_name}.{method_name} - {message}')

    def log_error(self, method_name, message):
        self.logger.error(f'{self.class_name}.{method_name} - {message}')

    def log_warning(self, method_name, message):
        self.logger.warning(f'{self.class_name}.{method_name} - {message}')
