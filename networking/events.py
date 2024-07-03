# networking/events.py
# Centralized event handling for the Battleship game.
import socket

from logs import logger
from shared import board_ships_players


class Events:
    def __init__(self):
        self.log = logger.Logger(self.__class__.__name__)
        self.board = board_ships_players.Board()
        self.ships = board_ships_players.Ships()
        self.players = board_ships_players.Players()

    def board_create_event(self):
        board_instance = self.board
        board = board_instance.create_board()
        self.log.log_info('board_create_event', 'Board created')
        return board

    def ships_create_event(self):
        ships = self.ships
        ships.create_ships()
        self.log.log_info('ships_create_event', 'Ships created')
        return ships

    def game_board_event(self):
        board = self.board
        board.place_ships(self.players.ships)
        self.log.log_info('game_board_event', 'Game board created and ships placed')
        return board

    def board_validation_event(self, server_board, client_board):
        if server_board.board == client_board.board:
            self.log.log_info('board_validation', 'Boards are synchronized and valid.')
            print("Boards are synchronized and valid.")
        else:
            self.log.log_warning('board_validation', 'Boards are not synchronized. Potential cheating detected!')
            print("Boards are not synchronized. Potential cheating detected!")

    def get_players_event(self):
        player = board_ships_players.Players()
        return player


class EventHandler:
    def __init__(self):
        self.log = logger.Logger(self.__class__.__name__)
        self.server_address = None
        self.client_address = None

    def handle_event(self, event, server):
        self.log.log_info('handle_event', f'Handling event: {event}')
        if event == 'connection':
            self.handle_connection(event, server)
        elif event == 'disconnection':
            self.handle_disconnection(event, server)
        elif event == 'socket_error':
            self.handle_socket_error_event(event)
        elif event == 'server_close':
            self.handle_server_close_event()
        elif event == 'game_start':
            self.game_start()
        else:
            self.log.log_warning('handle_event', f'Unhandled event type: {event}')

    def handle_connection(self, event, server):
        self.log.log_info('handle_connection', 'New connection established')
        self.server_address = server.server_address
        self.client_address = server.client_address
        self.log.log_info('handle_connection',
                          f'Server address: {self.server_address}, Client address: {self.client_address}')
        # Send acknowledgment to client
        try:
            server.conn.sendall(b'Connection established')
            self.log.log_info('handle_connection', 'Acknowledgment sent to client')
        except socket.error as se:
            self.log.log_error('handle_connection', f'Error sending acknowledgment: {se}')

    def handle_disconnection(self, event, server):
        self.log.log_info('handle_disconnection', 'Client disconnected')
        self.server_address = None
        self.client_address = None
        server.conn.close()
        self.log.log_info('handle_disconnection', 'Connection closed')

    def handle_socket_error_event(self, error):
        self.log.log_error('handle_socket_error_event', f'Socket error: {error}')
        # Implement socket error handling logic here
        try:
            # Attempt to close the connection
            error.conn.close()
        except socket.error as se:
            self.log.log_error('handle_socket_error_event', f'Error closing socket: {se}')

    def handle_server_close_event(self):
        self.log.log_info('handle_server_close_event', 'Server has shut down')
        # Implement server shutdown handling logic here
        try:
            # Attempt to close the server socket
            pass
        except socket.error as se:
            self.log.log_error('handle_server_close_event', f'Error closing server socket: {se}')

    def game_start(self):
        self.log.log_info('game_start', 'Starting game...')
        events = Events()
        board = events.board_create_event()
        ships = events.ships_create_event()
        game_board = events.game_board_event()
        self.log.log_info('game_start', 'Game board and ships created')
        # Implement further game start logic

    def handle_receive_data(self, client, received_data):
        if received_data:
            self.log.log_info('handle_receive_data', f'Information received: {received_data}')
            print(f'Received data from the server: {received_data}')
        else:
            self.log.log_warning('handle_receive_data', 'No data received, connection might be closed')
            client.running = False

    def handle_send_data(self, client, data):
        try:
            client.net.send_data(client.s, data)
            self.log.log_info('handle_send_data', f'Sent data to server: {data}')
        except socket.error as se:
            self.log.log_error('handle_send_data', f'Socket error on send: {se}')
            client.running = False
