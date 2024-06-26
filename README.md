# Battleship Game

## Description
A networked Battleship game with a graphical interface, animations, and user statistics. The game can be played over a LAN.

## Features
- Graphical interface for both server and client
- User statistics tracking (kills, wins, losses)
- Admin panel to manage users
- Placeholder for animations and settings
- Logging of all game events and actions

## File Structure
- `assets/`: Directory for image and sound assets
- `client/`: Client-side code
  - `client.py`: Main client logic
  - `gui.py`: Client GUI
  - `game_logic.py`: Client-side game logic
  - `animations.py`: Client-side animations
  - `settings.py`: Client-side settings panel
  - `network.py`: Client-side network communication
  - `player.py`: Client-side player information
  - `logger.py`: Client-side logging
- `server/`: Server-side code
  - `server.py`: Main server logic
  - `game_logic.py`: Server-side game logic
  - `network.py`: Server-side network communication
  - `player.py`: Server-side player information management
  - `logger.py`: Server-side logging
  - `gui.py`: Server GUI
- `config/`: Configuration files
  - `settings.json`: Game and network settings
- `main.py`: Entry point for the game

## TODOs
- Implement game logic for special attack moves
- Add animations for attacks and ship movements
- Expand the settings panel with more options
- Improve GUI design and functionality

## Running the Game
1. Start the server:
    ```sh
    python main.py
    ```
2. Start each client:
    ```sh
    python main.py
    ```

3. Enter the server's IP address and click "Connect". You can also click "Show Stats" to view user statistics, "Settings" to open the settings panel, and "Quit Game" to close the application.
