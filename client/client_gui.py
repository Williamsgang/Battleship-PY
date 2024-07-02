# client/client_gui.py

import pygame
from logs import logger
from shared.board_ships_players import Board, Ships, Players
from assets.images.images import battleship_icon


class ClientGUI:
    def __init__(self):
        self.log = logger.Logger(self.__class__.__name__)
        self.log.log_info('ClientGUI', 'Initializing GUI...')

        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption('Battleship')
        pygame.display.set_icon(pygame.image.load(battleship_icon))

        # Global variables
        self.SQ_SIZE = 45
        self.H_MARGIN = self.SQ_SIZE * 4
        self.V_MARGIN = self.SQ_SIZE
        self.WIDTH = self.SQ_SIZE * 10 * 2 + self.H_MARGIN
        self.HEIGHT = self.SQ_SIZE * 10 * 2 + self.V_MARGIN
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.INDENT = 10

        # Colors
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.WHITE = (255, 255, 255)

        # Initialize board and ships
        self.board = Board()
        self.ships = Ships()
        self.player = Players()
        # self.opponent = Players()  # Assuming an opponent player object for demonstration

    def draw_grid(self, left=0, top=0):
        for i in range(100):
            x = left + i % 10 * self.SQ_SIZE
            y = top + i // 10 * self.SQ_SIZE
            square = pygame.Rect(x, y, self.SQ_SIZE, self.SQ_SIZE)
            pygame.draw.rect(self.SCREEN, self.GREEN, square, width=3)
        self.log.log_info('draw_grid', 'Grid drawn')

    def draw_ships(self, player, left=0, top=0):
        for ship in player.ships.values():
            for (row, col) in ship.indexes:
                x = left + col * self.SQ_SIZE + self.INDENT
                y = top + row * self.SQ_SIZE + self.INDENT
                if ship.orientation == "horizontal":
                    width = ship.size * self.SQ_SIZE - 2 * self.INDENT
                    height = self.SQ_SIZE - 2 * self.INDENT
                else:
                    width = self.SQ_SIZE - 2 * self.INDENT
                    height = ship.size * self.SQ_SIZE - 2 * self.INDENT
                rectangle = pygame.Rect(x, y, width, height)
                pygame.draw.rect(self.SCREEN, self.WHITE, rectangle, border_radius=15)
        self.log.log_info('draw_ships', 'Ships drawn')

    def main_loop(self):
        running = True
        pausing = False
        self.log.log_info('main_loop', 'Entering main GUI loop...')
        while running:
            try:
                # Track user interaction
                for event in pygame.event.get():
                    # User closes the pygame window
                    if event.type == pygame.QUIT:
                        self.log.log_info('main_loop', 'QUIT event received')
                        running = False

                    # User presses key on keyboard
                    if event.type == pygame.KEYDOWN:
                        # Escape key to close the animation
                        if event.key == pygame.K_ESCAPE:
                            self.log.log_info('main_loop', 'ESCAPE key pressed')
                            running = False

                        # Space bar to pause and unpause the game
                        if event.key == pygame.K_SPACE:
                            self.log.log_info('main_loop', 'SPACE key pressed')
                            pausing = not pausing

                # Execution
                if not pausing:
                    # Draw background
                    self.SCREEN.fill(self.BLACK)
                    self.log.log_info('main_loop', 'Background drawn')

                    # Draw search grids
                    self.draw_grid()
                    self.draw_grid(left=(self.WIDTH - self.H_MARGIN) // 2 + self.H_MARGIN,
                                   top=(self.HEIGHT - self.V_MARGIN) // 2 + self.V_MARGIN)

                    # Draw position grids
                    self.draw_grid(top=(self.HEIGHT - self.V_MARGIN) // 2 + self.V_MARGIN)
                    self.draw_grid(left=(self.WIDTH - self.H_MARGIN) // 2 + self.H_MARGIN)

                    # Draw ships onto position grids
                    self.draw_ships(self.player, top=(self.HEIGHT - self.V_MARGIN) // 2 + self.V_MARGIN)
                    # self.draw_ships(self.opponent, left=(self.WIDTH - self.H_MARGIN) // 2 + self.H_MARGIN)

                    # Update screen
                    pygame.display.flip()
                    self.log.log_info('main_loop', 'Screen updated')
            except Exception as e:
                self.log.log_error('main_loop', f'Error during GUI loop: {e}')
                running = False


if __name__ == "__main__":
    client_gui = ClientGUI()
    client_gui.main_loop()
