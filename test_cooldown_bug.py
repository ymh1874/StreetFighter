"""Verify the special move cooldown bug"""
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

# Create fighter
khalid = create_fighter(0, 1)
target = create_fighter(1, 2)

print(f"Initial last_special_time: {khalid.last_special_time}")
print(f"Current time: {pygame.time.get_ticks()}")
print(f"Time difference: {pygame.time.get_ticks() - khalid.last_special_time}")
print(f"Cooldown requirement: 2000")
print(f"Can use special: {pygame.time.get_ticks() - khalid.last_special_time >= 2000}")

# Try using special
result = khalid.attack(target, 'special')
print(f"\nFirst attempt result: {result}")

# Wait long enough
pygame.time.wait(2100)
print(f"\nAfter waiting 2100ms:")
print(f"Current time: {pygame.time.get_ticks()}")

result2 = khalid.attack(target, 'special')
print(f"Second attempt result: {result2}")
print(f"Second attempt type: {type(result2)}")
