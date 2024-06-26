# client/player.py
# Player information for the Battleship client.

class Player:
    def __init__(self, name):
        self.name = name
        self.stats = {
            "kills": 0,
            "wins": 0,
            "losses": 0
        }

    def update_stats(self, kills=0, wins=0, losses=0):
        self.stats["kills"] += kills
        self.stats["wins"] += wins
        self.stats["losses"] += losses

    # TODO: Add methods for managing player stats.
