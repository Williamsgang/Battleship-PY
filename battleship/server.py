# battleship/server.py
import asyncio
import pickle
from typing import Tuple, Dict, Any

from log.logger import Logger
from networking.network import Network


class Server:
    def __init__(self, host_port: Tuple[str, int] = None):
        self.log = Logger(self.__class__.__name__)
        self.players = {}
        self.host_port = host_port or ('127.0.0.1', 65433)
        self.net = Network(self.host_port, is_server=True)
        self.running = True
        self.game_state = {}

    async def start_server(self):
        self.log.log_info('start_server', 'Starting server...')
        self.log.log_info('start_server', f'Server started on {self.host_port[0]}:{self.host_port[1]}')

        async def handle_client(reader, writer):
            addr = writer.get_extra_info('peername')
            self.log.log_info('handle_client', f'Connected by {addr}')
            self.players[addr] = writer

            writer.write(pickle.dumps(b'Welcome to Battleship!'))
            await writer.drain()

            while self.running:
                try:
                    data = await reader.read(100)
                    if data:
                        command = pickle.loads(data)
                        response = await self.process_command(addr, command)
                        writer.write(pickle.dumps(response))
                        await writer.drain()
                    else:
                        self.log.log_warning('handle_client', 'No data received, connection might be closed')
                        break
                except Exception as e:
                    self.log.log_error('handle_client', f'Error on receive: {e}')
                    break

            writer.close()
            await writer.wait_closed()
            del self.players[addr]

        server = await asyncio.start_server(handle_client, *self.host_port)
        async with server:
            await server.serve_forever()

    def stop_server(self):
        self.log.log_info('stop_server', 'Stopping server...')
        self.running = False
        self.log.log_info('stop_server', 'Server stopped')

    async def process_command(self, addr, command: Dict[str, Any]):
        cmd = command.get("cmd")
        if cmd == "shoot":
            return self.handle_shoot(addr, command.get("x"), command.get("y"))
        if cmd == "player_boards":
            self.handle_show_player_boards()
        return {"status": "unknown command"}

    def handle_shoot(self, addr, x: int, y: int):
        # Logic for handling a shot at coordinates (x, y)
        target = self.get_opponent(addr)
        if not target:
            return {"status": "no opponent"}

        # Game logic to check hit or miss
        hit = (x, y) in self.game_state.get(target, [])
        result = "hit" if hit else "miss"
        return {"status": result, "x": x, "y": y}

    def handle_show_player_boards(self):
        players = self.players

        for player in players:
            print(f'Player _insert_player_num_ ship tracker')
            print('============================================\n')
            for row in player.ship_tracker:
                print(row)
            print('============================================\n')

    def get_opponent(self, addr):
        for player in self.players:
            if player != addr:
                return player
        return None
