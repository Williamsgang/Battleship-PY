import asyncio
import signal
import sys
import threading

from battleship.client import Client
from battleship.server import Server

shutdown_event = threading.Event()


def start_server():
    server = Server()

    async def run_server():
        await server.start_server()

    def listen_for_keypress():
        import keyboard
        while not shutdown_event.is_set():
            if keyboard.is_pressed('q'):
                server.stop_server()
                shutdown_event.set()

    def signal_handler(sig, frame):
        shutdown_event.set()
        server.stop_server()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    keypress_thread = threading.Thread(target=listen_for_keypress)
    keypress_thread.start()

    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        server.stop_server()
    finally:
        shutdown_event.set()
        keypress_thread.join()


def start_client():
    client = Client(1)

    async def run_client():
        await client.net.start_client()

    def listen_for_keypress():
        import keyboard
        while not shutdown_event.is_set():
            if keyboard.is_pressed('q'):
                client.net.disconnect()
                shutdown_event.set()

    def signal_handler(sig, frame):
        shutdown_event.set()
        client.net.disconnect()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    keypress_thread = threading.Thread(target=listen_for_keypress)
    keypress_thread.start()

    try:
        asyncio.run(run_client())
    except KeyboardInterrupt:
        client.net.disconnect()
    finally:
        shutdown_event.set()
        keypress_thread.join()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        start_server()
    else:
        start_client()
