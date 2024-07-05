# battleship/bsp.py
import random
from typing import Tuple

from adhd_version.logs import logger
from config import settings

from collections import Counter

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
        self.board = self.create_board()

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
            if self.board[row][col] != "0":
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
                    self.board[r][c] = "C"
                elif ship.name == 'Battleship':
                    self.board[r][c] = "B"
                elif ship.name == 'Cruiser':
                    self.board[r][c] = "R"
                elif ship.name == 'Submarine':
                    self.board[r][c] = "S"
                elif ship.name == 'Destroyer':
                    self.board[r][c] = "D"
                else:
                    self.log.log_error('place_ships', f'Invalid ship name: {ship.name}')
                    return

            self.log.log_info('place_ships', f'Ship, {ship.name}, placed at positions: {positions}, '
                                             f'with an orientation of: {orientation}')
            ship.place_ship(positions)

    def display_board(self):
        for row in self.board:
            print(" ".join(row))
        self.log.log_info('display_board', f'Board displayed in the console.')

    def count_ships(self):
        board_clone = self.board
        for row in board_clone:
            while "0" in row:
                row.remove("0")
            while "X" in row:
                row.remove("X")
        return board_clone


class Player:
    def __init__(self):
        self.log = logger.Logger(self.__class__.__name__)

        self.ships = Ships().ships
        self.board = Board()
        self.board.place_ships(self.ships)

        self.shoot_board = Board()



    def place_ships(self, ships):
        for ship in ships.values():
            while True:
                row = random.randint(0, self.board.board_size[0] - 1)
                col = random.randint(0, self.board.board_size[1] - 1)
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
                    self.board[r][c] = "C"
                elif ship.name == 'Battleship':
                    self.board[r][c] = "B"
                elif ship.name == 'Cruiser':
                    self.board[r][c] = "R"
                elif ship.name == 'Submarine':
                    self.board[r][c] = "S"
                elif ship.name == 'Destroyer':
                    self.board[r][c] = "D"
                else:
                    self.log.log_error('place_ships', f'Invalid ship name: {ship.name}')
                    return

            self.log.log_info('place_ships', f'Ship, {ship.name}, placed at positions: {positions}, '
                                             f'with an orientation of: {orientation}')
            ship.place_ship(positions)
        self.log.log_info('place_ships', 'Ships placed for the player')


    def is_valid_position(self, positions):
        for (row, col) in positions:
            if row < 0 or row >= self.board.board_size[0] or col < 0 or col >= self.board.board_size[1]:
                return False
            if self.board.board[row][col] != "0":
                return False
        return True

    def show_ships(self, player):
        board = player.board.board
        for row in board:
            print(' '.join(row))
        self.log.log_info('show_ships', 'Player ships displayed')

    def shoot(self, position):
        pass
    # if shoot at J4
    # make self.shoot_board[j4] = "SHOOT"
    # if its a hit (from server) self.shoot_board[j4] = "HIT"