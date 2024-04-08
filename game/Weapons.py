class Weapons:
    def __init__(self, ammo, not_implemented):
        self.not_implemented = not_implemented
        self.ammo = ammo

    def not_implemented(self):
        print(self.not_implemented)

    def get_ammo(self):
        return self.ammo

    def set_ammo(self, ammo):
        self.ammo = ammo
