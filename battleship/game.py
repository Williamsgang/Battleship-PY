from typing import Tuple

from battleship.bsp import game_settings
from log import logger


class Game:
    def __init__(self, id):
        self.log = logger.Logger(self.__class__.__name__)
        self.id = id
        self.p1_shot = False
        self.p2_shot = False
        self.ready = False


    def get_players(self):
        return self.players

    def get_player_shot(self, player):
        pass

    def connected(self):
        return self.ready

    def shoot(self, attacking_player, target_player, position: Tuple[int, int]):
        a_player_shot_board = attacking_player.shot_tracker
        t_player_ship_board = target_player.ship_tracker

        row, col = position

        if not (0 <= row < game_settings['game']['board_size'] and 0 <= col < game_settings['game']['board_size']):  # Shot is in bounds check
            self.log.log_warning('shoot', f'Shot out of bounds @ ({row}, {col})')
            return

        if a_player_shot_board.grid[row][col] not in ['0', 'H', 'M']:  # Not shooting the same spot check
            self.log.log_warning('shoot', f'Shot already taken @ ({row}, {col})')
            return

        if t_player_ship_board.is_ship_location(position, target_player):  # Shot hits ship check
            a_player_shot_board.grid[row][col] = 'H'
            t_player_ship_board.grid[row][col] = 'H'

        else:  # Else missed shot
            a_player_shot_board.grid[row][col] = 'M'
            t_player_ship_board.grid[row][col] = 'M'
            self.log.log_info('shoot', f'Shot missed @ {position}')

    def winner(self):
        pass