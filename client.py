import socket
import numpy as np
import config

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # default to localhost for local testing
        self.host = config.SERVER_HOST
        self.port = config.SERVER_PORT
        self.addr = (self.host, self.port)

    def connect(self, name):
        self.client.connect(self.addr)

        # inform server of username - pad to exactly 16 bytes
        name_bytes = name.encode('utf-8')[:16]  # Truncate if too long
        name_bytes = name_bytes.ljust(16, b'\x00')  # Pad with null bytes to 16 bytes
        self.client.send(name_bytes)

        # receive user ID from server
        data = self.client.recv(4)
        player_id = int.from_bytes(data, byteorder='little')
        
        # receive collision map info
        map_info_bytes = self.client.recv(12)  # 3 int32s
        map_info = np.frombuffer(map_info_bytes, dtype=np.int32)
        self.grid_w, self.grid_h, self.grid_size = map_info
        
        # receive collision map data
        map_size = self.grid_w * self.grid_h * 4  # int32 = 4 bytes
        map_bytes = bytes()
        while len(map_bytes) < map_size:
            map_bytes += self.client.recv(4096)
        self.collision_map = np.frombuffer(map_bytes[:map_size], dtype=np.int32).reshape((self.grid_h, self.grid_w))
        
        return player_id 

    def disconnect(self):
        self.client.close()
    
    def get_collision_map(self):
        """Return the collision map and grid info"""
        return self.collision_map, self.grid_w, self.grid_h, self.grid_size

    def send(self, keyboard_input):
        try:
            client_msg = keyboard_input.tobytes()
            self.client.send(client_msg)
            reply = bytes()
            # expect 48 rows * 11 columns * 8 bytes per float64 = 4224 bytes
            # + spawn_data (variable size, max 50 spawns * 4 values * 4 bytes = 800 bytes)
            # + inventory_data (8 players * 3 values * 4 bytes = 96 bytes)
            # Total expected: 4224 + variable spawn + 96
            # For simplicity, receive a fixed larger buffer
            while len(reply) < 5120:  # Increased buffer size
                chunk = self.client.recv(2048)
                if not chunk:
                    break
                reply += chunk
                if len(reply) >= 4224:  # At minimum we have world_data
                    break
                    
            # Parse world_data (first 4224 bytes)
            game_world = np.frombuffer(reply[:4224], dtype=np.float64).reshape((48, 11))
            
            # Parse gun spawn data (variable length, but we'll read what's available)
            remaining = reply[4224:]
            gun_spawns = []
            inventory_data = None
            
            if len(remaining) >= 96:  # At least inventory data present
                # Try to parse spawn data (anything before last 96 bytes)
                spawn_bytes = remaining[:-96]
                inventory_bytes = remaining[-96:]
                
                if len(spawn_bytes) >= 16:  # At least one spawn (4 floats * 4 bytes)
                    try:
                        num_spawns = len(spawn_bytes) // 16
                        spawn_array = np.frombuffer(spawn_bytes[:num_spawns*16], dtype=np.float32).reshape((-1, 4))
                        gun_spawns = spawn_array.tolist()
                    except:
                        pass
                
                try:
                    inventory_data = np.frombuffer(inventory_bytes, dtype=np.int32).reshape((8, 3))
                except:
                    pass
            
            return game_world, gun_spawns, inventory_data
        except socket.error as e:
            print(e)
            return None, [], None

