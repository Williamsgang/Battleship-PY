# client/client.py
# Main client logic for the Battleship game.
import pickle
import socket
import time

from adhd_version.config import settings
from adhd_version.logs import logger
from adhd_version.networking import network
from adhd_version.networking.events import EventHandler
from adhd_version.shared.board_ships_players import Board, Ships
from adhd_version.screens.client_gui import GUI


class BattleshipClient1:
    def __init__(self):
        self.log = logger.Logger(self.__class__.__name__)
        self.running = False
        self.host_port = (settings.get_server_host(), settings.get_server_port())
        self.s = None
        self.net = network.Network(self.host_port, is_server=False)
        self.board_size = None
        self.board = None
        self.ships = None
        self.event_handler = EventHandler()
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
            self.log.log_warning('start_client', f'Connection attempt {i + 1} failed')
            time.sleep(2)

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
                self.board_size = game_state['board_size']
                self.board = Board()
                self.board.board = game_state['board']
                self.ships = Ships()
                self.ships.ships = game_state['ships']
                self.log.log_info('start_client', 'Game state received from the server')
            else:
                self.log.log_warning('start_client', 'No initial game state received from the server')

            self.gui_setup()
        except socket.error as se:
            self.event_handler.handle_socket_error_event(se)
        finally:
            self.log.log_info('start_client', 'Client disconnecting from the server...')
            self.net.disconnect()
            self.running = False
            self.log.log_info('start_client', 'Client stopped')

    def gui_setup(self):
        self.log.log_info('gui_setup', 'Setting up GUI...')
        gui = GUI()
        gui.main_loop()


if __name__ == "__main__":
    client = BattleshipClient()
    client.start_client()
