# client_gui.py

import pygame

from logs import logger
from .game import GameGUI
from .main_menu import MainMenuGUI
from .settings import SettingsGUI


class ClientGUI:
    def __init__(self):
        self.log = logger.Logger(self.__class__.__name__)
        self.log.log_info('ClientGUI', 'Initializing GUI...')
        pygame.init()
        pygame.display.set_caption('Battleship')
        self.SQ_SIZE = 45
        self.H_MARGIN = self.SQ_SIZE * 4
        self.V_MARGIN = self.SQ_SIZE
        self.WIDTH = self.SQ_SIZE * 10 * 2 + self.H_MARGIN
        self.HEIGHT = self.SQ_SIZE * 10 * 2 + self.V_MARGIN
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.running = True

        self.screens = {
            "main_menu": MainMenuGUI(self),
            "settings": SettingsGUI(self),
            "game": GameGUI(self),
        }
        self.current_screen = self.screens["main_menu"]

    def set_screen(self, screen_name):
        self.current_screen = self.screens[screen_name]

    def main_loop(self):
        self.log.log_info('main_loop', 'Entering main GUI loop...')
        while self.running:
            try:
                events = pygame.event.get()
                self.current_screen.handle_events(events)
                self.current_screen.update()
                self.current_screen.render()
                pygame.display.flip()
            except Exception as e:
                self.log.log_error('main_loop', f'Error during GUI loop: {e}')
                self.running = False

        pygame.quit()
        self.log.log_info('main_loop', 'Exited main GUI loop')


if __name__ == "__main__":
    client_gui = ClientGUI()
    client_gui.main_loop()
