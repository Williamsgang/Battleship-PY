import random
from .Players import Players


class Battleships:
    def __init__(self, board_size, ship_count, player_num):
        player_obj = Players(ship_count)
        self.board_size = board_size
        self.ship_count = ship_count
        self.players = []
        for num in range(player_num):
            self.players.append(player_obj.new_player(num + 1))

    # Method for randomizing the row value for ships
    def random_row(self, board):
        return random.randint(0, len(board) - 1)

    # Method for randomizing the column value for ships
    def random_col(self, board):
        return random.randint(0, len(board[0]) - 1)

    # Method to obtain the ship locations within the teams
    def set_ship_locations(self, players):
        for player in players:
            for ship in range(player["ship_count"]):
                ship_row = self.random_row(player["board"])
                ship_col = self.random_col(player["board"])
                # Prints board with the 'X' to show locations
                while player["board"][ship_row][ship_col] != "O":
                    ship_row = self.random_row(player["board"])
                    ship_col = self.random_col(player["board"])
                player["board"][ship_row][ship_col] = "X"
                player["ship_locations"].append((ship_row, ship_col))

    def get_ship_locations(self, players):
        ship_locations = {}
        for player in players:
            ship_locations[player['player_num']] = player['ship_locations']

        return ship_locations

    def is_ship_location(self, players, location):
        ship_locations = self.get_ship_locations(players)
        for player_num, locations in ship_locations.items():
            if location in locations:
                return True
        return False

    def check_ship_locations(self, players, BOARD_RECTS):
        for player in players:
            print(f"Player {player['player_num']}'s info: ")
            for ship_location in player["ship_locations"]:
                if ship_location in BOARD_RECTS:
                    print(f"Ship located at {ship_location}")
                else:
                    print(f"No ship at {ship_location}")

# TODO: Ship sizes: Introduce ships of different sizes (e.g., battleship, destroyer) and allow the player to sink each ship by hitting all of its segments.
# TODO: Difficulty levels: Implement different difficulty levels (easy, medium, hard) by adjusting factors like the number of ships, the size of the board, or the number of turns allowed.
# TODO: Power-ups: Add power-ups that give the player advantages, such as extra guesses, revealing nearby ship locations, or clearing a row or column.
