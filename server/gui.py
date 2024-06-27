# server/gui.py
# GUI for the Battleship server using pygame.

import threading
import pygame
import pygame.freetype
from .server import BattleshipServer
from client.settings import SettingsPanel
from assets.images import images
from .logger import ServerLogger


class BattleshipServerGUI:

    def __init__(self, server):
        self.logger_name_reference = 'BattleshipServerGUI'
        self.logger = ServerLogger(self.logger_name_reference)
        self.logger.log_info(self.logger_name_reference, "Logger initialized.")
        self.server = server
        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Battleship Server")

        self.font = pygame.freetype.SysFont(None, 24)
        self.running = True
        self.logger.log_info(self.logger_name_reference + '.constructor', f'System font was set to {self.font}.')

        self.text_area = pygame.Rect(50, 50, 500, 400)
        self.text_area_content = []
        self.set_icon(images.battleship_icon)

        self.buttons = [
            ("Admin Panel", pygame.Rect(600, 100, 150, 40), self.open_admin_panel),
            ("Settings", pygame.Rect(600, 150, 150, 40), self.open_settings),
            ("Quit Game", pygame.Rect(600, 200, 150, 40), self.quit_game)
        ]

        self.logger.log_info(self.logger_name_reference + '.constructor', "GUI initialized without issues")
        threading.Thread(target=self.server.start).start()

    # Allows for change of icons on the GUI
    def set_icon(self, icon_path):
        try:
            icon = pygame.image.load(icon_path)
            pygame.display.set_icon(icon)
            # self.log_message(f'Icon is set to {icon}')
            self.logger.log_info(self.logger_name_reference + '.set_icon', f'Icon is set to {icon}')
        except pygame.error as e:
            print(f'Could not load icon: {e}')
            self.logger.log_error(self.logger_name_reference + '.set_icon', f'Icon was unable to be loaded')

    # Logs the server messages
    def log_message(self, message):
        self.text_area_content.append(message)
        if len(self.text_area_content) > 20:
            self.text_area_content.pop(0)
        self.logger.log_info(self.logger_name_reference + '.log_message', f'Message logged to the admin gui. Message: {message}')

    # Shows the user the active information from the
    # communications between the server and client
    def open_admin_panel(self):
        self.log_message("Admin Panel opened.")


        self.logger.log_info(self.logger_name_reference + '.open_admin_panel', 'Admin panel was opened.')
        # TODO: Implement admin panel logic.

    def open_settings(self):
        self.log_message("Settings Panel opened.")



        self.logger.log_info(self.logger_name_reference + '.open_settings', 'Settings were opened.')
        # TODO: Implement settings panel logic.

    # Quits the game
    def quit_game(self):
        self.logger.log_info(self.logger_name_reference + '.quit_game', 'Game was closed.')
        self.running = False

    # Runs
    def run(self):
        while self.running:
            self.screen.fill((0, 0, 128))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for label, rect, callback in self.buttons:
                        if rect.collidepoint(mouse_pos):
                            callback()

            self.draw_text_area()
            self.draw_buttons()
            pygame.display.flip()
        self.logger.log_info(self.logger_name_reference + '.run', 'Game was ran without issues.')
        pygame.quit()

    def draw_text_area(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.text_area)
        for idx, message in enumerate(self.text_area_content):
            self.font.render_to(self.screen, (self.text_area.x + 10, self.text_area.y + 10 + idx * 20),
                                message, (0, 0, 0), (255, 255, 255))

    def draw_buttons(self):
        for label, rect, _ in self.buttons:
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
            self.font.render_to(self.screen, (rect.x + 10, rect.y + 10), label, (255, 255, 255))


if __name__ == "__main__":
    server = BattleshipServer()
    gui = BattleshipServerGUI(server)
    gui.run()
