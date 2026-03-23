def run(state, memory):
    did_attack = False

    if not memory:
        memory = {
            "roam_dir": 1,
            "roam_ticks": 240,
            "evade_dir": 1,
            "evade_ticks": 0,
            "strafe_dir": 1,
            "strafe_ticks": 0,
            "grenade_tick": 0,
            "dodge_tick": 0,
            "target_id": -1,
            "target_health": -1.0,
            "no_damage_ticks": 0,
            "target_x": 0.0,
            "target_y": 0.0,
            "stable_ticks": 0,
            "last_x": 0.0,
            "last_y": 0.0,
            "stuck_ticks": 0,
            "nade_escape_ticks": 0,
            "nade_escape_dir": 1,
            "fly_tick": 0,
        }

    enemies = state.enemy_positions()
    markers = state.player_markers()
    ammo_cur, _ = state.my_ammo()
    grenades = state.my_grenades()
    health = state.my_health()
    fuel = state.my_fuel()
    current_aim = state.my_aim_angle()
    my_x, my_y = state.my_position()

    # Proper defaults (IMPORTANT FIX)
    memory.setdefault("target_id", -1)
    memory.setdefault("target_health", -1.0)
    memory.setdefault("no_damage_ticks", 0)
    memory.setdefault("target_x", 0.0)
    memory.setdefault("target_y", 0.0)
    memory.setdefault("stable_ticks", 0)
    memory.setdefault("grenade_tick", 0)
    memory.setdefault("dodge_tick", 0)
    memory.setdefault("last_x", my_x)
    memory.setdefault("last_y", my_y)
    memory.setdefault("stuck_ticks", 0)
    memory.setdefault("nade_escape_ticks", 0)
    memory.setdefault("nade_escape_dir", 1)
    memory.setdefault("fly_tick", 0)
    memory.setdefault("roam_dir", 1)
    memory.setdefault("roam_ticks", 240)

    MIN_FIGHT_DIST = 100.0
    MAX_FIGHT_DIST = 300.0
    PRESSURE_DIST = 145.0
    GRENADE_ESCAPE_DIST = 180.0
    AIM_THRESHOLD = 0.13

    # Cooldowns
    if memory["grenade_tick"] > 0:
        memory["grenade_tick"] -= 1
    if memory["dodge_tick"] > 0:
        memory["dodge_tick"] -= 1
    if memory["fly_tick"] > 0:
        memory["fly_tick"] -= 1

    # -------- GRENADE ESCAPE --------
    nades = state.active_grenades()
    nearest_nade = None
    nearest_nade_dist = 1e9

    for g in nades:
        nx, ny = float(g["x"]), float(g["y"])
        d = math.sqrt((nx - my_x)**2 + (ny - my_y)**2)
        if d < nearest_nade_dist:
            nearest_nade_dist = d
            nearest_nade = g

    if nearest_nade and nearest_nade_dist < GRENADE_ESCAPE_DIST:
        gx = float(nearest_nade["x"])
        memory["nade_escape_dir"] = -1 if my_x < gx else 1
        memory["nade_escape_ticks"] = 18
    elif memory["nade_escape_ticks"] > 0:
        memory["nade_escape_ticks"] -= 1

    escaping_nade = memory["nade_escape_ticks"] > 0

    # -------- TARGET SELECTION --------
    if enemies:
        best_target = None
        best_dist = 1e9
        fallback_target = None
        fallback_dist = 1e9

        for e in enemies:
            ex, ey = float(e["x"]), float(e["y"])
            dist = float(e["distance"])

            dx = ex - my_x
            dy = ey - my_y
            angle = math.atan2(dy, dx)

            obstacle_dist = state.distance_to_obstacle(angle, max_distance=2000.0, step=4.0)
            blocked = obstacle_dist < max(0.0, dist - 20.0)

            if dist < fallback_dist:
                fallback_dist = dist
                fallback_target = e

            if not blocked and dist < best_dist:
                best_dist = dist
                best_target = e

        target = best_target if best_target else fallback_target

        target_id = int(target["id"])
        ex, ey = float(target["x"]), float(target["y"])
        target_health = float(target["health"])
        distance = float(target["distance"])

        dx = ex - my_x
        dy = ey - my_y
        angle = math.atan2(dy, dx)

        obstacle_dist = state.distance_to_obstacle(angle, max_distance=2000.0, step=4.0)
        blocked = obstacle_dist < max(0.0, distance - 20.0)

        # -------- AIM --------
        aim_error = angle - current_aim
        if aim_error > math.pi:
            aim_error -= 2 * math.pi
        elif aim_error < -math.pi:
            aim_error += 2 * math.pi

        if aim_error > 0.01:
            aim_right()
        elif aim_error < -0.01:
            aim_left()

        # -------- MOVEMENT (CHASE BASED) --------
        if escaping_nade:
            move_left() if memory["nade_escape_dir"] < 0 else move_right()
            if nearest_nade_dist < 120:
                jetpack()

        else:
            # Horizontal chase
            if dx < -5:
                move_left()
            elif dx > 5:
                move_right()

            # Vertical adjustment
            if abs(dx) <= 20:
                if dy < -10 and fuel > 8:
                    jetpack()

            # Obstacle handling
            if blocked and fuel > 8:
                jetpack()

            # Enemy above → chase up
            if dy < -20 and fuel > 8:
                if memory["fly_tick"] <= 0:
                    jetpack()
                    memory["fly_tick"] = 2

            # Far → boost forward
            if distance > 200 and fuel > 10:
                jetpack()

        # -------- SHOOT --------
        if not blocked and abs(aim_error) < AIM_THRESHOLD:
            if ammo_cur <= 0:
                reload()
            else:
                shoot()
                did_attack = True
        elif ammo_cur <= 0:
            reload()

        # -------- MEMORY UPDATE --------
        memory["target_id"] = target_id
        memory["target_health"] = target_health
        memory["target_x"] = ex
        memory["target_y"] = ey

        # Low HP panic
        if health < 30 and memory["dodge_tick"] <= 0:
            jetpack()
            memory["dodge_tick"] = 30

    # -------- NO ENEMY --------
    else:
        front_angle = math.pi if memory["roam_dir"] == -1 else 0
        front_dist = state.distance_to_obstacle(front_angle, max_distance=64, step=4)

        if front_dist < 22 or memory["roam_ticks"] <= 0:
            memory["roam_dir"] *= -1
            memory["roam_ticks"] = 240
            jetpack()

        memory["roam_ticks"] -= 1
        move_left() if memory["roam_dir"] == -1 else move_right()

    pickup_gun(state)

    # -------- ANTI-STUCK --------
    moved = math.sqrt((my_x - memory["last_x"])**2 + (my_y - memory["last_y"])**2)

    if moved < 2 and not did_attack:
        memory["stuck_ticks"] += 1
    else:
        memory["stuck_ticks"] = 0

    if memory["stuck_ticks"] >= 20:
        memory["roam_dir"] *= -1
        jetpack()
        memory["stuck_ticks"] = 0

    memory["last_x"] = my_x
    memory["last_y"] = my_y

    return memory