# client/gui.py
# GUI for the Battleship client.

import tkinter as tk
from tkinter import messagebox
from .animations import AnimationManager
from .settings import SettingsPanel

class BattleshipClientGUI:
    def __init__(self, client):
        self.client = client
        self.root = tk.Tk()
        self.root.title("Battleship Client")
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(padx=10, pady=10)

        self.board_buttons = [[tk.Button(self.board_frame, text="X", width=2, height=1,
                                         command=lambda x=i, y=j: self.attack(x, y))
                               for j in range(10)] for i in range(10)]

        for i in range(10):
            for j in range(10):
                self.board_buttons[i][j].grid(row=i, column=j)

        self.server_ip_label = tk.Label(self.root, text="Server IP:")
        self.server_ip_label.pack(pady=5)

        self.server_ip_entry = tk.Entry(self.root)
        self.server_ip_entry.pack(pady=5)

        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect_to_server)
        self.connect_button.pack(pady=5)

        self.stats_button = tk.Button(self.root, text="Show Stats", command=self.request_stats)
        self.stats_button.pack(pady=5)

        self.settings_button = tk.Button(self.root, text="Settings", command=self.open_settings)
        self.settings_button.pack(pady=5)

        self.quit_button = tk.Button(self.root, text="Quit Game", command=self.root.quit)
        self.quit_button.pack(pady=5)

        self.animation_manager = AnimationManager(self)

    def connect_to_server(self):
        # TODO: Implement connection to server logic.
        pass

    def attack(self, x, y):
        # TODO: Implement attack logic.
        pass

    def update_board(self, position, result):
        # TODO: Update the board with the result of an attack.
        pass

    def log_message(self, message):
        messagebox.showinfo("Game Info", message)

    def request_stats(self):
        # TODO: Request statistics from the server.
        pass

    def open_settings(self):
        SettingsPanel(self.root)

    def start(self):
        self.root.mainloop()
