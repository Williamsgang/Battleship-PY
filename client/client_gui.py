# client/client_gui.py
# GUI for the Battleship client using pygame.

import pygame
import pygame.freetype

from logs import logger
from assets.images import images


class BattleshipClientGUI:
    def __init__(self, client):
        self.logger_name_reference = 'BattleshipClientGUI'
        self.logger = logger.Logger(self.logger_name_reference)
        self.logger.log_info('Logger initialized.')

    def run(self):
        NotImplementedError


if __name__ == "__main__":
    client = None  # Replace with actual client object
    # gui = BattleshipClientGUI(client)
    # gui.run()
