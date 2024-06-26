# client/client.py
# Main client logic for the Battleship game.

import socket
import pickle
import threading
from .network import Network
from .gui import BattleshipClientGUI
from .game_logic import GameLogic
from .player import Player
from .logger import Logger

class BattleshipClient:
    def __init__(self, host, port, player_name):
        self.network = Network(host, port)
        self.gui = BattleshipClientGUI(self)
        self.game_logic = GameLogic(self)
        self.player = Player(player_name)
        self.logger = Logger(f"client_logs_{player_name}.log")

    def start(self):
        self.logger.log("Client started.")
        self.gui.start()

    # TODO: Add methods for handling network communication, game logic, etc.

if __name__ == "__main__":
    host = "127.0.0.1"  # TODO: Update with actual server IP.
    port = 65432
    player_name = "Player1"  # TODO: Get player name from user input.
    client = BattleshipClient(host, port, player_name)
    client.start()
