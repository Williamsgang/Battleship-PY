# server/server.py
# Main server logic for the Battleship game.

import socket
import threading
import pickle
from .network import Network
from .game_logic import GameLogic
from .player import PlayerManager
from .logger import ServerLogger


class BattleshipServer:

    HOST = "127.0.0.0"
    PORT = 65432

    def __init__(self, host=HOST, port=PORT):
        self.network = Network(host, port)
        self.game_logic = GameLogic(self)
        self.player_manager = PlayerManager()
        self.logger = ServerLogger("server_logs.log")
        self.clients = []

    def start(self):
        self.logger.log_info('BattleshipServer', 'Server started.')

        try:
            self.network.start_server(self.handle_client)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    self.logger.log_info(f"Connected by {addr}")
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        conn.sendall(data)
        except Exception as e:
            self.logger.log_error('BattleshipServer', f"Error occurred: {e}")

    def handle_client(self, client_socket):
        # TODO: Implement client handling logic.
        NotImplementedError

    def set_admin(self):
        pass

    # TODO: Add methods for handling game logic, client communication, etc.


if __name__ == "__main__":
    server = BattleshipServer()
    server.start()
