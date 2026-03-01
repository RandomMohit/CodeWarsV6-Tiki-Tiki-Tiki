# Mini Militia Style Bullet System Improvements

## Changes Made

### 1. **Bullet Gravity (Bullet Drop)**
- Bullets now drop over distance like in Mini Militia
- Added `BULLET_GRAVITY = 0.15` in config.py
- Bullets have separate vx and vy velocity components
- Gravity is applied each frame to vy

**Location:** `server.py` - bullet movement section

### 2. **Recoil Effect**
- Players get pushed back when shooting (Mini Militia style)
- Added `RECOIL_FORCE = 2.0` in config.py
- Pushback is in opposite direction of aim
- Affects both vertical and horizontal movement

**Location:** `server.py` - shooting section (lines ~638-688)

### 3. **Bullet Trails**
- Visual line behind each bullet showing trajectory
- Added `BULLET_TRAIL_LENGTH = 15` in config.py
- Yellow trail color (255, 255, 100)
- Makes bullets easier to see and track

**Location:** `game.py` - bullet rendering section

### 4. **Improved Hit Detection**
- Added `BULLET_HIT_RADIUS = 12` in config.py
- Better collision detection radius
- More forgiving hit detection like Mini Militia

## Configuration Options

You can tune these values in `config.py`:

```python
# Bullet Physics
BULLET_GRAVITY = 0.15          # Higher = more drop
RECOIL_FORCE = 2.0             # Higher = more pushback
BULLET_TRAIL_LENGTH = 15       # Longer = more visible trail
BULLET_HIT_RADIUS = 12         # Larger = easier to hit
```

## How It Works

### Bullet Gravity System:
1. When bullet spawns, it gets initial vx and vy based on aim angle
2. Each frame: `vy += BULLET_GRAVITY` (pulls bullet down)
3. Position updates: `x += vx`, `y += vy`
4. Result: Bullets arc downward over distance

### Recoil System:
1. When player shoots, calculate opposite angle: `recoil_angle = aim_angle + π`
2. Apply force: `player_vy -= sin(recoil_angle) * RECOIL_FORCE`
3. Apply horizontal: `player_x += cos(recoil_angle) * RECOIL_FORCE`
4. Check collision before applying horizontal recoil

### Bullet Trail System:
1. Calculate trail start point behind bullet
2. Draw line from trail_start to bullet position
3. Use yellow color for visibility
4. Trail follows bullet trajectory

## Testing Tips

1. **Test Gravity:** Shoot horizontally - bullets should drop
2. **Test Recoil:** Shoot while in air - you should move backward
3. **Test Trails:** Bullets should have visible yellow lines
4. **Test Long Range:** Sniper bullets should arc at long distances

## Future Enhancements (Optional)

- [ ] Muzzle flash effect when shooting
- [ ] Screen shake on shooting
- [ ] Bullet impact particles
- [ ] Different trail colors per weapon
- [ ] Bullet penetration (through players)
- [ ] Headshot detection (bonus damage)
- [ ] Bullet ricochet off walls
- [ ] Tracer rounds (every 5th bullet different color)

## Weapon-Specific Tuning

You can make different weapons have different bullet physics by adding to weapon stats:

```python
"bullet_gravity_multiplier": 1.0,  # 0.5 = less drop, 2.0 = more drop
"recoil_multiplier": 1.0,          # weapon-specific recoil
```

Then in server.py, multiply by these values when applying physics.
