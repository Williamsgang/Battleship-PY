import socket
import threading
from typing import Tuple
from logs import logger


class Network:
    def __init__(self, host_port: Tuple[str, int], is_server=False):
        self.is_server = is_server
        self.host_port = host_port
        self.log = logger.Logger(self.__class__.__name__)
        self.log.log_info('__init__', f'Logger initialized on {self.__class__.__name__}')
        self.s = None
        self.clients = []

        if is_server:
            self.setup_server()
        else:
            self.setup_client()

    def setup_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(self.host_port)
        self.s.listen(5)
        self.log.log_info('setup_server', f'Server listening on {self.host_port[0]}:{self.host_port[1]}')

    def setup_client(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.log.log_info('setup_client', 'Client socket setup complete')

    def accept_conn(self):
        if not self.is_server:
            raise RuntimeError("accept_conn can only be called on server instances")
        try:
            conn, addr = self.s.accept()
            self.log.log_info('accept_conn', f'Accepted connection from {addr}')
            self.clients.append(conn)
            return conn, addr
        except socket.error as se:
            self.log.log_error('accept_conn', f'Socket error on accept: {se}')
            return None, None

    def connect(self):
        if self.is_server:
            raise RuntimeError("connect can only be called on client instances")
        try:
            self.s.connect(self.host_port)
            self.log.log_info('connect', f'Connected to server at {self.host_port[0]}:{self.host_port[1]}')
            return self.s
        except socket.error as se:
            self.log.log_error('connect', f'Socket error: {se}')
            return None

    def disconnect(self):
        if self.s:
            try:
                self.s.close()
                self.log.log_info('disconnect', 'Socket closed')
            except socket.error as se:
                self.log.log_error('disconnect', f'Socket error: {se}')

    def send_data(self, conn, data):
        try:
            conn.sendall(data)
            self.log.log_info('send_data', 'Data sent successfully')
        except socket.error as se:
            self.log.log_error('send_data', f'Socket error: {se}')

    def receive_data(self, conn):
        try:
            data = conn.recv(4096)
            self.log.log_info('receive_data', 'Data received successfully')
            return data
        except socket.error as se:
            self.log.log_error('receive_data', f'Socket error: {se}')
            return None

    def get_connections(self):
        self.log.log_info('get_connections', 'Returning connected clients')
        return self.clients

    def broadcast(self, data):
        for client in self.clients:
            self.send_data(client, data)

    def start_server_thread(self):
        threading.Thread(target=self.run_server, daemon=True).start()

    def run_server(self):
        while True:
            conn, addr = self.accept_conn()
            if conn:
                threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def handle_client(self, conn):
        while True:
            data = self.receive_data(conn)
            if not data:
                self.clients.remove(conn)
                conn.close()
                break
            self.broadcast(data)
