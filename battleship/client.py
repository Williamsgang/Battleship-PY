# battleship/client.py
import asyncio

from battleship import bsp
from log.logger import Logger
from networking.network import Network


class Client:
    def __init__(self, client_num):
        self.log = Logger(self.__class__.__name__)
        self.running = True
        self.player = bsp.Player()
        self.s = None
        self.net = Network((f'127.0.0.{client_num}', 65433), is_server=False)

    async def start_client(self):
        await self.net.start_client()

    async def data_transfer(self, data):
        if self.s:
            reader, writer = self.s
            try:
                received_data = await self.net.data_transfer(reader, writer, data)
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
