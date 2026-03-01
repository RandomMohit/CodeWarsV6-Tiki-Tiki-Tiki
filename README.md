# PyTanks

A multiplayer 2D tank battle game with jetpacks, multiple weapons, and gun pickups inspired by Mini Militia.

## Requirements

- Python 3.x
- pygame
- numpy

## Installation

Install dependencies:
```bash
pip install pygame numpy
```

## How to Run

### 1. Start the Server

```bash
python server.py
```

The server will display its IP address. Keep this terminal running.

### 2. Start the Client(s)

In a new terminal:
```bash
python game.py
```

Enter your player name when prompted. Multiple players can connect by running `python game.py` in separate terminals or on different computers (update `SERVER_HOST` in `config.py` to the server's IP).

## Controls

| Key | Action |
|-----|--------|
| **W** | Jetpack (fly up) |
| **A** | Move left |
| **D** | Move right |
| **Arrow Keys** | Aim your gun |
| **Space** | Shoot |
| **R** | Reload |
| **S** | Switch between your two guns |
| **ESC** | Quit |

## How to Play

- **Move and Fly**: Use A/D to move horizontally and W to activate your jetpack
- **Aim and Shoot**: Use arrow keys to aim, Space to fire
- **Pick Up Guns**: Walk over glowing gun spawns to pick them up (you can carry 2 guns)
- **Switch Guns**: Press S to switch between your guns
- **Reload**: Press R or wait for auto-reload when your magazine is empty
- **Health**: You have 200 HP. Respawn when killed
- **Fuel**: Jetpack uses fuel (orange bar). It recharges when not in use

## Game Features

- **Multiple Weapons**: 15 different guns including pistols, rifles, SMGs, shotguns, sniper rifles, and rocket launchers
- **Gun Spawns**: Weapons spawn at fixed locations on the map every 15 seconds
- **Dual Wielding**: Carry two guns and switch between them
- **Jetpack System**: Limited fuel-based flight mechanic
- **Physics**: Realistic gravity and collision detection
- **Multiplayer**: Up to 8 players can play simultaneously

## Configuration

Edit `config.py` to customize:
- Server IP and port
- Weapon stats (damage, reload time, fire rate, etc.)
- Physics parameters (gravity, jetpack thrust, fuel consumption)
- Player health, speed, and colors
- Gun spawn locations and intervals
- Map selection

## Tips

- Conserve jetpack fuel - it doesn't recharge while flying
- Different guns have different reload times and fire rates
- Higher ground gives you a tactical advantage
- Pick up powerful weapons like the Sniper Rifle or SMAW for big damage
- Switch guns instead of reloading in combat for faster firing

Enjoy the game!