# main.py
# Entry point for the Battleship game.

import tkinter as tk
from client.gui import BattleshipClientGUI
from server.gui import BattleshipServerGUI

def start_server():
    root = tk.Tk()
    server_gui = BattleshipServerGUI(root)
    root.mainloop()

def start_client():
    root = tk.Tk()
    client_gui = BattleshipClientGUI(root)
    root.mainloop()

if __name__ == "__main__":
    # TODO: Add code to choose between starting a server or a client.
    start_server()  # or start_client()
