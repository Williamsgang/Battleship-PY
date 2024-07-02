# Battleship Game

## Description:
A networked Battleship game with a graphical interface, animations, and user statistics. The game can be played over a LAN.

## Features:
- Graphical interface for both server and client
- User statistics tracking (kills, wins, losses)
- Admin panel to manage users
- Placeholder for animations and settings
- Logging of all game events and actions

## File Structure:
- `assets/`: Directory for image and sound assets
- `client/`: Client-side code
  - `client.py`: Main client logic
  - `socket development`: "https://realpython.com/python-sockets/"
- `config/`: Configuration files
  - `settings.json`: Game and network settings
  - `settings.py`: Calls for network settings
- `logs/`: 
  - `logs/`: Holds all generated logs from all files
  - `logger.py`: Base class that logs all information
- `networking/`: Overall networking code
  - `events.py`: Holds overall events and event handlers
  - `game_rules.py`: Maintains the game rules
  - `network.py`: Creates the main net framework 
- `server/`: Server-side code
  - `server.py`: Main server logic
- `shared/`
- `main.py`: Entry point for the game

## TODOs
- Implement game logic for special attack moves
- Add animations for attacks and ship movements
- Expand the settings panel with more options
- Improve GUI design and functionality

## Running the Game:
1. Start the server:
    ```sh
    python main.py
    ```
2. Start each client:
    ```sh
    python main.py
    ```


## Credits
  ```python
    # Credit to Coding Cassowary from his Battleship AI
    # for a more stable way of creating ships and boards
    # along with players. 
    
    # https://www.youtube.com/@codingcassowary6391
  ```