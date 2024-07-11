# battleship/server.py
import pickle
import socket
from _thread import *

from battleship.game import Game


class Server:
    def __init__(self, server: str = "127.0.0.1", port=5555, server_is_running=True):
        if server is not None:
            self.server: str = server

        if port is not None:
            self.port: int = port

        if server_is_running is not None:
            self.server_is_running: bool = server_is_running

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.s.bind((self.server, self.port))
        except socket.error as se:
            str(se)

        self.s.listen(2)
        print("Server started. Waiting for connection.")

        self.current_players = 0
        self.players = []
        connected = set()
        games = {}
        self.id_count = 0

        def threaded_client(conn, player, game_id):
            global id_count
            conn.send(pickle.dumps(self.players[player]))

            reply = ""
            while True:
                try:
                    data = pickle.loads(conn.recv(2048))
                    self.players[player] = data

                    if not data:
                        print("Disconnected")
                        break
                    else:
                        if player:
                            reply = self.players[id_count]

                        # print("Received: ", data)
                        # print("Sending: ", reply)

                    conn.sendall(pickle.dumps(reply))
                except socket.error as se:
                    print(se)

            print("Lost connection")
            try:
                del games[game_id]
                print("Closing game: ", game_id)
            except:
                pass
            id_count -= 1
            conn.close()

        while server_is_running:
            conn, addr = self.s.accept()
            print('Connected to:', addr)

            start_new_thread(threaded_client, (conn, self.current_players, id_count))
            self.current_players += 1

            id_count += 1
            p = 0
            game_id = (id_count - 1) // 2
            if id_count % 2 == 1:
                games[game_id] = Game(game_id)
                print("Creating a new game...")
            else:
                games[game_id].ready = True
                p = 1

            start_new_thread(threaded_client, (conn, p, game_id))


s = Server()
s
