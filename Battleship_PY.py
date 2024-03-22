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

game_over = True # <========= Change to false when game is built 
ship_count = 5 # <=========== Change to player input
board_size = 10 # <========== Change to player input

team1 = {
    "team_num": 1,
    "ship_count": ship_count,
    "ship_locations": [],
    "board": []
    }

team2 = {
    "team_num": 2,
    "ship_count": ship_count,
    "ship_locations": [],
    "board": []
    }

teams = [team1, team2]

def create_boards(teams):
    for team in teams:
        for _ in range(board_size):
            team["board"].append(["O"] * board_size)

# Prints the board when the method is called
def print_board(teams):
    for team in teams:
        for _ in team["board"]: # <============================= FIX THIS LINE =====================================>
            print(" ".join(_))

# Method for randomizing the row value for ships
def random_row(boards):
    return [random.randint(0, len(board) - 1) for board in boards]

# Method for randomizing the column value for ships
def random_col(boards):
    return [random.randint(0, len(board[0]) - 1) for board in boards]
            
# Method to obtain the ship locations within the teams
def get_ship_locations(teams, boards):
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

# Debug for getting each team information
def debug_information(teams):
    for team in teams:
        create_boards(teams)

        print("============================")
        print("Team " + str(team["team_num"]) + " debug information")
        print("Team " + str(team["team_num"]) + " ship count: ", team["ship_count"])
        print("Team " + str(team["team_num"]) + " ship locations: ", team["ship_locations"])
        print("Team " + str(team["team_num"]) + " board: ", team["board"])
        print("============================")
        print()
        
        print_board(team)
        
    # print("Board size")
    # create_boards(boards)
    # print_board(boards)

debug_information(teams)

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