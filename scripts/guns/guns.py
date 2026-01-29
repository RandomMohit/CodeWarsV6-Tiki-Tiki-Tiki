import math
import random

# =========================
# BULLET FACTORY
# =========================
def spawn_bullet(x, y, angle, speed, damage):
    return {
        "x": x,
        "y": y,
        "vx": math.cos(angle) * speed,
        "vy": math.sin(angle) * speed,
        "damage": damage,
        "radius": 4
    }


# =========================
# GUN CLASS
# =========================
class Gun:
    def __init__(
        self,
        name,
        damage,
        accuracy,
        reload_time,
        melee,
        rpf,
        effective_range,
        dual_wielding,
        rate_of_fire,
        magazine_capacity,
        ammo_given,
        sprite,
        distancefactor=1.0,
        harm=False
    ):
        # ---- static properties ----
        self.name = name
        self.damage = damage
        self.accuracy = accuracy              # degrees
        self.reload_time = reload_time        # seconds
        self.melee_damage = melee
        self.rpf = rpf                        # rounds per fire
        self.effective_range = effective_range
        self.dual_wielding = dual_wielding
        self.rate_of_fire = rate_of_fire      # RPM
        self.magazine_capacity = magazine_capacity
        self.ammo_given = ammo_given
        self.sprite = sprite
        self.distancefactor = distancefactor
        self.harm = harm

        # ---- dynamic state ----
        self.current_ammo = magazine_capacity
        self.cooldown = 0.0
        self.reloading = False
        self.reload_timer = 0.0

    # =========================
    # UPDATE (CALLED EVERY FRAME)
    # =========================
    def update(self, dt):
        if self.cooldown > 0:
            self.cooldown = max(0.0, self.cooldown - dt)

        if self.reloading:
            self.reload_timer -= dt
            if self.reload_timer <= 0:
                self.current_ammo = self.magazine_capacity
                self.reloading = False

    # =========================
    # START RELOAD
    # =========================
    def start_reload(self):
        if self.reloading:
            return
        if self.current_ammo == self.magazine_capacity:
            return
        self.reloading = True
        self.reload_timer = self.reload_time

    # =========================
    # SHOOT
    # =========================
    def shoot(self, x, y, angle):
        if self.reloading or self.cooldown > 0:
            return []

        if self.current_ammo < self.rpf:
            self.start_reload()
            return []

        bullets = []

        for _ in range(self.rpf):
            spread = math.radians(
                random.uniform(-self.accuracy, self.accuracy)
            )
            bullet_angle = angle + spread

            bullets.append(
                spawn_bullet(
                    x,
                    y,
                    bullet_angle,
                    speed=50,
                    damage=self.damage
                )
            )

        self.current_ammo -= self.rpf
        self.cooldown = 60.0 / self.rate_of_fire
        return bullets

    # =========================
    # DEBUG / INFO
    # =========================
    def display_info(self):
        return (
            f"Gun: {self.name}\n"
            f"Damage: {self.damage}\n"
            f"Accuracy: {self.accuracy}\n"
            f"RPM: {self.rate_of_fire}\n"
            f"Magazine: {self.magazine_capacity}\n"
            f"Ammo: {self.current_ammo}/{self.magazine_capacity}\n"
            f"Sprite: {self.sprite}\n"
        )


