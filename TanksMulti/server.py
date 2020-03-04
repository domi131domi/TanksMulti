import socket
from _thread import *
import pickle
import init
from game_server import Game

server = init.server
port = init.port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error:
    print("Error! Couldn't start server")

s.listen(2)

id_counter = -1
key_statements = list()


def threaded_client(conn, tank_id, game):
    conn.send(str.encode(str(tank_id)))

    while True:
        keys = pickle.loads(conn.recv(init.space))

        if not keys:
            break
        else:
            game.update(tank_id, keys)

            conn.sendall(pickle.dumps(game.get_packages()))

    print("Lost connection")
    conn.close()


game = Game()
while True:
    conn, adr = s.accept()

    id_counter += 1

    start_new_thread(threaded_client, (conn, id_counter, game))
