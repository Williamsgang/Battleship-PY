# battleship/client.py

import pygame.display

from bsp import Player
from config import constants
from log import logger
from network import Network

log = logger.Logger('client')

# Initialize pygame
pygame.init()

SCREEN = pygame.display.set_mode(constants.SCREEN)
pygame.display.set_caption("Battleship Client")

# Create two surfaces for the grids
SHOT_TRACKER = pygame.Surface((constants.WIDTH, constants.HEIGHT // 2))
SHIP_TRACKER = pygame.Surface((constants.WIDTH, constants.HEIGHT // 2))


def redraw_screen(screen, ship_tracker, shot_tracker):
    screen.fill(constants.BLACK)

    # Draw shot tracker at the top
    screen.blit(shot_tracker, (0, 0))

    # Draw ship tracker at them bottom
    screen.blit(ship_tracker, (0, constants.HEIGHT // 2))

    pygame.display.update()


# function to draw a grid
def draw_grid(surface, left=0, top=0):
    for i in range(100):
        x = left + (i % 10) * constants.SQ_SIZE
        y = top + (i // 10) * constants.SQ_SIZE
        square = pygame.Rect(x, y, constants.SQ_SIZE, constants.SQ_SIZE)
        pygame.draw.rect(surface, constants.GREEN, square, width=3)


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
    p1 = Player()
    p2 = Player()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2 = n.send(p1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        SHOT_TRACKER.fill(constants.BLACK)
        SHIP_TRACKER.fill(constants.BLACK)

        draw_grid(SHOT_TRACKER)
        draw_grid(SHIP_TRACKER)
        draw_ships(p1, SHIP_TRACKER)

    redraw_screen(SCREEN, SHOT_TRACKER, SHIP_TRACKER)

    # Debugging output to verify the drawing process
    print("Redrawing screen")
    print(f"Player 1 Ships: {[(ship.name, ship.row, ship.col) for ship in p1.ships.values()]}")

    pygame.quit()

if __name__ == "__main__":
    main()
