# battleship/bsp.py

# imports from outside packages
import random
from typing import Tuple
import numpy as np

# imports from local packages
from config import settings
from log import logger

game_settings = settings.load_settings()


class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.row = random.randrange(0, game_settings['game']['board_size'])
        self.col = random.randrange(0, game_settings['game']['board_size'])
        self.orientation = random.choice(['horizontal', 'vertical'])
        self.indexes = self.compute_indexes()

    def compute_indexes(self):
        indexes = []
        for i in range(self.size):
            if self.orientation == 'horizontal':
                if self.col + i >= game_settings['game']['board_size']:  # Prevent horizontal overflow
                    return []
                indexes.append((self.row, self.col + i))
            elif self.orientation == 'vertical':
                if self.row + i >= game_settings['game']['board_size']:  # Prevent vertical overflow
                    return []
                indexes.append((self.row + i, self.col))
        return indexes

    def place_ship(self, positions):
        self.indexes = positions


class Ships:
    def __init__(self):
        self.log = logger.Logger(self.__class__.__name__)
        self.ships = self.create_ships()

    def create_ships(self):
        ships_config = game_settings['game']['ships']
        ships = {ship['name']: Ship(ship['name'], ship['size']) for ship in ships_config}
        self.log.log_info('create_ships', 'Ships created')
        return ships


class Board:
    def __init__(self):
        self.log = logger.Logger(self.__class__.__name__)
        self.board_size = (game_settings['game']['board_size'], game_settings['game']['board_size'])
        self.grid = self.create_board()

    def create_board(self, board_size: Tuple[int, int] = None):
        if board_size is None:
            board_size = self.board_size

        rows = board_size[0]
        cols = board_size[1]
        board = []

        for row in range(rows):
            board.append([])
            for col in range(cols):
                board[row].append("0")

        self.log.log_info('create_board', f'Board created. Board size is: {board_size}')
        return board

    def is_valid_position(self, positions):
        for (row, col) in positions:
            if row < 0 or row >= self.board_size[0] or col < 0 or col >= self.board_size[1]:
                return False
            if self.grid[row][col] != "0":
                return False
        return True

    def place_ships(self, ships):
        for ship in ships.values():
            while True:
                row = random.randint(0, self.board_size[0] - 1)
                col = random.randint(0, self.board_size[1] - 1)
                positions = []
                orientation = random.choice(["horizontal", "vertical"])

                for i in range(ship.size):
                    if orientation == "horizontal":
                        positions.append((row, col + i))
                    elif orientation == "vertical":
                        positions.append((row + i, col))

                if self.is_valid_position(positions):
                    break
                else:
                    self.log.log_warning('place_ships', f'Invalid position for placing {ship.name}.')

            for (r, c) in positions:
                if ship.name == 'Carrier':
                    self.grid[r][c] = "C"
                elif ship.name == 'Battleship':
                    self.grid[r][c] = "B"
                elif ship.name == 'Cruiser':
                    self.grid[r][c] = "R"
                elif ship.name == 'Submarine':
                    self.grid[r][c] = "S"
                elif ship.name == 'Destroyer':
                    self.grid[r][c] = "D"
                else:
                    self.log.log_error('place_ships', f'Invalid ship name: {ship.name}')
                    return

            self.log.log_info('place_ships', f'Ship, {ship.name}, placed at positions: {positions}, '
                                             f'with an orientation of: {orientation}')
            ship.place_ship(positions)

    def display_board(self):
        for row in self.grid:
            print(" ".join(row))
        self.log.log_info('display_board', f'Board displayed in the console.')

    def count_ships(self, player):
        grid_clone = player.ship_tracker.grid

        values, counts = np.unique(grid_clone, return_counts=True)

        return f'{values, counts}'


class Player:
    def __init__(self):
        # Logger to map issues and log all necessary details
        self.log = logger.Logger(self.__class__.__name__)

        # Ship board that typically the player knows their own ship locations
        self.ships = Ships().ships
        self.ship_tracker = Board()
        self.ship_tracker.place_ships(self.ships)

        # Board for the player to track where they
        # have shot at and where the enemy players ships are
        self.shot_tracker = Board()

    def shoot(self, position):
        pass
    # if shoot at J4
    # make self.shoot_board[j4] = "SHOOT"
    # if its a hit (from server) self.shoot_board[j4] = "HIT"
