# battleship/server.py
import asyncio
import pickle
from typing import Tuple

from log.logger import Logger
from networking.network import Network


class Server:
    def __init__(self, host_port: Tuple[str, int] = None):
        self.log = Logger(self.__class__.__name__)
        self.players = []
        self.host_port = host_port or ('127.0.0.1', 65433)
        self.net = Network(self.host_port, is_server=True)
        self.running = True

    async def start_server(self):
        self.log.log_info('start_server', 'Starting server...')
        self.log.log_info('start_server', f'Server started on {self.host_port[0]}:{self.host_port[1]}')

        async def handle_client(reader, writer):
            addr = writer.get_extra_info('peername')
            self.log.log_info('handle_client', f'Connected by {addr}')

            writer.write(pickle.dumps(b'Hello World'))
            await writer.drain()

            while self.running:
                try:
                    data = await reader.read(100)
                    if data:
                        decoded_data = pickle.loads(data)
                        self.log.log_info('handle_client', f'Received data: {decoded_data}')
                    else:
                        self.log.log_warning('handle_client', 'No data received, connection might be closed')
                        break
                except Exception as e:
                    self.log.log_error('handle_client', f'Error on receive: {e}')
                    break

            writer.close()
            await writer.wait_closed()

        server = await asyncio.start_server(handle_client, *self.host_port)
        async with server:
            await server.serve_forever()

    def stop_server(self):
        self.log.log_info('stop_server', 'Stopping server...')
        self.running = False
        self.log.log_info('stop_server', 'Server stopped')
