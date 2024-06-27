# client/client.py
# Main client logic for the Battleship game.

import socket
from .network import ClientNetwork
from .gui import BattleshipClientGUI
from .game_logic import GameLogic
from .player import Player
from .logger import ClientLogger


class BattleshipClient:
    def __init__(self, host, port, player_name):
        self.logger_name_reference = 'BattleshipClient'
        self.network = ClientNetwork(host, port)
        self.gui = BattleshipClientGUI(self)
        self.game_logic = GameLogic(self)
        self.player = Player(player_name)
        self.logger = ClientLogger(f"client_logs_{player_name}.log")
        self.logger.log_info(self.logger_name_reference + '.contstructor', "Client has been initialized")


    def start(self):
        self.logger.log_info(self.logger_name_reference + '.start()', "Client started.")
        self.gui.run()
        try: 
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.network.host, self.network.port))
                s.sendall(b'Client started and connected to server')
                data = s.recv(1024)

            self.logger.log_info(self.logger_name_reference + '.start()', "Client connection succeeded")
        except Exception as e:
            print(e)

    def receive_data(self):
        while True:
            try:
                data = self.network.receive()
                if data:
                    self.logger.log_info(self.logger_name_reference + '.receive_data()', 'Data was received here')
                else:
                    self.logger.log_error(self.logger_name_reference + '.receive_data()', 'Data was not received from the server')
            except socket.error as e:
                self.logger.log_error(self.logger_name_reference + '.receive_data()', f'Socket error occurred at: {e}')

    def send_data(self, data):
        try:
            self.network.send(data)
            self.logger.log_info(self.logger_name_reference + '.send_data()', f'Data was sent from here')
        except socket.error as e:
            self.logger.log_error(self.logger_name_reference + '.send_data()', f'Socket error occurred at: {e}')
            

    # TODO: Add methods for handling network communication, game logic, etc.

if __name__ == "__main__":
    host = "127.0.0.1"  # TODO: Update with actual server IP.
    port = 65432
    player_name = "Player1"  # TODO: Get player name from user input.
    client = BattleshipClient(host, port, player_name)
    client.start()
