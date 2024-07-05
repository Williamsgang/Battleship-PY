# server/game_logic.py
from adhd_version.logs import logger
from adhd_version.shared import board_ships_players


class GameLogic:
    def __init__(self):
        # Initialize the log, board, ships, players, hits, and ships sunk count
        self.log = logger.Logger(self.__class__.__name__)
        self.log.log_info('__init__', 'Initializing GameLogic')
        self.board = board_ships_players.Board()
        self.ships = board_ships_players.Ships()
        self.players = [board_ships_players.Players() for _ in range(2)]  # Assuming 2 players
        self.hits = 0
        self.ships_sunk = 0

    def shoot(self, player_index: int, x: int, y: int):
        """
        Handles the shooting logic. Checks if the shot is a hit or miss and logs the result.
        """
        self.log.log_info('shoot', f'Player {player_index} shooting at coordinates ({x}, {y})')
        target_player = (player_index + 1) % 2  # The target is the other player
        board = self.players[target_player].search
        if board[x][y] != 'U':  # 'U' for unknown
            self.log.log_warning('shoot', 'Coordinates already shot at')
            return 'Already Shot'

        if self.hit(target_player, x, y):
            self.log.log_info('shoot', 'Hit confirmed')
            board[x][y] = 'H'  # 'H' for hit
            if self.ship_sunk(target_player):
                self.log.log_info('shoot', 'Ship sunk')
                self.ships_sunk += 1
                return 'Ship Sunk'
            return 'Hit'
        else:
            self.log.log_info('shoot', 'Miss')
            board[x][y] = 'M'  # 'M' for miss
            return 'Miss'

    def hit(self, target_player: int, x: int, y: int) -> bool:
        """
        Checks if the shot is a hit. If it is, marks the ship's hit.
        """
        for ship in self.players[target_player].ships:
            if (x, y) in ship.indexes:
                ship.indexes.remove((x, y))
                self.log.log_info('hit', f'Ship hit at ({x}, {y})')
                self.hits += 1
                return True
        return False

    def ship_sunk(self, target_player: int) -> bool:
        """
        Checks if a ship has been sunk.
        """
        for ship in self.players[target_player].ships:
            if not ship.indexes:  # No more indexes left, ship is sunk
                self.log.log_info('ship_sunk', f'{ship.name} has been sunk')
                self.players[target_player].ships.remove(ship)
                return True
        return False

    def all_ships_sunk(self, target_player: int) -> bool:
        """
        Checks if all ships of a player have been sunk.
        """
        if not self.players[target_player].ships:
            self.log.log_info('all_ships_sunk', f'All ships of player {target_player} have been sunk')
            return True
        return False


if __name__ == "__main__":
    game_logic_check = GameLogic()
    result = game_logic_check.shoot(0, 1, 2)
    print(f"Shot result: {result}")
