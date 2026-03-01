"""
Utility to migrate weapon spawn points from config.py to map files
Run this once to convert existing hardcoded spawn points to the new JSON file format
"""

import json
import os
from config import GUN_SPAWN_POINTS

def migrate_spawn_points():
    """Convert GUN_SPAWN_POINTS from config to individual map spawn files"""
    maps_dir = "maps"
    if not os.path.exists(maps_dir):
        os.makedirs(maps_dir)
    
    for map_name, spawn_data in GUN_SPAWN_POINTS.items():
        spawns_filepath = os.path.join(maps_dir, f"{map_name}_spawns.json")
        
        # Convert to list format (already is, but ensure)
        spawn_list = [[x, y, weapon_id] for x, y, weapon_id in spawn_data]
        
        # Save to JSON file
        with open(spawns_filepath, 'w') as f:
            json.dump(spawn_list, f, indent=2)
        
        print(f"✓ Migrated {len(spawn_list)} spawn points to {spawns_filepath}")
    
    print(f"\n✓ Migration complete! {len(GUN_SPAWN_POINTS)} maps migrated.")
    print("You can now edit weapon spawns using the map editor (press W to enter weapon mode)")

if __name__ == "__main__":
    migrate_spawn_points()
