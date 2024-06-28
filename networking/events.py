# networking/events.py
# Centralized event handling for the Battleship game.
import socket

from logs import logger
from shared import board, ships


class Events:
    def __init__(self):
        self.log = logger.Logger(self.__class__.__name__)
        self.board = board.Board()
        self.ships = ships.Ships()

    def board_create_event(self):
        board_instance = self.board
        board = board_instance.create_board()
        self.log.log_info('board_create_event', f'Board created')
        return board

    def ships_create_event(self):
        ships_instance = self.ships
        self.log.log_info('ships_create_event', f'Ships created')
        return ships_instance

    def game_board_event(self):
        return NotImplementedError


class EventHandler:
    def __init__(self):
        self.log = logger.Logger(self.__class__.__name__)
        self.server_address = None
        self.client_address = None

    def handle_event(self, event, server):
        # TODO: Implement this
        pass

    def handle_connection(self, event, server):
        # Handle new connection
        self.log.log_info('handle_connection', f'New connection from {event.client_address}')
        # TODO: Add connection logic here

    def handle_disconnection(self, event, server):
        # Handle disconnection
        self.log.log_info('handle_disconnection', f'Client disconnected: {event.client_address}')
        # TODO: Add disconnection logic here

    def handle_socket_error_event(self):
        # Handle socket disconnection
        self.log.log_info('handle_socked_error_event', f'Connection failed due to a socket error {socket.error}')
        # TODO: Add disconnection logic here

    def game_start(self):
        events = Events()

        board = events.board_create_event()
