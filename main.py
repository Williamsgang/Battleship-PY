# main.py
# Entry point for the Battleship game.

import sys
from server.gui import BattleshipServerGUI
from server.server import BattleshipServer

def start_server():
    server = BattleshipServer()
    gui = BattleshipServerGUI(server)
    gui.run()

def start_client():
    # Assuming the client GUI uses pygame as well, following similar restructuring
    from client.gui import BattleshipClientGUI
    client = None  # Replace with actual client object
    gui = BattleshipClientGUI(client)
    gui.run()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        start_server()
    else:
        start_client()
    # TODO: Add code to choose between starting a server or a client.