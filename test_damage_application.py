"""Test if damage is applied correctly and not duplicated"""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'

import pygame
pygame.init()

from entities import Fighter
import config as c

def create_fighter(char_index, player_num):
    controls = {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
                'light_punch': pygame.K_j, 'heavy_punch': pygame.K_k,
                'light_kick': pygame.K_l, 'heavy_kick': pygame.K_i, 'special': pygame.K_u}
    return Fighter(100 if player_num == 1 else 700, 400, c.CHARACTERS[char_index], controls)

# Create fighters
attacker = create_fighter(0, 1)  # Khalid
target = create_fighter(1, 2)    # Eduardo

# Position target in range
target.rect.x = attacker.rect.right + 10

print(f"Initial target health: {target.health}")
print(f"Attacker damage multiplier: {attacker.dmg_mult}")
print(f"Light punch damage: {attacker.moves['light_punch'].damage}")

# Execute attack
attacker.attacking = False
attacker.last_attack_time = 0
result = attacker.attack(target, 'light_punch')

print(f"\nAfter attack:")
print(f"Attack hit: {result}")
print(f"Target health: {target.health}")
print(f"Expected health: {95 - 5.0} = 90.0")
print(f"Damage dealt: {95 - target.health}")

# Check if damage matches expected
expected_damage = 5.0 * 1.0  # base * multiplier
expected_health = 95 - expected_damage
print(f"\nDamage correct: {target.health == expected_health}")
