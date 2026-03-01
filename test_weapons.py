"""
Weapon System Test & Showcase
Run this to see all available weapons and their stats
"""

from weapons import WEAPONS, get_all_weapon_names
import pygame
from weapon_renderer import WeaponRenderer
import math

def showcase_weapons():
    """Display all weapon information"""
    print("=" * 60)
    print("PYTANKS WEAPON ARSENAL")
    print("=" * 60)
    
    for weapon_id in sorted(WEAPONS.keys()):
        gun = WEAPONS[weapon_id]
        print(f"\n[{weapon_id}] {gun.name}")
        print(f"  Damage: {gun.damage} | RPF: {gun.rpf} | Magazine: {gun.magazine_capacity}")
        print(f"  Rate of Fire: {gun.rate_of_fire}s | Reload: {gun.reload_time}s")
        print(f"  Range: {gun.effective_range}px | Accuracy: {gun.accuracy}°")
        print(f"  Bullet Speed: {gun.bullet_speed} | Melee: {gun.melee_damage}")
        print(f"  Dual Wield: {'Yes' if gun.dual_wielding else 'No'}")
        print(f"  Ammo: {gun.magazine_capacity}/{gun.ammo_given}")
        print(f"  Sprite: {gun.sprite_file}")


def visual_showcase():
    """Visual showcase of all weapons"""
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("PyTanks Weapon Showcase")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 20)
    title_font = pygame.font.SysFont(None, 32)
    
    renderer = WeaponRenderer()
    running = True
    angle = 0
    
    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.fill((30, 30, 40))
        
        # Title
        title = title_font.render("PyTanks Weapon Arsenal", True, (255, 255, 255))
        screen.blit(title, (350, 20))
        
        # Rotate angle for visual effect
        angle += 0.02
        
        # Display weapons in a grid
        weapons_per_row = 3
        x_start = 100
        y_start = 80
        x_spacing = 300
        y_spacing = 150
        
        for weapon_id in sorted(WEAPONS.keys()):
            gun = WEAPONS[weapon_id]
            row = weapon_id // weapons_per_row
            col = weapon_id % weapons_per_row
            
            x = x_start + col * x_spacing
            y = y_start + row * y_spacing
            
            # Draw background box
            box_rect = pygame.Rect(x - 40, y - 30, 280, 120)
            pygame.draw.rect(screen, (50, 50, 60), box_rect)
            pygame.draw.rect(screen, (100, 150, 200), box_rect, 2)
            
            # Draw weapon
            weapon_x = x + 50
            weapon_y = y + 20
            # Draw rotating weapon
            display_angle = angle + (weapon_id * 0.3)
            renderer.draw_gun(screen, weapon_x, weapon_y, display_angle, gun, tank_radius=15)
            
            # Draw weapon name
            name_surf = font.render(gun.name, True, (255, 255, 255))
            screen.blit(name_surf, (x - 30, y - 20))
            
            # Draw stats
            stats_y = y + 40
            stats = [
                f"DMG:{gun.damage} RNG:{gun.effective_range}",
                f"MAG:{gun.magazine_capacity} RLD:{gun.reload_time}s",
                f"ROF:{gun.rate_of_fire}s SPD:{gun.bullet_speed}"
            ]
            
            for i, stat in enumerate(stats):
                stat_surf = font.render(stat, True, (200, 200, 200))
                screen.blit(stat_surf, (x - 30, stats_y + i * 18))
        
        # Instructions
        inst = font.render("Press ESC to exit", True, (150, 150, 150))
        screen.blit(inst, (450, 770))
        
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("PyTanks Weapon System")
    print("="*60)
    print("\n1. Text showcase")
    print("2. Visual showcase (pygame)")
    print("\nStarting visual showcase in 2 seconds...")
    print("(Press ESC in the window to exit)\n")
    
    import time
    time.sleep(2)
    
    showcase_weapons()
    print("\n" + "="*60)
    visual_showcase()
