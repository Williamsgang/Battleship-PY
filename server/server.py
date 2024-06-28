# server/server.py
# Main server logic for the Battleship game.

import socket

from logs import logger
from networking import network


class BattleshipServer:
    def __init__(self):
        self.running = True
        self.host = "127.0.0.1"
        self.port = 65432
        self.log = logger.Logger(self.__class__.__name__)
        self.net = network.Network(self.host, self.port, is_server=True)
        self.log.log_info('__init__', 'Server initialized')
        # TODO: Add methods for handling game logic, client communication, etc.

    def start_server(self):
        self.log.log_info('start_server', 'Starting server...')
        self.net.accept_conn()
        print(f'Server started on {self.host}:{self.port}')
        self.log.log_info('start_server', f'Server started on {self.host}:{self.port}')

        while self.running:
            try:
                conn, addr = self.net.accept_conn()
                if conn is None:
                    self.log.log_warning('start_server', 'No connection accepted')
                    break
                print(f'Connected by {addr}')
                self.log.log_info('start_server', f'Connected by {addr}')
                while self.running:
                    try:
                        data = self.net.receive_data(conn)
                        if data:
                            print(f'Received data: {data}')
                            self.log.log_info('start_server', f'Received data: {data}')
                        else:
                            self.log.log_warning('start_server', 'No data received, connection might be closed')
                            break
                    except socket.error as se:
                        self.log.log_error('start_server', f'Socket error on receive: {se}')
                        break
            except socket.error as se:
                self.log.log_error('start_server', f'Socket error on accept: {se}')
                self.running = False

    def stop_server(self):
        self.log.log_info('stop_server', 'Stopping server...')
        self.net.disconnect()
        self.running = False
        self.log.log_info('stop_server', 'Server stopped')



if __name__ == "__main__":
    server = BattleshipServer()
    server.start_server()
