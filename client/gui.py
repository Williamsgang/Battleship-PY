# client/gui.py
# GUI for the Battleship client using pygame.

import pygame
import pygame.freetype

from .logger import ClientLogger
from .animations import AnimationManager
from assets.images import images


class BattleshipClientGUI:
    def __init__(self, client):
        self.logger_name_reference = 'BattleshipClientGUI'
        self.logger = ClientLogger(self.logger_name_reference)
        self.logger.log_info(self.logger_name_reference, "Logger initialized.")

        self.client = client
        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Battleship Client")

        self.font = pygame.freetype.SysFont(None, 24)
        self.running = True

        self.board_size = 10
        self.cell_size = 40
        self.margin = 5

        self.set_icon(images.battleship_icon)

        self.board_buttons = [[pygame.Rect(j * (self.cell_size + self.margin) + 100,
                                           i * (self.cell_size + self.margin) + 100,
                                           self.cell_size, self.cell_size)
                               for j in range(self.board_size)] for i in range(self.board_size)]

        self.buttons = [
            ("Connect", pygame.Rect(600, 100, 150, 40), self.connect_to_server),
            ("Show Stats", pygame.Rect(600, 150, 150, 40), self.request_stats),
            ("Settings", pygame.Rect(600, 200, 150, 40), self.open_settings),
            ("Quit Game", pygame.Rect(600, 250, 150, 40), self.quit_game)
        ]

        self.animation_manager = AnimationManager(self)

    def connect_to_server(self):
        # TODO: Implement connection to server logic.
        pass

    def attack(self, x, y):
        # TODO: Implement attack logic.
        pass

    def update_board(self, position, result):
        # TODO: Update the board with the result of an attack.
        pass

    def log_message(self, message):
        # Display a message on the screen (for simplicity)
        print(f"Game Info: {message}")

    def request_stats(self):
        # TODO: Request statistics from the server.
        pass

    def open_settings(self):
        # TODO: Open settings window
        pass

    def quit_game(self):
        self.running = False

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
                    for i in range(self.board_size):
                        for j in range(self.board_size):
                            if self.board_buttons[i][j].collidepoint(mouse_pos):
                                self.attack(i, j)

            self.draw_board()
            self.draw_buttons()
            pygame.display.flip()

        pygame.quit()

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

    def draw_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                pygame.draw.rect(self.screen, (0, 0, 0), self.board_buttons[i][j], 2)
                self.font.render_to(self.screen, (self.board_buttons[i][j].x + 10, self.board_buttons[i][j].y + 10),
                                    "X", (255, 255, 255))

    def draw_buttons(self):
        for label, rect, _ in self.buttons:
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
            self.font.render_to(self.screen, (rect.x + 10, rect.y + 10), label, (255, 255, 255))


if __name__ == "__main__":
    client = None  # Replace with actual client object
    gui = BattleshipClientGUI(client)
    gui.run()