# =========================
# DATA-DRIVEN GUN DEFINITIONS
# =========================
GUN_DATA = [

    # =====================
    # ASSAULT RIFLES
    # =====================
    dict(
        name="AK47",
        damage=10,
        accuracy=4,
        reload_time=2.0,
        melee=30,
        rpf=1,
        effective_range=800,
        dual_wielding=False,
        rate_of_fire=600,
        magazine_capacity=35,
        ammo_given=250,
        sprite="ak47.png"
    ),

    dict(
        name="M4",
        damage=14,
        accuracy=2,
        reload_time=2.0,
        melee=30,
        rpf=1,
        effective_range=1000,
        dual_wielding=False,
        rate_of_fire=700,
        magazine_capacity=30,
        ammo_given=300,
        sprite="m4.png"
    ),

    dict(
        name="TAVOR",
        damage=9,
        accuracy=2,
        reload_time=1.5,
        melee=30,
        rpf=1,
        effective_range=750,
        dual_wielding=False,
        rate_of_fire=650,
        magazine_capacity=35,
        ammo_given=200,
        sprite="tavor.png"
    ),

    dict(
        name="XM8",
        damage=8,
        accuracy=3,
        reload_time=1.9,
        melee=30,
        rpf=1,
        effective_range=875,
        dual_wielding=False,
        rate_of_fire=700,
        magazine_capacity=30,
        ammo_given=200,
        sprite="xm8.png"
    ),

    # =====================
    # PISTOLS
    # =====================
    dict(
        name="Desert Eagle",
        damage=8,
        accuracy=2,
        reload_time=1.25,
        melee=15,
        rpf=1,
        effective_range=500,
        dual_wielding=False,
        rate_of_fire=240,
        magazine_capacity=15,
        ammo_given=75,
        sprite="deagle.png"
    ),

    dict(
        name="Golden Deagle",
        damage=10,
        accuracy=2,
        reload_time=1.25,
        melee=25,
        rpf=1,
        effective_range=600,
        dual_wielding=False,
        rate_of_fire=300,
        magazine_capacity=15,
        ammo_given=75,
        sprite="gdeagle.png"
    ),

    dict(
        name="Magnum",
        damage=30,
        accuracy=1,
        reload_time=2.0,
        melee=25,
        rpf=1,
        effective_range=650,
        dual_wielding=False,
        rate_of_fire=180,
        magazine_capacity=6,
        ammo_given=36,
        sprite="magnum.png"
    ),

    # =====================
    # SMGs (DUAL-WIELDABLE)
    # =====================
    dict(
        name="MP5",
        damage=7,
        accuracy=5,
        reload_time=1.75,
        melee=30,
        rpf=1,
        effective_range=700,
        dual_wielding=True,
        rate_of_fire=800,
        magazine_capacity=50,
        ammo_given=400,
        sprite="mp5.png"
    ),

    dict(
        name="UZI",
        damage=7,
        accuracy=6,
        reload_time=1.5,
        melee=20,
        rpf=1,
        effective_range=500,
        dual_wielding=True,
        rate_of_fire=900,
        magazine_capacity=40,
        ammo_given=400,
        sprite="uzi.png"
    ),

    dict(
        name="TEC9",
        damage=10,
        accuracy=4,
        reload_time=1.5,
        melee=25,
        rpf=1,
        effective_range=600,
        dual_wielding=True,
        rate_of_fire=750,
        magazine_capacity=40,
        ammo_given=400,
        sprite="tec9.png"
    ),

    # =====================
    # SHOTGUNS
    # =====================
    dict(
        name="SPAS-12",
        damage=25,
        accuracy=10,
        reload_time=2.5,
        melee=40,
        rpf=5,              # pellets per shot
        effective_range=325,
        dual_wielding=False,
        rate_of_fire=80,
        magazine_capacity=5,
        ammo_given=24,
        sprite="shotgun.png"
    ),

    # =====================
    # SNIPERS
    # =====================
    dict(
        name="M14",
        damage=36,
        accuracy=0.5,
        reload_time=2.25,
        melee=35,
        rpf=1,
        effective_range=1200,
        dual_wielding=False,
        rate_of_fire=180,
        magazine_capacity=6,
        ammo_given=36,
        sprite="m14.png"
    ),

    dict(
        name="M93BA Sniper",
        damage=75,
        accuracy=0.25,
        reload_time=2.5,
        melee=35,
        rpf=1,
        effective_range=1500,
        dual_wielding=False,
        rate_of_fire=60,
        magazine_capacity=3,
        ammo_given=20,
        sprite="sniper.png"
    ),

    # =====================
    # HEAVY / SPECIAL
    # =====================
    dict(
        name="MINIGUN",
        damage=30,
        accuracy=7,
        reload_time=4.25,
        melee=35,
        rpf=1,
        effective_range=650,
        dual_wielding=False,
        rate_of_fire=1200,
        magazine_capacity=50,
        ammo_given=200,
        sprite="minigun.png"
    ),

    dict(
        name="SMAW",
        damage=100,
        accuracy=0,
        reload_time=4.0,
        melee=35,
        rpf=1,
        effective_range=1,
        dual_wielding=False,
        rate_of_fire=30,
        magazine_capacity=3,
        ammo_given=6,
        sprite="smaw.png"
    ),
]
