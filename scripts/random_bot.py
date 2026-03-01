def run(state, memory):

    r = rand()

    # Random movement
    if r < 0.25:
        move_left()
    elif r < 0.5:
        move_right()

    # Random aiming
    r2 = rand()
    if r2 < 0.25:
        aim_left()
    elif r2 < 0.5:
        aim_right()
    elif r2 < 0.75:
        aim_up()
    else:
        aim_down()

    # Random shooting
    if rand() < 0.4:
        shoot()

    if rand() < 0.05:
        reload()

    if rand() < 0.02:
        switch_weapon()

    if rand() < 0.1:
        jetpack()

    return memory
