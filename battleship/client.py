# battleship/client.py
import asyncio
from battleship import bsp
from log import logger
from networking import network


class Client:
    def __init__(self, client_num):
        # Client initialization
        self.log = logger.Logger(self.__class__.__name__)
        self.running = True

        # Player information
        self.player = bsp.Player()

        # Port connections for LAN
        self.s = None
        self.net = network.Network((f'127.0.0.{client_num}', 65432), is_server=False)

    async def start_client(self):
        while self.running:
            for i in range(5):
                self.log.log_info('start_client', f'Attempt {i + 1} to connect to {self.net.host_port}')
                reader, writer = await self.net.client_connects()
                if writer:
                    self.s = (reader, writer)
                    self.log.log_info('start_client', f'Successfully connected to {self.net.host_port} on attempt {i + 1}')
                    break
                self.log.log_warning('start_client', f'Connection attempt {i + 1} failed')
                await asyncio.sleep(2)

            if not self.s:
                self.log.log_error('start_client', 'Failed to connect to the server')
                self.running = False
                return

    async def data_transfer(self, data):
        if self.s:
            reader, writer = self.s
            try:
                writer.write(data)
                await writer.drain()
                self.log.log_info('data_transfer', 'Data sent successfully')

                received_data = await reader.read(4096)
                self.log.log_info('data_transfer', f'Data received: {received_data}')
                return received_data

            except Exception as e:
                self.log.log_error('data_transfer', f'Transfer error: {e}')
                return None

if __name__ == "__main__":
    client_num = 1
    client = Client(client_num)

    try:
        asyncio.run(client.start_client())
    except KeyboardInterrupt:
        client.running = False
