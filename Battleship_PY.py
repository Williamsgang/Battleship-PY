import pygame
from game.Battleships import Battleships
from game.Boards import Boards
from game.Players import Players
from lib import Colors

"""
Welcome to Battleship-PY!
A basic program to get into Python coding!
"""

"""
__________         __    __  .__                .__    .__        
\______   \_____ _/  |__/  |_|  |   ____   _____|  |__ |__|_____  
 |    |  _/\__  \   __\   __\  | _/ __ \ /  ___/  |  \|  \____ \ 
 |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   Y  \  |  |_> >
 |______  /(____  /__|  |__| |____/\___  >____  >___|  /__|   __/ 
        \/      \/                     \/     \/     \/   |__|    
"""

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30
BOARD_RECTS = {}

# This sets the margin between each cell
MARGIN = 15

# Calculate the total size considering the cells and the margins
WINDOW_SIZE = [720, 720]

game_over = False  # <=========== Change to false when game is built
ship_count = 5  # <=========== Change to player input
board_size = 10  # <=========== Change to player input
player_num = 1  # <=========== Change to player input
players = []  # <=========== Based on player_num value

player = Players(ship_count)
print(player.new_player(0))

player_obj = Players(ship_count)
player_obj.create_players(player_num)

players = player_obj.get_players()

boards_obj = Boards(board_size, ship_count, players)
boards_obj.create_boards(players)

battleships_obj = Battleships(board_size, ship_count, player_num)
battleships_obj.set_ship_locations(players)
battleships_obj.get_ship_locations(players)

boards_obj.print_board(players)


def rect_drawing(screen, color, row, column):
    return pygame.draw.rect(screen, color,
                            [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])


def debug_information(players, BOARD_RECTS):
    print('Testing debug information')
    player_obj.player_debug_information(players)
    battleships_obj.check_ship_locations(players, BOARD_RECTS)


# Main game function
def game(game_done, window_size):
    player_obj.get_players()
    battleships_obj.get_ship_locations(players)
    # Initialize Pygame
    pygame.init()

    screen = pygame.display.set_mode(window_size)

    # Set title of screen
    pygame.display.set_caption("Battleship-PY")

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not game_done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                game_done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if the click happened on any of the rects
                for (row, column), rect in BOARD_RECTS.items():
                    if rect.collidepoint(event.pos):  # Use event.pos, not mouse_pos
                        if battleships_obj.is_ship_location(players, (row, column)):
                            print(f'Button clicked @ {(row, column)}, ship located.')
                            color = Colors.GREEN
                        else:
                            print(f'Button clicked @ {(row, column)}, no ship located.')

        # Set the screen background
        screen.fill(Colors.WHITE)
        # Get mouse pos()
        mouse_pos = pygame.mouse.get_pos()

        # Draw the grid
        for row in range(board_size):
            for column in range(board_size):
                color = Colors.BLACK
                grid_square = rect_drawing(screen, color, row, column)
                BOARD_RECTS[(row, column)] = grid_square

        # Check if the mouse is over any of the rects
        for (row, column), rect in BOARD_RECTS.items():
            if rect.collidepoint(mouse_pos):
                color = Colors.RED
            elif battleships_obj.is_ship_location(players, (row, column)):
                color = Colors.BLUE
            else:
                color = Colors.BLACK
            rect_drawing(screen, color, row, column)

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()


game(game_over, WINDOW_SIZE)
debug_information(players, BOARD_RECTS)
# print(f'Board locations: {BOARD_RECTS}')



# FINISHED: Multiple ships: Instead of just one battleship, you can have multiple ships of different sizes placed randomly on the board.
# TODO: Visual representation: Use ASCII art or graphical elements to represent the ships and the ocean visually.
# TODO: AI opponent: Create an AI opponent for single-player mode, where the player competes against the computer to sink each other's ships.
# TODO: Customizable ship placement: Let the player manually place their ships on the board before starting the game.
# TODO: Historical tracking: Keep track of the player's performance over multiple games, such as wins, losses, and high scores.
# TODO: Sound effects and music: Add sound effects for hits, misses, sinking ships, and background music to enhance the gaming experience.
# TODO: Animations: Include animations for ship movements, explosions when a ship is sunk, or effects when a player makes a successful guess.
# TODO: Multiplayer mode: Enable multiplayer functionality, allowing two players to compete against each other on separate boards.
# TODO: Time limit: Add a time limit for each turn to increase the tension and challenge for the player.
# TODO: Tutorial mode: Provide a tutorial mode that guides the player through the game mechanics and strategies.
