# networking/events.py
# Centralized event handling for the Battleship game.
import socket

from logs import logger
from server.game_logic import GameLogic
from shared import board_ships_players


class Events:
    def __init__(self):
        """
        Initialize the Events class.
        This class handles various game events such as creating boards, placing ships, and validating boards.
        """
        self.log = logger.Logger(self.__class__.__name__)
        self.board = board_ships_players.Board()
        self.ships = board_ships_players.Ships()
        self.players = board_ships_players.Players()
        self.game_logic = GameLogic()

    def board_create_event(self):
        """
        Create a new game board.
        """
        board_instance = self.board
        board = board_instance.create_board()
        self.log.log_info('board_create_event', 'Board created')
        return board

    def ships_create_event(self):
        """
        Create ships for the game.
        """
        ships = self.ships
        ships.create_ships()
        self.log.log_info('ships_create_event', 'Ships created')
        return ships

    def game_board_event(self):
        """
        Place ships on the game board.
        """
        board = self.board
        board.place_ships(self.players.ships)
        self.log.log_info('game_board_event', 'Game board created and ships placed')
        return board

    def board_validation_event(self, server_board, client_board):
        """
        Validate the board by comparing the server's board with the client's board.
        """
        if server_board.board == client_board.board:
            self.log.log_info('board_validation', 'Boards are synchronized and valid.')
            print("Boards are synchronized and valid.")
        else:
            self.log.log_warning('board_validation', 'Boards are not synchronized. Potential cheating detected!')
            print("Boards are not synchronized. Potential cheating detected!")

    def get_players_event(self):
        """
        Retrieve player information.
        """
        player = board_ships_players.Players()
        return player

    def shoot_event(self, player_index, x, y):
        """
        Handle the shoot event.
        """
        result = self.game_logic.shoot(player_index, x, y)
        self.log.log_info('shoot_event', f'Shoot result: {result}')
        return result


class EventHandler:
    def __init__(self):
        """
        Initialize the EventHandler class.
        This class handles various events like connections, disconnections, and game start.
        """
        self.log = logger.Logger(self.__class__.__name__)
        self.server_address = None
        self.client_address = None

    def handle_event(self, event, server):
        """
        Handle different types of events.
        """
        self.log.log_info('handle_event', f'Handling event: {event}')
        if event == 'connection':
            self.handle_connection(server)
        elif event == 'disconnection':
            self.handle_disconnection(server)
        elif event == 'socket_error':
            self.handle_socket_error_event(event)
        elif event == 'server_close':
            self.handle_server_close_event()
        elif event == 'game_start':
            self.game_start()
        else:
            self.log.log_warning('handle_event', f'Unhandled event type: {event}')

    def handle_connection(self, server):
        """
        Handle a new connection event.
        """
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

    def handle_disconnection(self, server):
        """
        Handle a disconnection event.
        """
        self.log.log_info('handle_disconnection', 'Client disconnected')
        self.server_address = None
        self.client_address = None
        server.conn.close()
        self.log.log_info('handle_disconnection', 'Connection closed')

    def handle_socket_error_event(self, error):
        """
        Handle a socket error event.
        """
        self.log.log_error('handle_socket_error_event', f'Socket error: {error}')
        # Implement socket error handling logic here
        try:
            # Attempt to close the connection
            error.conn.close()
        except socket.error as se:
            self.log.log_error('handle_socket_error_event', f'Error closing socket: {se}')

    def handle_server_close_event(self):
        """
        Handle the server close event.
        """
        self.log.log_info('handle_server_close_event', 'Server has shut down')
        # Implement server shutdown handling logic here
        try:
            # Attempt to close the server socket
            pass
        except socket.error as se:
            self.log.log_error('handle_server_close_event', f'Error closing server socket: {se}')

    def game_start(self):
        """
        Start the game by creating the game board and ships.
        """
        self.log.log_info('game_start', 'Starting game...')
        events = Events()
        board = events.board_create_event()
        ships = events.ships_create_event()
        game_board = events.game_board_event()
        self.log.log_info('game_start', 'Game board and ships created')
        # Implement further game start logic

    def handle_receive_data(self, client, received_data):
        """
        Handle data received from the server.
        """
        if received_data:
            self.log.log_info('handle_receive_data', f'Information received: {received_data}')
            print(f'Received data from the server: {received_data}')
        else:
            self.log.log_warning('handle_receive_data', 'No data received, connection might be closed')
            client.running = False

    def handle_send_data(self, client, data):
        """
        Handle sending data to the server.
        """
        try:
            client.net.send_data(client.s, data)
            self.log.log_info('handle_send_data', f'Sent data to server: {data}')
        except socket.error as se:
            self.log.log_error('handle_send_data', f'Socket error on send: {se}')
            client.running = False

    def handle_game_shot(self, client, x, y):
        """
        Handle the shooting logic from the client.
        """
        try:
            result = client.game_logic.shoot(client.player_index, x, y)
            self.log.log_info('handle_game_shot', f'Shot result: {result}')
            client.net.send_data(client.s, f'Shot: {x},{y} Result: {result}'.encode())
        except socket.error as se:
            self.log.log_error('handle_game_shot', f'Socket error on send: {se}')
            client.running = False
