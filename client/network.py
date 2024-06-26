# client/network.py
# Network communication for the Battleship client.

import socket
import pickle
from logger import Logger


class ClientNetwork:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger = Logger(f"client_server_.log")

    def connect(self, port):
        self.socket.connect(port)
        self.logger.log_info(f"Connect to port: {port}")
        # TODO: Implement connection to the server.


    def send(self, data):
        # TODO: Implement sending data to the server.
        pass

    def receive(self):
        # TODO: Implement receiving data from the server.
        pass
