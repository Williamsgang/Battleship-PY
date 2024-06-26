# server/player.py
# Player information management for the Battleship server.

class AIManager:
    def __init__(self):
        self.ai = {}

    def add_ai(self, ip_address, player_name):
        self.ai[ip_address] = {
            "name": player_name,
            "stats": {
                "kills": 0,
                "wins": 0,
                "losses": 0
            }
        }

    def update_stats(self, ip_address, kills=0, wins=0, losses=0):
        ai = self.ai.get(ip_address)
        if ai:
            ai["stats"]["kills"] += kills
            ai["stats"]["wins"] += wins
            ai["stats"]["losses"] += losses

    # TODO: Add methods for managing player stats and information.
