# client/client.py
# Main client logic for the Battleship game.

import socket
from logs import logger
from networking import network

class BattleshipClient:
    def __init__(self):
        self.running = False
        self.host = '127.0.0.1'
        self.port = 65432
        self.log = logger.Logger(self.__class__.__name__)
        self.net = network.Network(self.host, self.port, is_server=False)
        self.s = None
        self.log.log_info('__init__', 'Client initialized')

    def start_client(self):
        self.running = True
        self.log.log_info('start_client', 'Starting client...')
        self.s = self.net.connect()

        if not self.s:
            self.log.log_error('start_client', 'Failed to connect to the server')
            return

        try:
            while self.running:
                try:
                    received_data = self.net.receive_data(self.s)
                    if received_data:
                        print(f'Received data from the server: {received_data}')
                        self.log.log_info('start_client', f'Information received: {received_data}')
                    else:
                        self.log.log_warning('start_client', 'No data received, connection might be closed')
                        break
                except socket.error as se:
                    self.log.log_error('start_client', f'Socket error on receive: {se}')
                    break

                try:
                    self.net.send_data(self.s, b'Hello from client')
                    self.log.log_info('start_client', 'Sent data to server: Hello from client')
                except socket.error as se:
                    self.log.log_error('start_client', f'Socket error on send: {se}')
                    break
        except socket.error as se:
            self.log.log_error('start_client', f'Socket error: {se}')
        finally:
            self.log.log_info('start_client', 'Client disconnecting from the server...')
            self.net.disconnect()
            self.running = False
            self.log.log_info('start_client', 'Client stopped')


    # TODO: Add methods for handling network communication, game logic, etc.

if __name__ == "__main__":
    client = BattleshipClient()
    client.start_client()
