# battleship/client.py
import asyncio
import pickle

from log.logger import Logger
from networking.network import Network


class Client:
    def __init__(self, client_num):
        self.log = Logger(self.__class__.__name__)
        self.running = True
        self.net = Network((f'127.0.0.{client_num}', 65433), is_server=False)
        self.reader = None
        self.writer = None

    async def start_client(self):
        reader, writer = await self.net.client_connects()
        if not writer:
            return

        self.reader, self.writer = reader, writer
        self.log.log_info('start_client', 'Connected to server')

        await asyncio.gather(self.handle_user_input(), self.handle_server_response())

    async def send_command(self, command):
        self.writer.write(pickle.dumps(command))
        await self.writer.drain()

    def disconnect(self):
        self.net.disconnect()

    async def handle_user_input(self):
        while self.running:
            command = await asyncio.get_event_loop().run_in_executor(None, input, "Enter command: ")
            if command.startswith("shoot"):
                _, x, y = command.split()
                await self.send_command({"cmd": "shoot", "x": int(x), "y": int(y)})
            elif command.startswith("show_boards"):
                _, player = command.split()
                await self.send_command({"cmd": "show_boards", "player": player.ship_tracker})
            elif command == "exit":
                self.running = False
                self.disconnect()
            else:
                print("Unknown command")

    async def handle_server_response(self):
        while self.running:
            try:
                response_data = await self.reader.read(100)
                if response_data:
                    response = pickle.loads(response_data)
                    print(f"Response: {response}")
                else:
                    print("Server closed connection")
                    self.running = False
            except Exception as e:
                print(f"Error receiving data: {e}")
                self.running = False


if __name__ == "__main__":
    client_num = 1
    client = Client(client_num)
    try:
        asyncio.run(client.start_client())
    except KeyboardInterrupt:
        client.disconnect()
