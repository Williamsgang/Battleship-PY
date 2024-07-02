# shared/board_ships_players.py
# Initialization of the board, ships, and players

import random
from typing import Tuple

import config.settings
from logs import logger

game_settings = config.settings.load_settings()


class Ship:
    def __init__(self, name, size):
        self.log = logger.Logger(self.__class__.__name__)
        self.name = name
        self.size = size
        self.row = random.randrange(0, game_settings['game']['board_size'])
        self.col = random.randrange(0, game_settings['game']['board_size'])
        self.orientation = random.choice(['horizontal', 'vertical'])
        self.indexes = self.compute_indexes()
        self.log.log_info('__init__',
                          f'{self.name} initialized with size {self.size}, position ({self.row}, {self.col}), orientation {self.orientation}')

    def compute_indexes(self):
        indexes = []
        for i in range(self.size):
            if self.orientation == 'horizontal':
                if self.col + i >= game_settings['game']['board_size']:  # Prevent horizontal overflow
                    self.log.log_warning('compute_indexes', 'Horizontal overflow prevented')
                    return []
                indexes.append((self.row, self.col + i))
            elif self.orientation == 'vertical':
                if self.row + i >= game_settings['game']['board_size']:  # Prevent vertical overflow
                    self.log.log_warning('compute_indexes', 'Vertical overflow prevented')
                    return []
                indexes.append((self.row + i, self.col))
        self.log.log_info('compute_indexes', f'Indexes computed for {self.name}: {indexes}')
        return indexes

    def place_ship(self, positions):
        self.indexes = positions
        self.log.log_info('place_ship', f'{self.name} placed at positions {positions}')


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
                self.log.log_warning('is_valid_position', f'Position out of bounds: ({row}, {col})')
                return False
            if self.board[row][col] != "0":
                self.log.log_warning('is_valid_position', f'Position already occupied: ({row}, {col})')
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
                    self.log.log_warning('place_ships', f'Invalid position for placing {ship.name} at ({row}, {col})')

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

            self.log.log_info('place_ships',
                              f'Ship, {ship.name}, placed at positions: {positions}, with an orientation of: {orientation}')
            ship.place_ship(positions)

    def display_board(self):
        for row in self.board:
            print(" ".join(row))
        self.log.log_info('display_board', 'Board displayed in the console')


class Players:
    def __init__(self):
        self.log = logger.Logger(self.__class__.__name__)
        self.ships = Ships().ships
        self.search = ['U' for _ in range(100)]  # 'U' for unknown
        self.indexes = []  # Initialize indexes before placing ships
        self.place_ships()

    def place_ships(self):
        board = Board()
        board.place_ships(self.ships)
        self.log.log_info('place_ships', 'Ships placed for the player')
        self.board = board

    def show_ships(self):
        display_board = [['-' for _ in range(game_settings['game']['board_size'])] for _ in
                         range(game_settings['game']['board_size'])]
        for ship in self.ships.values():
            for (row, col) in ship.indexes:
                display_board[row][col] = 'X'
        for row in display_board:
            print(' '.join(row))
        self.log.log_info('show_ships', 'Player ships displayed')


if __name__ == "__main__":
    player = Players()
    player1 = Players()

    player.show_ships()

    print()

    player1.show_ships()
