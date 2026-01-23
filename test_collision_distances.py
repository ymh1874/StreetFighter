"""Test for collision detection issues"""
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

# Test collision detection for all attacks
khalid = create_fighter(0, 1)
target = create_fighter(1, 2)

print("=" * 60)
print("COLLISION DETECTION TEST")
print("=" * 60)

# Position fighters at different distances
distances = [
    (0, "Overlapping"),
    (10, "Very close (10px)"),
    (30, "Close (30px)"),
    (60, "Medium (60px)"),
    (90, "Far (90px)"),
    (120, "Very far (120px)"),
]

attack_types = ['light_punch', 'heavy_punch', 'light_kick', 'heavy_kick']

for distance, desc in distances:
    # Reset fighters
    khalid = create_fighter(0, 1)
    target = create_fighter(1, 2)
    
    # Position target at specific distance
    target.rect.x = khalid.rect.right + distance
    
    print(f"\n--- Distance: {desc} ---")
    print(f"Khalid right edge: {khalid.rect.right}")
    print(f"Target left edge: {target.rect.left}")
    print(f"Actual distance: {target.rect.left - khalid.rect.right}px")
    
    for attack_type in attack_types:
        khalid.attacking = False
        khalid.last_attack_time = 0
        
        initial_health = target.health
        result = khalid.attack(target, attack_type)
        
        if khalid.attack_rect:
            hit = khalid.attack_rect.colliderect(target.rect)
            width = khalid.moves[attack_type].width
            print(f"  {attack_type:15} - width:{width:3}px, hit:{hit}, returned:{result}")
