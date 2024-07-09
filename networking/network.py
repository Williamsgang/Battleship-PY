# networking/network.py
import asyncio
from typing import Tuple
from log.logger import Logger

class Network:
    def __init__(self, host_port: Tuple[str, int], is_server=False):
        self.log = Logger(self.__class__.__name__)
        self.host_port = host_port
        self.server = None
        self.is_server = is_server
        self.client_ips = []
        self.clients = []
        self.client_count = 0

        if is_server:
            try:
                asyncio.run(self.start_server())
            except OSError as e:
                if e.errno == 10048:
                    self.log.log_error('init', f'Port {self.host_port[1]} is already in use. Please use a different port.')
                else:
                    self.log.log_error('init', f'Error: {e}')
                raise

    async def start_server(self, host_port=('127.0.0.1', 65432)):
        if self.host_port is None:
            self.host_port = host_port

        try:
            self.server = await asyncio.start_server(self.handle_client, *self.host_port)
            self.log.log_info('start_server', f'Server listening on {self.host_port[0]}:{self.host_port[1]}')

            async with self.server:
                await self.server.serve_forever()
        except OSError as e:
            self.log.log_error('start_server', f'Error: {e}')
            raise

    async def stop_server(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.log.log_info('stop_server', 'Server stopped')

    async def start_client(self):
        self.log.log_info('start_client', f'Client setup on {self.host_port[0]}:{self.host_port[1]}')

        try:
            reader, writer = await asyncio.open_connection(*self.host_port)
            self.client_count += 1
            self.log.log_info('start_client', f'Connected to server at {self.host_port[0]}:{self.host_port[1]}')
            self.reader, self.writer = reader, writer
            await self.handle_client(reader, writer)
        except Exception as e:
            self.log.log_error('start_client', f'Connection error: {e}')

    async def client_connects(self):
        if self.is_server:
            raise RuntimeError("connect can only be called on client instances")
        try:
            reader, writer = await asyncio.open_connection(*self.host_port)
            self.client_count += 1
            self.log.log_info('client_connects', f'Connected to server at {self.host_port[0]}:{self.host_port[1]}')
            return reader, writer
        except Exception as e:
            self.log.log_error('client_connects', f'Connection error: {e}')
            return None, None

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        if self.is_server:
            self.client_ips.append(addr[0])
            self.log.log_info('handle_client', f'Accepted connection from {addr[0]}:{addr[1]}')

        try:
            while True:
                data = await asyncio.wait_for(reader.read(100), timeout=10.0)
                if not data:
                    break
                self.log.log_info('handle_client', f'Received data: {data.decode()}')
                writer.write(data)
                await writer.drain()
        except asyncio.TimeoutError:
            self.log.log_warning('handle_client', 'Connection timed out')
        except asyncio.CancelledError:
            self.log.log_warning('handle_client', 'Connection cancelled')
        except Exception as e:
            self.log.log_error('handle_client', f'Error: {e}')
        finally:
            self.log.log_info('handle_client', f'Connection closed from {addr[0]}:{addr[1]}')
            writer.close()
            await writer.wait_closed()

    async def data_transfer(self, reader, writer, data):
        try:
            writer.write(data)
            await writer.drain()
            self.log.log_info('data_transfer', 'Data sent successfully')

            received_data = await reader.read(4096)
            self.log.log_info('data_transfer', f'Data received: {received_data.decode()}')
            return received_data

        except Exception as e:
            self.log.log_error('data_transfer', f'Transfer error: {e}')
            return None

    def disconnect(self):
        if self.writer:
            self.writer.close()
            asyncio.run(self.writer.wait_closed())
            self.log.log_info('disconnect', 'Disconnected from server')
