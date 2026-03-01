# PyTanks Map Editor Guide

## Overview
The PyTanks Map Editor allows you to create and edit maps with both collision geometry (obstacles) and weapon spawn points.

## Running the Editor
```bash
python map_editor.py
```

## Controls

### Navigation & General
- **Q**: Quit the editor
- **S**: Save current map (prompts for filename)
- **L**: Load a map (prompts for filename)
- **B**: Browse available maps
- **C**: Clear entire map (obstacles and weapon spawns)

### Obstacle Editing Mode (Default)
- **LEFT CLICK + DRAG**: Draw obstacles (gray blocks)
- **RIGHT CLICK + DRAG**: Erase obstacles
- **G**: Fill bottom row with ground obstacles

### Weapon Spawn Mode
- **W**: Toggle weapon spawn mode ON/OFF
- **LEFT/RIGHT ARROW**: Select weapon type to place
- **LEFT CLICK**: Place weapon spawn at mouse position
- **RIGHT CLICK**: Remove weapon spawn near mouse position

## Map File Format

Each map consists of two files in the `maps/` directory:

### 1. Collision Map: `<mapname>.npy`
- Binary NumPy array storing obstacle data
- 0 = obstacle (impassable)
- 1 = passable space

### 2. Weapon Spawns: `<mapname>_spawns.json`
- JSON array of spawn points
- Format: `[[x, y, weapon_id], [x, y, weapon_id], ...]`
- Example:
```json
[
  [100, 300, 1],
  [450, 400, 10],
  [700, 300, 5]
]
```

## Weapon IDs

| ID | Weapon Name      | ID | Weapon Name     |
|----|------------------|----|-----------------|
| 0  | AK47             | 8  | UZI             |
| 1  | Desert Eagle     | 9  | TEC9            |
| 2  | Golden Deagle    | 10 | SPAS-12         |
| 3  | M14              | 11 | SMAW            |
| 4  | M4               | 12 | TAVOR           |
| 5  | M93BA Sniper     | 13 | XM8             |
| 6  | Magnum           | 14 | MINIGUN         |
| 7  | MP5              |    |                 |

## Workflow Example

### Creating a New Map
1. Run `python map_editor.py`
2. Press **C** to clear the default map
3. Press **G** to add ground at bottom
4. Draw obstacles with **LEFT CLICK**
5. Press **W** to enter weapon spawn mode
6. Use **LEFT/RIGHT** arrows to select weapons
7. **LEFT CLICK** to place weapon spawns
8. Press **S** to save (enter filename, e.g., "arena")

### Editing an Existing Map
1. Run `python map_editor.py`
2. Press **B** to browse maps
3. Select map with **UP/DOWN** arrows, press **ENTER**
4. Edit obstacles or weapon spawns as needed
5. Press **S** to save

## Visual Indicators

- **Gray blocks**: Obstacles (impassable)
- **Dark blocks**: Passable space
- **Gold circles with text**: Weapon spawn points
  - Circle shows spawn location
  - Text shows weapon name (truncated)

## Migration from Config-Based Spawns

If you have existing spawn points in `config.py`, run the migration script:

```bash
python migrate_spawns.py
```

This converts `GUN_SPAWN_POINTS` from config to individual JSON files.

## Tips

- **Strategic Placement**: Place powerful weapons (Sniper, SMAW) in contested or hard-to-reach areas
- **Balance**: Distribute weapon types across the map
- **Visibility**: Ensure spawn points aren't hidden inside obstacles
- **Testing**: Load the map in-game to test spawn positions and gameplay flow
- **Grid Size**: Each cell is 10x10 pixels; map is 800x600 (80x60 cells)

## Integration with Game

The server automatically loads weapon spawns from map files:
1. Server reads `maps/<mapname>.npy` for collision
2. Server reads `maps/<mapname>_spawns.json` for weapon spawns
3. Falls back to `config.py` if JSON file doesn't exist
4. Spawns appear in-game with gold glow effect
5. Players pickup weapons by walking near spawn points

## Troubleshooting

**Spawn points not appearing in-game?**
- Ensure `<mapname>_spawns.json` exists in `maps/` folder
- Check JSON syntax is valid
- Verify weapon IDs are valid (0-14)
- Ensure spawn coordinates are within map bounds (0-800, 0-600)

**Can't place weapons in editor?**
- Make sure weapon spawn mode is ON (press **W**)
- Check mode indicator at bottom of screen
- Current weapon is shown in brackets

**Map not saving?**
- Check `maps/` directory exists and is writable
- Ensure filename contains only alphanumeric characters and underscores
