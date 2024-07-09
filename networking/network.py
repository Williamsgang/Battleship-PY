import asyncio
from typing import Tuple
from log import logger


class Network:
    def __init__(self, host_port: Tuple[str, int], is_server=False):
        # Initialization of the network and determining logic
        self.log = logger.Logger(self.__class__.__name__)
        self.host_port = host_port
        self.server = None
        self.is_server = is_server

        # Connections and clients
        self.client_ips = []
        self.clients = []
        self.client_count = 0

        for ip in self.client_ips:
            self.clients.append(
                {
                    'ip': ip,
                    'client_num': self.client_ips.index(ip)
                }
            )

        for client in self.clients:
            print(f'Client num: {client["client_num"]}, '
                  f'Client ip: {client["ip"]}')

        if is_server:
            asyncio.run(self.start_server())
        else:
            asyncio.run(self.start_client())

    async def start_server(self, host_port=('127.0.0.1', 65432)):
        if self.host_port is None:
            self.host_port = host_port

        self.server = await asyncio.start_server(self.handle_client, *self.host_port)
        self.log.log_info('setup_server', f'Server listening on {self.host_port[0]}:{self.host_port[1]}')

        async with self.server:
            await self.server.serve_forever()

    async def stop_server(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.log.log_info('stop_server', 'Server stopped')

    async def start_client(self):
        self.log.log_info('setup_client',
                          f'Client setup on {self.host_port[0]}:{self.host_port[1]}')

    async def client_connects(self):
        if self.is_server:
            raise RuntimeError("connect can only be called on client instances")
        try:
            reader, writer = await asyncio.open_connection(*self.host_port)
            self.client_count += 1
            self.log.log_info('connect', f'Connected to server at {self.host_port[0]}:{self.host_port[1]}')
            return reader, writer
        except Exception as e:
            self.log.log_error('connect', f'Connection error: {e}')
            return None, None

    def get_clients(self):
        pass

    async def accept_conn(self):
        raise NotImplementedError("Use start_server to accept connections")

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        self.client_ips.append(addr[0])
        self.log.log_info('accept_conn', f'Accepted connection from {addr[0]}:{addr[1]}')

        while True:
            data = await reader.read(100)
            if not data:
                break
            self.log.log_info('handle_client', f'Received data: {data.decode()}')
            writer.write(data)
            await writer.drain()

        self.log.log_info('handle_client', f'Connection closed from {addr[0]}:{addr[1]}')
        writer.close()
        await writer.wait_closed()

    async def data_transfer(self, writer, data):
        try:
            writer.write(data)
            await writer.drain()
            self.log.log_info('data_transfer', 'Data sent successfully')

            # If you expect a response, you can read from the reader
            received_data = await reader.read(4096)

        except Exception as e:
            self.log.log_error('data_transfer', f'Transfer error: {e}')
