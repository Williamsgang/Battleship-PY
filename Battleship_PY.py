import random

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

game_over = True # <=========== Change to false when game is built 
ship_count = 5   # <=========== Change to player input
board_size = 5   # <=========== Change to player input
player_num = 2   # <=========== Change to player input
players = []     # <=========== Based on player_num value

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
def print_board(boards):
    return "Not implemented yet"

# Method for randomizing the row value for ships                            <======================= FINISH THIS ==============================
def random_row(board):
    return [random.randint(0, len(row["board"]) - 1) for row in board]

# Method for randomizing the column value for ships
def random_col(board):
    return [random.randint(0, len(col["board"][0]) - 1) for col in board]
            
# Method to obtain the ship locations within the teams
def get_ship_locations(ship_count, players):
    for player in players:
        for ship in range(ship_count):
            random_row(player["ship_locations"])
            random_col(player["ship_locations"])

    return "Not implemented yet"

# TODO: Obtain the ship locations for each team



# TODO: Game continuous logic
# while game_over != True:
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

def debug_information(player_num, players):
    print('Testing debug information')
    player_debug_information(players)


create_players(player_num, players)
create_boards(players)
debug_information(player_num, players)

"""
TODO: Multiple ships: Instead of just one battleship, you can have multiple ships of different sizes placed randomly on the board.
TODO: Ship sizes: Introduce ships of different sizes (e.g., battleship, destroyer) and allow the player to sink each ship by hitting all of its segments.
TODO: Player feedback: Provide more detailed feedback to the player after each turn, such as "You're getting closer!" or "You're far off the mark!"
TODO: Difficulty levels: Implement different difficulty levels (easy, medium, hard) by adjusting factors like the number of ships, the size of the board, or the number of turns allowed.
TODO: Power-ups: Add power-ups that give the player advantages, such as extra guesses, revealing nearby ship locations, or clearing a row or column.
TODO: Visual representation: Use ASCII art or graphical elements to represent the ships and the ocean visually.
TODO: AI opponent: Create an AI opponent for single-player mode, where the player competes against the computer to sink each other's ships.
TODO: Customizable board size: Allow the player to choose the size of the board before starting the game.
TODO: Customizable ship placement: Let the player manually place their ships on the board before starting the game.
TODO: Historical tracking: Keep track of the player's performance over multiple games, such as wins, losses, and high scores.
TODO: Sound effects and music: Add sound effects for hits, misses, sinking ships, and background music to enhance the gaming experience.
TODO: Animations: Include animations for ship movements, explosions when a ship is sunk, or effects when a player makes a successful guess.
TODO: Multiplayer mode: Enable multiplayer functionality, allowing two players to compete against each other on separate boards.
TODO: Time limit: Add a time limit for each turn to increase the tension and challenge for the player.
TODO: Tutorial mode: Provide a tutorial mode that guides the player through the game mechanics and strategies.
"""