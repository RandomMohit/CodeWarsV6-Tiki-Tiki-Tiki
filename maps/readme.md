## Files

### Map Tools
- `map_editor.py` - Visual map editor
- `create_maps.py` - Generate sample maps programmatically

### Maps Folder
- `maps/` - Contains all map files (.npy format)

## How to Create Maps

### Option 1: Visual Editor (Recommended)
```bash
python map_editor.py
```

**Controls:**
- **Left Click** - Draw obstacles (walls, platforms)
- **Right Click** - Erase obstacles
- **S** - Save map (enter filename)
- **L** - Load map (enter filename)
- **C** - Clear entire map
- **G** - Add ground (bottom row)
- **Q** - Quit

**Workflow:**
1. Run map_editor.py
2. Draw your map with mouse
3. Press 'S', enter name like "my_map"
4. File saved as `maps/my_map.npy`

### Option 2: Code Your Own Maps
Edit `create_maps.py` to add your own map functions:

```python
def create_my_custom_map():
    GRID_H, GRID_W = 30, 40
    collision_map = np.ones((GRID_H, GRID_W), dtype=np.int32)
    
    # 1 = passable air, 0 = solid obstacle
    collision_map[-1, :] = 0  # ground
    collision_map[20, 10:20] = 0  # platform
    
    return collision_map
```

Then add it to the maps dictionary and run `python create_maps.py`

## Using Maps in Game

Edit `server.py` line 96:
```python
self.load_map("default")  # Change to any map name
```

Available default maps:
- **default** - Simple platforms
- **minimilitia** - Mini Militia inspired (symmetrical bunkers and platforms)
- **arena** - Enclosed arena with corner platforms
- **open** - Minimal obstacles, open combat

## Map Format

- Grid: 40 cells wide × 30 cells tall
- Cell size: 20×20 pixels
- Total area: 800×600 pixels
- Values: `1` = passable, `0` = obstacle
- Format: NumPy array saved as .npy file

## Mini Militia Style Tips

To replicate Mini Militia maps:
1. **Symmetrical design** - left/right mirror for fairness
2. **Bunkers** - enclosed areas with roof and walls
3. **Multiple levels** - 3-4 height layers
4. **Cover spots** - small walls and platforms
5. **Vertical space** - use jetpack to reach upper areas
6. **Center control point** - contested middle area

## Examples

Load different maps:
```python
# In server.py setup_game():
self.load_map("wncc2")  

