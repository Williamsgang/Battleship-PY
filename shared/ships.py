# shared/ships.py
# Parent class of the ships for server and clients
from logs import logger


class Ship:
    def __init__(self, name, size):
        self.log = logger.Logger(self.__class__.__name__)
        self.name = name
        self.size = size
        self.hits = 0
        self.positions = []

    def is_sunk(self):
        return self.hits == self.size

    def place_ship(self, positions):
        self.positions = positions

    def hit(self):
        self.hits += 1


class Ships:
    def __init__(self):
        self.log = logger.Logger(self.__class__.__name__)
        self.ships = {
            'aircraft_carrier': Ship('Aircraft Carrier', 5),
            'battleship': Ship('Battleship', 4),
            'light_missile_cruiser': Ship('Light Missile Cruiser', 3),
            'submarine': Ship('Submarine', 3),
            'destroyer': Ship('Destroyer', 2),
        }

    def all_sunk(self):
        self.log.log_info('all_sunk', f'All ships have been sunk')
        return all(ship.is_sunk() for ship in self.ships.values())

    def get_ship(self, name):
        return self.ships.get(name)

    def get_ships(self, ships):
        ships = self.ships
        return ships

    def place_ship(self, name, positions):
        ship = self.get_ship(name)
        if ship:
            ship.place_ship(positions)
        self.log.log_info('place_ship', f'Ship place @: {positions}')

    def hit_ship(self, position):
        for ship in self.ships.values():
            if position in ship.positions:
                ship.hit()
                self.log.log_info('hit_ship', f'{ship.name} hit @ {position}')
                return ship.name
        return None

