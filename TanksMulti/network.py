import socket
import pickle
import init


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = init.server
        self.port = init.port
        self.adr = (self.server, self.port)
        self.player_id = self.connect()

    def connect(self):
        try:
            self.client.connect(self.adr)
            return int(self.client.recv(init.space).decode())
        except socket.error:
            print("Couldn't connect to the server")

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(init.space))
        except socket.error:
            print("Couldn't send data")

