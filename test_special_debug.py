"""Debug test for special moves"""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'

import pygame
pygame.init()

from entities import Fighter
import config as c

def create_fighter(char_index, player_num):
    controls = {
        'left': pygame.K_a,
        'right': pygame.K_d,
        'jump': pygame.K_w,
        'light_punch': pygame.K_j,
        'heavy_punch': pygame.K_k,
        'light_kick': pygame.K_l,
        'heavy_kick': pygame.K_i,
        'special': pygame.K_u
    }
    return Fighter(100 if player_num == 1 else 700, 400, c.CHARACTERS[char_index], controls)

# Test Khalid's special
khalid = create_fighter(0, 1)
target = create_fighter(1, 2)

print(f"Khalid stats: {khalid.stats}")
print(f"Special type: {khalid.stats.get('special', 'NOT FOUND')}")
print(f"Last special time: {khalid.last_special_time}")
print(f"Current time: {pygame.time.get_ticks()}")

khalid.attacking = False
khalid.last_attack_time = 0
khalid.last_special_time = 0

print(f"Before attack - attacking: {khalid.attacking}")

# Add some time to ensure cooldown check passes
pygame.time.wait(100)  # Wait 100ms

result = khalid.execute_special_move(target)
print(f"Direct execute_special_move result: {result}")

# Now try through attack method
khalid.attacking = False
khalid.last_special_time = 0
result2 = khalid.attack(target, 'special')
print(f"Through attack() result: {result2}")
print(f"Result type: {type(result2)}")

# Test all characters
chars = ['Khalid', 'Eduardo', 'Hasan', 'Hammoud']
for i, name in enumerate(chars):
    fighter = create_fighter(i, 1)
    target = create_fighter(0, 2)
    fighter.attacking = False
    fighter.last_attack_time = 0
    fighter.last_special_time = 0
    
    result = fighter.attack(target, 'special')
    print(f"{name} special result: {result}, type: {type(result)}")
