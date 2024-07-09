# main.py
import signal
import sys
import threading

from battleship.server import Server
from networking import network

# is_running = True
#
# player1 = bsp.Player()
# player2 = bsp.Player()
#
# print("Player 1's ships:")
# print(f"Player 1 ship count: {player1.ship_tracker.count_ships(player1)}")
#
# player1.show_ships(player1)
#
# print()
# print('===============================')
# print()
#
# print("Player 2's ships:")
# print(f"Player 2 ship count: {player2.ship_tracker.count_ships(player2)}")
#
# player2.show_ships(player2)
#
# players = [player1, player2]

shutdown_event = threading.Event()


def start_server():
    server = Server()

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


def start_client():
    pass


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        start_server()
    else:
        start_client()
