"""Test combo mechanics in realistic game scenario"""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'

import pygame
pygame.init()

from entities import Fighter
from combat import CombatSystem
import config as c

def create_fighter(char_index, player_num, combat_system, fighter_id):
    controls = {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
                'light_punch': pygame.K_j, 'heavy_punch': pygame.K_k,
                'light_kick': pygame.K_l, 'heavy_kick': pygame.K_i, 'special': pygame.K_u}
    return Fighter(100 if player_num == 1 else 700, 400, c.CHARACTERS[char_index], controls, 
                   is_p2=(player_num==2), combat_system=combat_system, fighter_id=fighter_id)

# Create combat system
combat_system = CombatSystem()
combat_system.register_fighter("p1")
combat_system.register_fighter("p2")

# Create fighters with combat system
attacker = create_fighter(0, 1, combat_system, "p1")  # Khalid
target = create_fighter(1, 2, combat_system, "p2")    # Eduardo

# Position target in range
target.rect.x = attacker.rect.right + 10

print("="*60)
print("COMBO TEST - Simulating Real Game Scenario")
print("="*60)
print(f"Attacker: Khalid (dmg mult: {attacker.dmg_mult})")
print(f"Target: Eduardo (initial health: {target.health})")
print()

# Sequence of attacks
attacks = [
    ('light_punch', 5.0, 1.0),  # Hit 1 - full damage
    ('light_kick', 8.0, 1.0),   # Hit 2 - full damage
    ('heavy_punch', 12.0, 1.0), # Hit 3 - full damage
    ('light_punch', 5.0, 0.8),  # Hit 4 - 80% damage
    ('heavy_kick', 15.0, 0.8),  # Hit 5 - 80% damage
]

current_health = target.health

for i, (attack_type, base_damage, expected_scaling) in enumerate(attacks, 1):
    # Wait for attack to finish
    pygame.time.wait(100)
    
    # Reset attack state
    attacker.attacking = False
    attacker.last_attack_time = 0
    attacker.update()  # Clear attack_rect
    
    # Position target in range (accounting for knockback)
    target.rect.x = attacker.rect.right + 10
    
    # Execute attack
    result = attacker.attack(target, attack_type)
    
    # Calculate expected damage
    expected_damage = base_damage * attacker.dmg_mult * expected_scaling
    expected_new_health = current_health - expected_damage
    
    # Get combo info (don't increment, attack already did that)
    combo_count = combat_system.get_combo_count("p1")
    combo_scaling = combat_system.get_combo_damage_multiplier("p1")
    
    print(f"Hit {i}: {attack_type:15}")
    print(f"  Hit: {result}")
    print(f"  Base damage: {base_damage}")
    print(f"  Expected scaling: {expected_scaling}")
    print(f"  Combo count: {combo_count}")
    print(f"  Combo scaling from system: {combo_scaling}")
    print(f"  Expected new health: {expected_new_health:.1f}")
    print(f"  Actual new health: {target.health:.1f}")
    print(f"  Damage dealt: {current_health - target.health:.1f}")
    print()
    
    current_health = target.health

print(f"Final combo count: {combat_system.get_combo_count('p1')}")
print(f"Total damage dealt: {95 - target.health:.1f}")
