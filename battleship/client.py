# battleship/client.py

import pygame.display
from pygame import font

import server
from bsp import Player
from config import constants
from log import logger
from network import Network

log = logger.Logger('client')

# Initialize pygame
pygame.init()

SCREEN = pygame.display.set_mode(constants.SCREEN)
pygame.display.set_caption("Battleship Client")

font = pygame.font.SysFont('comicsans', 40)


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redraw_screen(screen,  player):
    screen.fill(constants.BLACK)

    # Display Player 1 ship locations
    ship_info = "Player 1 ship locations: " + ", ".join(
        [f"{ship.name} at {ship.indexes}" for ship in player.ships.values()]
    )
    display_text(screen, ship_info, (10, constants.HEIGHT - 50))

    pygame.display.update()


def display_text(surface, text, position, color=constants.WHITE):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)


# function to draw a grid
def draw_grid(surface, left=0, top=0):
    for row in range(constants.BOARD_SIZE):
        for col in range(constants.BOARD_SIZE):
            x = left + col * constants.SQ_SIZE
            y = top + row * constants.SQ_SIZE
            rectangle = pygame.Rect(x, y, constants.SQ_SIZE, constants.SQ_SIZE)
            pygame.draw.rect(surface, constants.GREEN, rectangle, 1)  # Draw the grid with a green color


# function to draw ships onto the position grids
def draw_ships(player, surface, left=0, top=0):
    for ship in player.ships.values():
        for (r, c) in ship.indexes:
            x = left + c * constants.SQ_SIZE + constants.INDENT
            y = top + r * constants.SQ_SIZE + constants.INDENT
            if ship.orientation == "h":
                width = ship.size * constants.SQ_SIZE - 2 * constants.INDENT
                height = constants.SQ_SIZE - 2 * constants.INDENT
            else:
                width = constants.SQ_SIZE - 2 * constants.INDENT
                height = ship.size * constants.SQ_SIZE - 2 * constants.INDENT
            rectangle = pygame.Rect(x, y, width, height)
            pygame.draw.rect(surface, constants.WHITE, rectangle, border_radius=15)


def main():
    run = True
    n = Network()
    p1 = server.Server.players[0]
    p2 = server.players[1]
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2 = n.send(p1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        SCREEN.fill(constants.BLACK)

    # Debugging output to verify the drawing process
    print("Redrawing screen")
    print(f"Player 1 Ships: {[(ship.name, ship.row, ship.col) for ship in p1.ships.values()]}")

    pygame.quit()


if __name__ == "__main__":
    main()
