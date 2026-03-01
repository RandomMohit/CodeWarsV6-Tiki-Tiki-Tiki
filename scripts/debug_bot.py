# scripts/debug_bot.py

def run(state, memory):

    t = now()

    # Memory format: "last_time|step"
    if memory == "":
        last_time = 0.0
        step = 0
    else:
        try:
            parts = memory.split("|")
            last_time = float(parts[0])
            step = int(parts[1])
        except:
            last_time = 0.0
            step = 0

    # Only act once per second
    if t - last_time >= 1.0:

        print("----- DEBUG STEP -----")
        print("Position:", state.my_position())
        print("Health:", state.my_health())
        print("Fuel:", state.my_fuel())
        print("Score:", state.my_score())
        print("Ammo:", state.my_ammo())
        print("Enemies:", state.enemy_positions())
        print("Bullets:", state.bullet_positions())

        # Cycle through actions deterministically
        action_cycle = [
            move_left,
            move_right,
            aim_left,
            aim_right,
            aim_up,
            aim_down,
            shoot,
            reload,
            switch_weapon,
            jetpack
        ]

        action = action_cycle[step % len(action_cycle)]
        action()

        print("Action sent:", action.__name__)
        print("----------------------")

        step += 1
        last_time = t

    # Store updated timing + step
    new_memory = f"{last_time}|{step}"
    return new_memory[:100]
