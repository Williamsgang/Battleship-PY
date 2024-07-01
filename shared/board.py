# shared/engine.py
# Parent class of the engine for server and clients
import random
from typing import Tuple

from logs import logger
from shared.ships import Ships


class Board:
    def __init__(self):
        self.log = logger.Logger(self.__class__.__name__)
        self.board_size = (10, 10)  # 10x10 engine size
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

        self.log.log_info('create_board()', f'Board created. Board size is: {board_size}')
        return board

    def is_valid_position(self, positions):
        for (row, col) in positions:
            if row < 0 or row >= self.board_size[0] or col < 0 or col >= self.board_size[1]:
                return False
            if self.board[row][col] != "0":
                return False
        return True

    def place_ships(self):
        ships = Ships()
        for ship in ships.ships.values():
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
                    self.log.log_warning('place_ships()', f'Invalid position for placing {ship.name}.')

            for (r, c) in positions:
                if ship.name == 'Aircraft Carrier':
                    self.board[r][c] = "A"
                elif ship.name == 'Battleship':
                    self.board[r][c] = "B"
                elif ship.name == 'Light Missile Cruiser':
                    self.board[r][c] = "L"
                elif ship.name == 'Submarine':
                    self.board[r][c] = "S"
                elif ship.name == 'Destroyer':
                    self.board[r][c] = "D"
                else:
                    self.log.log_error('place_ships()', f'Invalid ship name: {ship.name}')
                    return

            self.log.log_info('place_ships()', f'Ship, {ship.name}, placed at positions: {positions}, '
                                               f'with an orientation of: {orientation}')
            ship.place_ship(positions)

    def display_board(self):
        for row in self.board:
            print(" ".join(row))
        self.log.log_info('display_board()', f'Board displayed in the console.')


if __name__ == "__main__":
    board_instance = Board()
    ships = Ships()
    # for ship in ships.ships.values():  # Iterate over the ship instances
    #     board_instance.place_ships(ship, (random.randint(0, 10), random.randint(0, 10)), "vertical")

    # for ship in ships.ships.values():
    #     board_instance.place_ships(ship)

    board_instance.place_ships()

    board_instance.display_board()
