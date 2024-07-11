# battleship/server.py
import pickle
import socket
from _thread import *

from bsp import Player

server: str = "127.0.0.1"
port: int = 5555
server_is_running = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as se:
    str(se)

s.listen(2)
print("Server started. Waiting for connection.")

players = [Player(), Player()]


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))
        except socket.error as se:
            print(se)


current_players = 0
while server_is_running:
    conn, addr = s.accept()
    print('Connected to:', addr)

    start_new_thread(threaded_client, (conn, current_players))
    current_players += 1
