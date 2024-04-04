class Boards:
    def __init__(self, board_size, ship_count, players):
        self.board_size = board_size
        self.ship_count = ship_count
        self.players = players

    def create_boards(self, players):
        for player in players:
            for num in range(self.board_size):
                player['board'].append(["O"] * self.board_size)

    # Prints the board when the method is called
    def print_board(self, players):
        for player in players:
            print("Player " + str(player["player_num"]) + "'s board:")
            for row in player["board"]:
                print(" ".join(row))
            print("=============================")
