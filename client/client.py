# client/client.py
# Main client logic for the Battleship game.
import errno
import pickle
import socket

from config import settings
from logs import logger
from networking import network
from shared import board, ships


class BattleshipClient:
    def __init__(self):
        self.running = False
        self.host_port = (settings.get_server_host(), settings.get_server_port())
        self.log = logger.Logger(self.__class__.__name__)
        self.s = None
        self.net = network.Network(self.host_port, is_server=False)
        self.board = None
        self.ships = None
        self.log.log_info('__init__', 'Client initialized')

    def start_client(self):
        self.running = True
        self.log.log_info('start_client', 'Starting client...')

        for i in range(5):
            self.log.log_info('start_client', f'Attempt {i + 1} to connect to {self.host_port}')
            self.s = self.net.connect()
            if self.s:
                self.log.log_info('start_client', f'Successfully connected to {self.host_port} on attempt {i + 1}')
                break

        if not self.s:
            self.log.log_error('start_client', 'Failed to connect to the server')
            self.running = False
            return

        try:
            self.log.log_info('start_client', 'Receiving initial game state from the server...')

            # Receive the game state from the server
            game_state = self.net.receive_data(self.s)
            if game_state:
                game_state = pickle.loads(game_state)
                self.board = board.Board()
                self.board.board = game_state['board']
                self.ships = ships.Ships()
                self.ships.ships = game_state['ships']
                self.log.log_info('start_client', 'Game state received from the server')
            else:
                self.log.log_warning('start_client', 'No initial game state received from the server')

            while self.running:
                try:
                    self.log.log_info('start_client', 'Waiting to receive data from the server...')

                    received_data = self.net.receive_data(self.s)
                    if received_data:
                        self.log.log_info('start_client', f'Information received: {received_data}')
                        print(f'Received data from the server: {received_data}')
                    else:
                        self.log.log_warning('start_client', 'No data received, connection might be closed')
                        self.running = False
                        break

                except socket.error as se:
                    self.log.log_error('start_client', f'Socket error on receive: {se}')
                    if errno == errno.EHOSTDOWN:
                        self.log.log_info('start_client',
                                          'Server closed before client could disconnect. Disconnecting client...')
                        self.net.disconnect()
                        self.running = False
                    break

                try:
                    self.log.log_info('start_client', 'Sending data to the server...')
                    data = b'Hello from the client'
                    self.net.send_data(self.s, data)
                    self.log.log_info('start_client', f'Sent data to server: {data}')
                except socket.error as se:
                    self.log.log_error('start_client', f'Socket error on send: {se}')
                    self.running = False
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
