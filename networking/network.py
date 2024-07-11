# networking/network.py
from typing import Tuple

from log.logger import Logger


class Network:
    def __init__(self, host_port: Tuple[str, int], is_server=False):
        self.log = Logger(self.__class__.__name__)
        self.host_port = host_port
