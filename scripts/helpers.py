# scripts/helpers.py

import numpy as np
import random
import time
import math

# =========================
# Action Buffer (internal)
# =========================

_action_buffer = np.zeros(10, dtype=bool)

def _reset_action_buffer():
    _action_buffer[:] = False

def _get_action():
    return _action_buffer.copy()

# =========================
# Primitive Controls
# (match existing 10-bit layout)
# =========================
# [0]=jetpack
# [1]=left
# [2]=right
# [3]=aim_up
# [4]=aim_down
# [5]=aim_left
# [6]=aim_right
# [7]=shoot
# [8]=reload
# [9]=switch

def cos(x):
    return math.cos(x)

def sin(x):
    return math.sin(x)

def pi():
    return math.pi

def now():
    return time.time()

def rand():
    return random.random()

def jetpack():
    _action_buffer[0] = True

def move_left():
    _action_buffer[1] = True

def move_right():
    _action_buffer[2] = True

def aim_up():
    _action_buffer[3] = True

def aim_down():
    _action_buffer[4] = True

def aim_left():
    _action_buffer[5] = True

def aim_right():
    _action_buffer[6] = True

def shoot():
    _action_buffer[7] = True

def reload():
    _action_buffer[8] = True

def switch_weapon():
    _action_buffer[9] = True


# =========================
# Read-Only Game State
# =========================

class GameState:

    def __init__(self, player_id, world_data, collision_map, grid_size):
        self._id = player_id
        self._world = world_data.copy()
        self._collision_map = collision_map.copy()
        self._grid_size = grid_size
        self._grid_h, self._grid_w = collision_map.shape

    # ---- Self ----
    def my_position(self):
        me = self._world[self._id]
        return float(me[1]), float(me[2])

    def my_health(self):
        return float(self._world[self._id, 7])

    def my_fuel(self):
        return float(self._world[self._id, 6])

    def my_score(self):
        return float(self._world[self._id, 8])

    def my_ammo(self):
        return float(self._world[self._id, 9]), float(self._world[self._id, 10])

    # ---- Enemies ----
    def enemy_positions(self):
        positions = []
        for i in range(8):
            if i != self._id and self._world[i, 0] == 1:
                positions.append((
                    float(self._world[i, 1]),
                    float(self._world[i, 2])
                ))
        return positions

    def all_players(self):
        players = []
        for i in range(8):
            if self._world[i, 0] == 1:
                players.append({
                    "id": i,
                    "x": float(self._world[i, 1]),
                    "y": float(self._world[i, 2]),
                    "health": float(self._world[i, 7]),
                    "score": float(self._world[i, 8])
                })
        return players

    # ---- Bullets ----
    def bullet_positions(self):
        bullets = []
        for i in range(8, 48):
            if self._world[i, 0] == 1:
                bullets.append((
                    float(self._world[i, 1]),
                    float(self._world[i, 2])
                ))
        return bullets

    def distance_to_obstacle(self, theta, max_distance=2000.0, step=2.0):
        """
        raycasting function
        """

        x, y = self.my_position()

        dx = math.cos(theta)
        dy = math.sin(theta)

        distance = 0.0

        while distance < max_distance:
            check_x = x + dx * distance
            check_y = y + dy * distance

            # Convert to grid cell
            grid_x = int(check_x / self._grid_size)
            grid_y = int(check_y / self._grid_size)

            # Out of bounds counts as obstacle
            if (grid_x < 0 or grid_x >= self._grid_w or
                grid_y < 0 or grid_y >= self._grid_h):
                return distance

            # Check obstacle
            if self._collision_map[grid_y, grid_x] == 0:
                return distance

            distance += step

        return max_distance


def build_state(player_id, world_data, collision_map, grid_size):
    return GameState(player_id, world_data, collision_map, grid_size)
