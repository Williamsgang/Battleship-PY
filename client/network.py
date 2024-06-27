# client/network.py
# Network communication for the Battleship client.

import socket
import pickle
from .logger import ClientLogger


class ClientNetwork:
    def __init__(self, host, port):
        self.logger_name_reference = 'ClientNetwork'
        self.ip = self.get_ip_address()
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger = ClientLogger(f'client_network.log')

    def connect(self, host, port):
        try:
            self.socket.connect((host, port))
            self.logger.log_info(self.logger_name_reference + '.connect()',
                                 f"Connect to port: {port}")
        except BrokenPipeError as bpe:
            self.logger.log_error(self.logger_name_reference + '.connect()',
                                  f"BrokenPipeError occurred: {bpe}")
        except socket.error as e:
            self.logger.log_error(self.logger_name_reference + '.connect()',
                                  f"Did not connect to port, {port}. "
                                  f"Error occurred: {e}")

        # TODO: Implement connection to the server.

    def send(self, data):
        try:
            self.socket.sendall(data)
            self.logger.log_info(self.logger_name_reference + '.send()',
                                 f"Sent information to the server")
        except BrokenPipeError as bpe:
            self.logger.log_error(self.logger_name_reference + '.send()',
                                  f"BrokenPipeError occurred: {bpe}")
        except socket.error as e:
            self.logger.log_error(self.logger_name_reference + '.send()',
                                  f"Did not send information to the server. Error occurred {e}")

        # TODO: Implement sending data to the server.

    def receive(self):
        try:
            self.socket.recv(1024)
            self.logger.log_info(self.logger_name_reference + '.receive()',
                                 f"Received information from the server")
        except BrokenPipeError as bpe:
            self.logger.log_error(self.logger_name_reference + '.receive()',
                                  f"BrokenPipeError occurred: {bpe}")
        except socket.error as e:
            self.logger.log_error(self.logger_name_reference + '.receive()',
                                  f"Did not receive information from the server. Error occurred: {e}")

        # TODO: Implement receiving data from the server.

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            # Connect to a public DNS server
            s.connect(('8.8.8.8', 80))

            # Get the IP address of the socket
            ip_address = s.getsockname()
            self.logger.log_info(self.logger_name_reference + '.get_ip_address()',
                                 f'IP Address: {ip_address}')
        except BrokenPipeError as bpe:
            self.logger.log_error(self.logger_name_reference + '.receive()',
                                  f"BrokenPipeError occurred: {bpe}")
        except socket.error as e:
            self.logger.log_error(self.logger_name_reference + '.receive()',
                                  f"Error occurred: {e}")
        finally:
            # Close the socket
            s.close()
        return ip_address
