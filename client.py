import socket
import numpy as np


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = ("127.0.0.1", 5555)

    # -----------------------------
    # LOW-LEVEL SAFE RECEIVE
    # -----------------------------
    def _recv_exact(self, size):
        data = b""
        while len(data) < size:
            packet = self.client.recv(size - len(data))
            if not packet:
                raise ConnectionError("Connection closed by server")
            data += packet
        return data

    # -----------------------------
    # CONNECT HANDSHAKE
    # -----------------------------
    def connect(self, name):
        self.client.connect(self.addr)

        # send player name
        self.client.sendall(name.encode("utf-8"))

        # receive player ID (int32)
        pid_bytes = self._recv_exact(4)
        player_id = np.frombuffer(pid_bytes, dtype=np.int32)[0]

        # receive map info (3 int32s)
        map_info_bytes = self._recv_exact(12)
        self.grid_w, self.grid_h, self.grid_size = np.frombuffer(
            map_info_bytes, dtype=np.int32
        )

        # receive collision map
        map_size = self.grid_w * self.grid_h * 4
        map_bytes = self._recv_exact(map_size)
        self.collision_map = np.frombuffer(
            map_bytes, dtype=np.int32
        ).reshape(self.grid_h, self.grid_w)

        return player_id

    # -----------------------------
    # SEND INPUT → RECEIVE WORLD
    # -----------------------------
    def send(self, keyboard_input):
        # send input (8 bools)
        self.client.sendall(keyboard_input.tobytes())

        # expect full world_data
        rows = 48
        cols = 11
        bytes_needed = rows * cols * 8  # float64

        reply = self._recv_exact(bytes_needed)
        game_world = np.frombuffer(reply, dtype=np.float64).reshape((rows, cols))
        return game_world

    # -----------------------------
    def disconnect(self):
        self.client.close()

    def get_collision_map(self):
        return self.collision_map, self.grid_w, self.grid_h, self.grid_size
