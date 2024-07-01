# server/server.py
# Main server logic for the Battleship game.
import pickle
import socket

from logs import logger
from networking import network
from shared import board, ships


class BattleshipServer:
    def __init__(self):
        self.running = True
        self.host_port = ("127.0.0.1", 65432)
        self.log = logger.Logger(self.__class__.__name__)
        self.net = network.Network(self.host_port, is_server=True)
        self.log.log_info('__init__', 'Server initialized')
        self.board = board.Board()
        self.ships = ships.Ships()
        self.board.create_board()
        self.board.place_ships()

        self.players = []

        # TODO: Add methods for handling game logic, client communication, etc.

    def start_server(self):
        self.log.log_info('start_server', 'Starting server...')
        self.net.accept_conn()
        print(f'Server started on {self.host_port[0]}:{self.host_port[1]}')
        self.log.log_info('start_server', f'Server started on {self.host_port[0]}:{self.host_port[1]}')

        while self.running:
            try:
                conn, addr = self.net.accept_conn()
                if conn is None:
                    self.log.log_warning('start_server', 'No connection accepted')
                    break
                print(f'Connected by {addr}')
                self.log.log_info('start_server', f'Connected by {addr}')

                # Send the game state to the client
                game_state = {
                    'board': self.board.board,
                    'ships': self.ships.ships
                }
                conn.sendall(pickle.dumps(game_state))

                while self.running:
                    try:
                        data = self.net.receive_data(conn)
                        if data:
                            print(f'Received data: {data}')
                            self.log.log_info('start_server', f'Received data: {data}')
                        else:
                            self.log.log_warning('start_server', 'No data received, connection might be closed')
                            break
                    except socket.error as se:
                        self.log.log_error('start_server', f'Socket error on receive: {se}')
                        break
            except socket.error as se:
                self.log.log_error('start_server', f'Socket error on accept: {se}')
                self.running = False

    def stop_server(self):
        self.log.log_info('stop_server', 'Stopping server...')
        self.net.disconnect()
        self.running = False
        self.log.log_info('stop_server', 'Server stopped')

    def handle_client(self, conn, addr):
        self.log.log_info('handle_client', f'Handling client {addr}')
        while self.running:
            try:
                data = self.net.receive_data(conn)
                if data:
                    print(f'Received data: {data}')
                    self.log.log_info('handle_client', f'Received data: {data}')
                    # Echo data back to client (as an example)
                    self.net.send_data(conn, data)
                else:
                    self.log.log_warning('handle_client', 'No data received, connection might be closed')
                    break
            except socket.error as se:
                self.log.log_error('handle_client', f'Socket error on receive: {se}')
                break
        conn.close()
        self.log.log_info('handle_client', f'Connection closed with {addr}')


if __name__ == "__main__":
    server = BattleshipServer()
    server.start_server()
