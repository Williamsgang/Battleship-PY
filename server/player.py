# server/player.py
# Player information management for the Battleship server.

class PlayerManager:
    def __init__(self):
        self.players = {}

    def add_player(self, ip_address, player_name):
        self.players[ip_address] = {
            "name": player_name,
            "stats": {
                "kills": 0,
                "wins": 0,
                "losses": 0
            }
        }

    def update_stats(self, ip_address, kills=0, wins=0, losses=0):
        player = self.players.get(ip_address)
        if player:
            player["stats"]["kills"] += kills
            player["stats"]["wins"] += wins
            player["stats"]["losses"] += losses

    # TODO: Add methods for managing player stats and information.
