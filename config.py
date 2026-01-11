import pygame

# --- CONFIGURATION & CONSTANTS ---
# Internal logic resolution (scales up to fullscreen automatically)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)
GREEN = (50, 255, 50)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (100, 100, 100)
DARK_GRAY = (40, 40, 40)

# Physics Defaults
GRAVITY = 0.8
FLOOR_Y = SCREEN_HEIGHT - 100
P_WIDTH = 50
P_HEIGHT = 100

# Combat
FIREBALL_SPEED = 12

# Character Archetypes
CHARACTERS = [
    {'name': 'RYU-LIKE', 'color': RED, 'speed': 5, 'jump': -18, 'health': 100, 'dmg_mult': 1.0},
    {'name': 'ZANGIEF-LIKE', 'color': GREEN, 'speed': 3, 'jump': -15, 'health': 140, 'dmg_mult': 1.3},
    {'name': 'CHUN-LIKE', 'color': YELLOW, 'speed': 7, 'jump': -20, 'health': 80, 'dmg_mult': 0.8},
    {'name': 'BISON-LIKE', 'color': PURPLE, 'speed': 4, 'jump': -17, 'health': 110, 'dmg_mult': 1.1},
]