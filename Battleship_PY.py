from math import e
from os import close
import random
import pygame

"""
Welcome to Battleship-PY!
A basic program to get into Python coding!
"""

print(
    """

__________         __    __  .__                .__    .__        
\______   \_____ _/  |__/  |_|  |   ____   _____|  |__ |__|_____  
 |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___/  |  \|  \____ \ 
 |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   Y  \  |  |_> >
 |______  /(____  /__|  |__| |____/\___  >____  >___|  /__|   __/ 
        \/      \/                     \/     \/     \/   |__|    

"""
)
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30
BOARD_RECTS = {}

# This sets the margin between each cell
MARGIN = 15

# Calculate the total size considering the cells and the margins
WINDOW_SIZE = [(WIDTH + MARGIN) * 10 + MARGIN, (HEIGHT + MARGIN) * 10 + MARGIN]

game_over = False  # <=========== Change to false when game is built
ship_count = 5  # <=========== Change to player input
board_size = 10  # <=========== Change to player input
player_num = 2  # <=========== Change to player input
players = []  # <=========== Based on player_num value


def new_player(num):
    player = {
        "player_num": num,
        "ship_count": ship_count,
        "ship_locations": [],
        "board": []
    }
    return player


def create_players(player_num, players):
    for num in range(player_num):
        players.append(new_player(num + 1))


def create_boards(players):
    for player in players:
        for num in range(board_size):
            player['board'].append(["O"] * board_size)


# Prints the board when the method is called
def print_board(players):
    for player in players:
        print("Player " + str(player["player_num"]) + "'s board:")
        for row in player["board"]:
            print(" ".join(row))
        print("=============================")


# Method for randomizing the row value for ships
def random_row(board):
    return random.randint(0, len(board) - 1)


# Method for randomizing the column value for ships
def random_col(board):
    return random.randint(0, len(board[0]) - 1)


# Method to obtain the ship locations within the teams
def get_ship_locations(players):
    for player in players:
        for ship in range(player["ship_count"]):
            ship_row = random_row(player["board"])
            ship_col = random_col(player["board"])
            # Prints board with the 'X' to show locations
            while player["board"][ship_row][ship_col] != "O":
                ship_row = random_row(player["board"])
                ship_col = random_col(player["board"])
            player["board"][ship_row][ship_col] = "X"
            player["ship_locations"].append((ship_row, ship_col))


# TODO: User input for the coordinates
# TODO: Logic for guesses to hit the ship
# TODO: Logic for boundaries
# TODO: Logic for previously hit locations
# TODO: Logic for misses
# TODO print the board after every shot


# Debug for getting each player information
def player_debug_information(players):
    for player in players:
        print("==================================")
        print("")
        print(f"Player {player['player_num']}:")
        for key, value in player.items():
            print(f"{key}: {value}")
        print("")


def check_ship_locations(players, BOARD_RECTS):
    for player in players:
        print(f"Player {player['player_num']}'s info: ")
        for ship_location in player["ship_locations"]:
            if ship_location in BOARD_RECTS:
                print(f"Ship located at {ship_location}")
            else:
                print(f"No ship at {ship_location}")


# Prints player game function
def debug_information(player_num, players, BOARD_RECTS):
    print('Testing debug information')
    player_debug_information(players)
    check_ship_locations(players, BOARD_RECTS)


def rect_drawing(screen, color, row, column):
    return pygame.draw.rect(screen, color,
                            [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])


# Main game function
def game(game_done, window_size, player_num, players):
    new_player(player_num)
    create_players(player_num, players)
    create_boards(players)
    get_ship_locations(players)
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
                        print('Button clicked @ ', (row, column))

        # Set the screen background
        screen.fill(BLACK)
        # Get mouse pos()
        mouse_pos = pygame.mouse.get_pos()

        # Draw the grid
        for row in range(board_size):
            for column in range(board_size):
                color = WHITE
                grid_square = rect_drawing(screen, color, row, column)
                BOARD_RECTS[(row, column)] = grid_square

        # Check if the mouse is over any of the rects
        for (row, column), rect in BOARD_RECTS.items():
            if rect.collidepoint(mouse_pos):
                color = RED
            else:
                color = WHITE
            rect_drawing(screen, color, row, column)

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()


game(game_over, WINDOW_SIZE, player_num, players)
debug_information(player_num, players, BOARD_RECTS)
# print(f'Board locations: {BOARD_RECTS}')


# FINISHED: Multiple ships: Instead of just one battleship, you can have multiple ships of different sizes placed randomly on the board.
# TODO: Ship sizes: Introduce ships of different sizes (e.g., battleship, destroyer) and allow the player to sink each ship by hitting all of its segments.
# TODO: Player feedback: Provide more detailed feedback to the player after each turn, such as "You're getting closer!" or "You're far off the mark!"
# TODO: Difficulty levels: Implement different difficulty levels (easy, medium, hard) by adjusting factors like the number of ships, the size of the board, or the number of turns allowed.
# TODO: Power-ups: Add power-ups that give the player advantages, such as extra guesses, revealing nearby ship locations, or clearing a row or column.
# TODO: Visual representation: Use ASCII art or graphical elements to represent the ships and the ocean visually.
# TODO: AI opponent: Create an AI opponent for single-player mode, where the player competes against the computer to sink each other's ships.
# TODO: Customizable board size: Allow the player to choose the size of the board before starting the game.
# TODO: Customizable ship placement: Let the player manually place their ships on the board before starting the game.
# TODO: Historical tracking: Keep track of the player's performance over multiple games, such as wins, losses, and high scores.
# TODO: Sound effects and music: Add sound effects for hits, misses, sinking ships, and background music to enhance the gaming experience.
# TODO: Animations: Include animations for ship movements, explosions when a ship is sunk, or effects when a player makes a successful guess.
# TODO: Multiplayer mode: Enable multiplayer functionality, allowing two players to compete against each other on separate boards.
# TODO: Time limit: Add a time limit for each turn to increase the tension and challenge for the player.
# TODO: Tutorial mode: Provide a tutorial mode that guides the player through the game mechanics and strategies.

