# server/network.py
# Network communication for the Battleship server.

import socket
import threading
from .logger import Logger

class Network:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger = Logger("server_logs.log")

    def start_server(self, client_handler):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Client {client_address} connected.")
            threading.Thread(target=client_handler, args=(client_socket,)).start()

    def send(self, client_socket, data):
        # TODO: Implement sending data to a client.
        pass

    def receive(self, client_socket):
        # TODO: Implement receiving data from a client.
        pass
