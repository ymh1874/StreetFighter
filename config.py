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

# Skin tones
KHALID_SKIN = (101, 67, 33)  # Dark brown
EDUARDO_SKIN = (210, 180, 140)  # Tan
HASAN_SKIN = (194, 140, 80)  # Medium brown
HAMMOUD_SKIN = (220, 190, 150)  # Light tan

# Outfit colors
KHALID_GI = (255, 165, 0)  # Orange
EDUARDO_APRON = (220, 20, 60)  # Red
EDUARDO_HAT = (255, 255, 255)  # White
HASAN_ROBE = (255, 215, 0)  # Gold/yellow
HAMMOUD_COAT = (34, 139, 34)  # Green

# Effect colors
COMIC_TEXT = (255, 255, 0)  # Yellow for "POW!"
COMIC_OUTLINE = (0, 0, 0)  # Black outline
DIRT_BROWN = (139, 90, 43)  # Dirt brown ground

# Physics Defaults
GRAVITY = 0.8
FLOOR_Y = SCREEN_HEIGHT - 100
P_WIDTH = 50
P_HEIGHT = 100

# Professor Character Definitions
CHARACTERS = [
    {
        'name': 'PROF. KHALID', 
        'color': KHALID_GI,
        'skin': KHALID_SKIN,
        'speed': 6, 
        'jump': -19, 
        'health': 110, 
        'dmg_mult': 1.0, 
        'desc': 'TAEKWONDO MASTER',
        'special': 'spinning_kick'
    },
    {
        'name': 'PROF. EDUARDO', 
        'color': EDUARDO_APRON,
        'skin': EDUARDO_SKIN,
        'speed': 5, 
        'jump': -16, 
        'health': 95, 
        'dmg_mult': 0.9, 
        'desc': 'PIZZA MASTER',
        'special': 'pizza_throw'
    },
    {
        'name': 'PROF. HASAN', 
        'color': HASAN_ROBE,
        'skin': HASAN_SKIN,
        'speed': 5, 
        'jump': -18, 
        'health': 100, 
        'dmg_mult': 1.1, 
        'desc': 'PYROMANCER',
        'special': 'fireball'
    },
    {
        'name': 'PROF. HAMMOUD', 
        'color': HAMMOUD_COAT,
        'skin': HAMMOUD_SKIN,
        'speed': 7, 
        'jump': -20, 
        'health': 85, 
        'dmg_mult': 0.85, 
        'desc': 'TECH WIZARD',
        'special': 'circuit_board'
    },
]

# Attack Frame Data
FRAME_DATA = {
    'light_punch': {'startup': 3, 'active': 2, 'recovery': 5, 'total': 10, 'can_move_early': True},
    'heavy_punch': {'startup': 8, 'active': 4, 'recovery': 15, 'total': 27, 'can_move_early': False},
    'light_kick': {'startup': 4, 'active': 3, 'recovery': 6, 'total': 13, 'can_move_early': True},
    'heavy_kick': {'startup': 10, 'active': 5, 'recovery': 18, 'total': 33, 'can_move_early': False},
    'special': {'startup': 12, 'active': 10, 'recovery': 20, 'total': 42, 'can_move_early': False},
    'block': {'startup': 5, 'active': -1, 'recovery': 3, 'total': -1, 'can_move_early': True},
    'dash': {'startup': 2, 'active': 8, 'recovery': 5, 'total': 15, 'can_move_early': True},
}

# Combo System
MAX_COMBO_HITS = 5
COMBO_DAMAGE_SCALING = {
    1: 1.0,  # First hit
    2: 1.0,  # Second hit
    3: 1.0,  # Third hit
    4: 0.8,  # Fourth hit - 80% damage
    5: 0.8,  # Fifth hit - 80% damage
}