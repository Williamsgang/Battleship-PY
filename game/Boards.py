class Boards:
    board_sizes = [(10, 14),  # Normal board size
                   (5, 5),    # Speed rounds
                   (26, 26)]  # Armada round

    def __init__(self, board_size, ship_count, players):
        self.board_size = board_size
        self.ship_count = ship_count
        self.players = players

    def create_boards(self, size_index, players):
        board_size = self.board_sizes[size_index]

        for player in players:
            player['board'] = []  # initialize the board for each player
            for _ in range(board_size[0]):  # iterate for the number of rows
                player['board'].append(["O"] * board_size[1])  # add a row with the correct number of column

    # Prints the board when the method is called
    def print_board(self, players):
        for player in players:
            print("Player " + str(player["player_num"]) + "'s board:")
            for row in player["board"]:
                print(" ".join(row))
            print("=============================")


class Tiles:
    def __init__(self, num_tiles):
        self.num_tiles = num_tiles  # Number of tiles

    def display(self):
        print("Displaying " + str(self.num_tiles) + " tiles")


players = [{"name": "Alice", "board": [], "player_num": 0}, {"name": "Bob", "board": [], "player_num": 1}]  # Initialize players

# Initialize a Boards object
boards = Boards(board_size=(10, 10), ship_count=5, players=players)

# Call the create_boards_new method with an index of the desired board size
# For example, 0 for (10, 14), 1 for (5, 5), or 2 for (26, 26)
boards.create_boards(0, players)
boards.print_board(players)
