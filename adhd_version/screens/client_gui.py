import pygame
from adhd_version.logs import logger
from adhd_version.networking import network
from main_menu import MainMenuScreen
from settings import SettingsGUI
from game import GameGUI
from user_info import UserInfoGUI
import pickle


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
        self.ip_address = "127.0.0.1"  # Example IP address, replace with actual client IP

        self.screens = {
            "main_menu": MainMenuScreen(self),
            "settings": SettingsGUI(self),
            "game": GameGUI(self),
            "user_info": UserInfoGUI(self),
        }
        self.current_screen = self.screens["main_menu"]
        self.network = network.Network((self.ip_address, 65432), is_server=False)

    def set_screen(self, screen_name):
        self.current_screen = self.screens[screen_name]

    def get_ip_address(self):
        return self.ip_address

    def start_game(self):
        self.log.log_info('start_game', 'Attempting to start game...')
        self.network.connect()
        self.network.send_data(self.network.s, pickle.dumps({"action": "find_match", "username": self.username}))
        while True:
            data = self.network.receive_data(self.network.s)
            if data:
                response = pickle.loads(data)
                if response.get("status") == "match_found":
                    self.opponent_name = response.get("opponent_name")
                    self.log.log_info('start_game', f'Match found with {self.opponent_name}')
                    self.set_screen("game")
                    break

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
