# main.py
# Entry point for the Battleship game.

import sys
import keyboard
import threading
import signal

from client import client
from server.server import BattleshipServer

shutdown_event = threading.Event()


def start_server():
    server = BattleshipServer()

    # Function to listen for the 'q' keypress to stop the server
    def listen_for_keypress():
        import keyboard
        while not shutdown_event.is_set():
            if keyboard.is_pressed('q'):
                server.stop_server()
                shutdown_event.set()

    # Handle termination signals
    def signal_handler(sig, frame):
        server.stop_server()
        shutdown_event.set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start the keypress listener in a separate thread
    keypress_thread = threading.Thread(target=listen_for_keypress)
    keypress_thread.start()

    # Start the server (this will block the main thread)
    server.start_server()

    # Wait for the shutdown event before exiting
    shutdown_event.wait()
    # TODO: Add functionality to this


def start_client():
    # Function to listen for the 'q' keypress to stop the server
    def listen_for_keypress():
        keyboard.wait('q')
        client.net.disconnect()

    # Handle termination signals
    def signal_handler(sig, frame):
        client.net.disconnect()
        shutdown_event.set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start the keypress listener in a separate thread
    keypress_thread = threading.Thread(target=listen_for_keypress)
    keypress_thread.start()

    client = client.BattleshipClient()
    client.net.connect()
    # TODO: Add functionality to this


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        start_server()
    else:
        start_client()
    # TODO: Add code to choose between starting a server or a client.
