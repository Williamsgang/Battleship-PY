# battleship/server.py
import pickle
import asyncio
from typing import Tuple

from networking import network
from log import logger


class Server:
    def __init__(self, host_port: Tuple[str, int] = None):
        """
        :type host_port: Tuple[str, int]:
        :type is_server: bool:
        :type is_running: bool:
        """
        # Logger to map issues and log all necessary details
        self.log = logger.Logger(self.__class__.__name__)

        # Game information
        self.players = []

        # Server and client connections and necessary variables
        if host_port is None:
            self.host_port = ('127.0.0.1', 65432)
        else:
            self.host_port = host_port

        self.net = network.Network(self.host_port, is_server=True)
        self.running = True

    async def start_server(self):
        self.log.log_info('start_server', 'Starting server...')
        self.log.log_info('start_server', f'Server started on {self.host_port[0]}:{self.host_port[1]}')

        async def handle_client(reader, writer):
            addr = writer.get_extra_info('peername')
            self.log.log_info('start_server', f'Connected by {addr}')

            writer.write(pickle.dumps(b'Hello World'))
            await writer.drain()

            while self.running:
                try:
                    data = await reader.read(100)
                    if data:
                        decoded_data = pickle.loads(data)
                        print(f'Received data: {decoded_data}')
                        self.log.log_info('start_server', f'Received data: {decoded_data}')
                    else:
                        self.log.log_warning('start_server', 'No data received, connection might be closed')
                        break
                except Exception as e:
                    self.log.log_error('start_server', f'Error on receive: {e}')
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


if __name__ == "__main__":
    host_port = ('127.0.0.1', 65432)
    server = Server(host_port)

    try:
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        server.stop_server()
