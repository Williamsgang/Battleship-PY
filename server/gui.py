# server/gui.py
# GUI for the Battleship server.

import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from .server import BattleshipServer
from client.settings import SettingsPanel

class BattleshipServerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Battleship Server")

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=10)

        self.admin_button = tk.Button(master, text="Admin Panel", command=self.open_admin_panel)
        self.admin_button.pack(pady=5)

        self.settings_button = tk.Button(master, text="Settings", command=self.open_settings)
        self.settings_button.pack(pady=5)

        self.quit_button = tk.Button(master, text="Quit Game", command=master.quit)
        self.quit_button.pack(pady=5)

        self.server = BattleshipServer()
        threading.Thread(target=self.server.start).start()

    def log_message(self, message):
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)

    def open_admin_panel(self):
        AdminPanel(self.master, self.server)

    def open_settings(self):
        SettingsPanel(self.master)

class AdminPanel:
    def __init__(self, master, server):
        self.server = server
        self.top = tk.Toplevel(master)
        self.top.title("Admin Panel")

        self.ip_label = tk.Label(self.top, text="Enter IP to set as Admin:")
        self.ip_label.pack(pady=5)

        self.ip_entry = tk.Entry(self.top)
        self.ip_entry.pack(pady=5)

        self.set_admin_button = tk.Button(self.top, text="Set Admin", command=self.set_admin)
        self.set_admin_button.pack(pady=10)

        self.stats_button = tk.Button(self.top, text="Show Stats", command=self.show_stats)
        self.stats_button.pack(pady=10)

    def set_admin(self):
        ip = self.ip_entry.get()
        self.server.set_admin(ip)
        messagebox.showinfo("Admin Panel", f"{ip} has been set as the admin.")

    def show_stats(self):
        stats = "\n".join([f"{ip}: {data}" for ip, data in self.server.player_manager.players.items()])
        messagebox.showinfo("User Stats", stats)

class SettingsPanel:
    def __init__(self, master):
        self.top = tk.Toplevel(master)
        self.top.title("Settings")
        # TODO: Add settings options here.
