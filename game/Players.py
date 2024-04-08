class Players:
    def __init__(self, ship_count):
        self.ship_count = ship_count
        self.players = []

    def new_player(self, num):
        player = {
            "player_num": num,
            "ship_count": self.ship_count,
            "ship_locations": [],
            "board": []
        }
        return player

    def create_players(self, player_num):
        for num in range(player_num):
            self.players.append(self.new_player(num + 1))

    def get_players(self):
        return self.players

    # Debug for getting each player information
    def player_debug_information(self, players):
        for player in players:
            print("==================================")
            print("")
            print(f"Player {player['player_num']}:")
            for key, value in player.items():
                print(f"{key}: {value}")
            print("")

    def check_ship_locations(self, players, tiles):
        for player in players:
            print(f"Player {player['player_num']}'s info: ")
            for ship_location in player["ship_locations"]:
                if ship_location in tiles:
                    print(f"Ship located at {ship_location}")
                else:
                    print(f"No ship at {ship_location}")
