# Gun Spawn System Documentation

## Overview
A complete gun spawning and pickup system inspired by Mini Militia, with support for carrying two guns and switching between them.

## New Files Created

### `gun_spawner.py`
Contains two main classes:

#### `GunSpawner`
Manages gun spawn points and their cooldowns.
- **Spawn Interval**: 15 seconds (configurable)
- **Pickup Radius**: 20 pixels
- **Spawn Points**: Defined per map in `_define_spawn_points()`

**Methods:**
- `initialize_map(map_name)`: Load spawn points for a specific map
- `update(delta_time)`: Update cooldowns and respawn guns
- `check_pickup(x, y)`: Check if player is near a gun spawn
- `get_active_spawns()`: Get list of currently spawned guns for rendering

#### `PlayerInventory`
Manages each player's two-gun inventory system.
- **Capacity**: 2 guns maximum
- **Default**: Starts with Desert Eagle (weapon ID 1)

**Methods:**
- `pickup_gun(weapon_id)`: Pick up a new gun (replaces current if both slots full)
- `switch_gun()`: Switch between gun slots (S key)
- `get_current_gun()`: Get currently active weapon
- `get_gun_ids()`: Get both gun IDs for syncing
- `get_ammo_data()`: Get ammo for both guns

## Spawn Points (Catacombs Map)

Currently defined 12 spawn points across the catacombs map:

**Left Side:**
- (100, 300) - Desert Eagle
- (150, 450) - UZI
- (200, 150) - MP5

**Center:**
- (400, 250) - AK47
- (450, 400) - Shotgun
- (500, 100) - M4

**Right Side:**
- (700, 300) - Sniper
- (650, 450) - M14
- (750, 150) - SMAW

**Additional:**
- (300, 500) - Magnum
- (600, 500) - TAVOR
- (350, 50) - XM8

## Controls

### New Keybinds
- **S** - Switch between guns (if carrying two)
- **R** - Reload current gun (existing)
- **SPACE** - Shoot current gun (existing)

## How It Works

### Gun Spawning
1. Guns spawn at predefined locations when the map loads
2. Gun spawns are shown as gold/yellow circles with "G" marker
3. When picked up, the spawn becomes inactive
4. After 15 seconds, the gun respawns at the same location
5. If a gun is already spawned and not picked up, no duplicate spawns

### Gun Pickup
1. Walk within 20 pixels of a gun spawn
2. Gun is automatically picked up
3. If you have an empty slot, it goes there
4. If both slots are full, it replaces your current gun

### Gun Switching
1. Press **S** to switch between your two guns
2. Each gun maintains its own ammo count
3. Reload times and fire rates are specific to each gun

## Network Protocol Updates

### Client → Server (10 bytes)
Input array: `[W, A, D, UP, DOWN, LEFT, RIGHT, SPACE, R, S]`

### Server → Client
1. **World Data** (4224 bytes): Player states, bullets, etc.
2. **Gun Spawn Data** (variable): Active gun spawn locations
3. **Inventory Data** (96 bytes): Each player's gun loadout

## Adding New Maps

To add spawn points for a new map, edit `gun_spawner.py`:

```python
def _define_spawn_points(self):
    # Add your map here
    self.spawn_points['your_map_name'] = [
        (x, y, weapon_id),  # Spawn point 1
        (x, y, weapon_id),  # Spawn point 2
        # ... more spawn points
    ]
```

Then update server initialization to use your map:
```python
self.current_map_name = "your_map_name"
```

## Configuration

### Spawn Settings (in `gun_spawner.py`)
```python
self.SPAWN_INTERVAL = 15.0    # Respawn time in seconds
self.PICKUP_RADIUS = 20.0     # Pickup distance in pixels
```

### Starting Weapon (in `server.py`)
```python
PlayerInventory(starting_weapon_id=1)  # 1 = Desert Eagle
```

## Testing

1. Start server: `python server.py`
2. Start client: `python game.py`
3. Walk near gold circles to pick up guns
4. Press S to switch between guns
5. Each gun has its own ammo and characteristics

## Future Enhancements

- Gun drop on death
- Weapon rarity system
- Ammo pickups separate from guns
- Visual weapon models instead of "G" marker
- Weapon stats HUD showing both guns
- Different spawn patterns per map
