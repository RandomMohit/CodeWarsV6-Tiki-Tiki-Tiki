# Weapon Visual Effects System - Phase 1

## What's Been Added

### 1. **Muzzle Flashes**
- Appear when any player shoots
- Weapon-specific colors and sizes:
  - **Pistols**: Bright yellow flash (Golden Deagle has golden tint)
  - **Assault Rifles**: Orange flash
  - **SMGs**: Small rapid flashes
  - **Snipers**: Large bright white flash
  - **Shotgun**: Wide orange flash
  - **SMAW**: Huge orange-red flash
  - **Minigun**: Continuous small flashes

### 2. **Impact Effects**
- Spark particles when bullets hit walls/obstacles
- Particle count varies by weapon:
  - SMGs: 4 particles (fast fire rate)
  - Pistols/Rifles: 6 particles
  - Shotgun: 8 particles
  - Snipers: 12 particles
  - SMAW: 20 particles (explosion-like)

### 3. **Enhanced Bullet Trails**
- Existing yellow trails maintained
- Now integrated with new effects system

## Files Created/Modified

### New Files:
- `weapon_effects.py` - Complete visual effects system

### Modified Files:
- `game.py` - Integrated effects manager

## How It Works

### Muzzle Flash Detection:
```python
# Detects when ammo decreases (player shot)
if current_ammo < previous_ammo:
    add_muzzle_flash(position, angle, weapon_id)
```

### Impact Detection:
```python
# Detects when bullets disappear (hit something)
if bullet_was_active and now_inactive:
    add_impact_effect(last_position, weapon_id)
```

## Performance

- **Optimized for 60 FPS**
- Effects auto-cleanup when finished
- Particle lifetime: 0.1-0.3 seconds
- Muzzle flash lifetime: 0.05 seconds (50ms)

## Customization

### Adjust Effect Intensity:

In `weapon_effects.py`, modify these methods:

**Muzzle Flash Size:**
```python
def _get_flash_properties(self, weapon_id):
    size = 10  # Change this value
    color = (255, 200, 100)
    return size, color
```

**Particle Count:**
```python
def _get_particle_count(self, weapon_id):
    return 6  # More particles = more intense
```

**Effect Duration:**
```python
# In MuzzleFlash.__init__
self.lifetime = 0.05  # Increase for longer flash

# In ImpactEffect.__init__
lifetime = random.uniform(0.1, 0.3)  # Adjust range
```

## Testing

1. Start server: `python server.py`
2. Start game: `python game.py`
3. Shoot different weapons to see effects
4. Watch for:
   - Muzzle flash when shooting
   - Spark particles when bullets hit walls
   - Different effects per weapon type

## Known Limitations

- Impact effects only trigger on wall hits (not player hits yet)
- No screen shake (can be added in Phase 2)
- No smoke trails (can be added in Phase 2)
- No explosion animations for SMAW (can be added in Phase 2)

## Future Enhancements (Phase 2)

If you want more advanced effects:
- [ ] Screen shake on shooting
- [ ] Smoke particle trails
- [ ] Explosion animations for SMAW
- [ ] Shell casing ejection
- [ ] Weapon-specific recoil animations
- [ ] Hit markers on player hits
- [ ] Blood/damage particles
- [ ] Dual-wield alternating flashes

## Troubleshooting

**Effects not showing:**
- Check console for errors
- Verify `weapon_effects.py` is in same directory as `game.py`
- Make sure server is running

**Performance issues:**
- Reduce particle count in `_get_particle_count()`
- Reduce effect lifetime
- Lower FPS cap in config

**Effects too subtle:**
- Increase muzzle flash size
- Increase particle count
- Make colors brighter
- Increase particle size

## Code Structure

```
weapon_effects.py
├── Particle (base particle class)
├── MuzzleFlash (weapon-specific flashes)
├── ImpactEffect (spark particles)
└── WeaponEffectsManager (manages all effects)

game.py
├── Import WeaponEffectsManager
├── Initialize in __init__
├── Update in run_game loop
├── Detect shots in render
└── Draw effects in render
```

Enjoy the enhanced visuals!
