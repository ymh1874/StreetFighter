"""
Pygame compatibility layer for CMU Arcade Box

This module provides a unified way to import pygame that works both:
1. On regular systems with standard pygame
2. On the CMU arcade box with cmu_graphics' bundled pygame

Usage: Instead of `import pygame`, use:
    from pygame_compat import pygame
"""

# Try multiple import paths for pygame compatibility
pygame = None

try:
    # First, try the cmu_graphics bundled pygame (arcade box)
    from cmu_graphics.libs import pygame_loader as pygame
except ImportError:
    pass

if pygame is None:
    try:
        # Fall back to standard pygame
        import pygame as _pygame
        pygame = _pygame
    except ImportError:
        raise ImportError(
            "Could not import pygame. Please install it with: pip install pygame"
        )

# Ensure pygame is initialized for key constants to be available
# Use try/except for arcade box compatibility (some pygame builds lack get_init)
try:
    if hasattr(pygame, 'get_init') and not pygame.get_init():
        pygame.init()
    elif not hasattr(pygame, 'get_init'):
        # Arcade box pygame - just call init (it's safe to call multiple times)
        pygame.init()
except Exception:
    # If anything fails, try to initialize anyway
    try:
        pygame.init()
    except Exception:
        pass  # Already initialized or not needed

# ============================================================
# KEY CONSTANT FALLBACKS
# The CMU arcade box pygame doesn't always have key constants.
# We define them with their standard SDL key values as fallbacks.
# ============================================================

# Standard SDL key values (these are the actual integer values pygame uses)
_KEY_CONSTANTS = {
    # Letters (a=97 in ASCII, SDL uses same values)
    'K_a': 97, 'K_b': 98, 'K_c': 99, 'K_d': 100, 'K_e': 101,
    'K_f': 102, 'K_g': 103, 'K_h': 104, 'K_i': 105, 'K_j': 106,
    'K_k': 107, 'K_l': 108, 'K_m': 109, 'K_n': 110, 'K_o': 111,
    'K_p': 112, 'K_q': 113, 'K_r': 114, 'K_s': 115, 'K_t': 116,
    'K_u': 117, 'K_v': 118, 'K_w': 119, 'K_x': 120, 'K_y': 121,
    'K_z': 122,
    # Arrow keys
    'K_UP': 1073741906, 'K_DOWN': 1073741905,
    'K_LEFT': 1073741904, 'K_RIGHT': 1073741903,
    # Modifiers
    'K_LSHIFT': 1073742049, 'K_RSHIFT': 1073742053,
    'K_LCTRL': 1073742048, 'K_RCTRL': 1073742052,
    'K_LALT': 1073742050, 'K_RALT': 1073742054,
    # Common keys
    'K_SPACE': 32, 'K_RETURN': 13, 'K_ESCAPE': 27,
    'K_BACKSPACE': 8, 'K_TAB': 9, 'K_DELETE': 127,
    # Numbers (top row)
    'K_0': 48, 'K_1': 49, 'K_2': 50, 'K_3': 51, 'K_4': 52,
    'K_5': 53, 'K_6': 54, 'K_7': 55, 'K_8': 56, 'K_9': 57,
    # Numpad
    'K_KP0': 1073741922, 'K_KP1': 1073741913, 'K_KP2': 1073741914,
    'K_KP3': 1073741915, 'K_KP4': 1073741916, 'K_KP5': 1073741917,
    'K_KP6': 1073741918, 'K_KP7': 1073741919, 'K_KP8': 1073741920,
    'K_KP9': 1073741921,
    # Function keys
    'K_F1': 1073741882, 'K_F2': 1073741883, 'K_F3': 1073741884,
    'K_F4': 1073741885, 'K_F5': 1073741886, 'K_F6': 1073741887,
    'K_F7': 1073741888, 'K_F8': 1073741889, 'K_F9': 1073741890,
    'K_F10': 1073741891, 'K_F11': 1073741892, 'K_F12': 1073741893,
}

# Inject missing key constants into the pygame module
for key_name, key_value in _KEY_CONSTANTS.items():
    if not hasattr(pygame, key_name):
        setattr(pygame, key_name, key_value)

# Also handle event types that might be missing
_EVENT_CONSTANTS = {
    'QUIT': 256,
    'KEYDOWN': 768,
    'KEYUP': 769,
    'MOUSEMOTION': 1024,
    'MOUSEBUTTONDOWN': 1025,
    'MOUSEBUTTONUP': 1026,
    'JOYAXISMOTION': 1536,
    'JOYBUTTONDOWN': 1539,
    'JOYBUTTONUP': 1540,
    'JOYDEVICEADDED': 1541,
    'JOYDEVICEREMOVED': 1542,
}

for event_name, event_value in _EVENT_CONSTANTS.items():
    if not hasattr(pygame, event_name):
        setattr(pygame, event_name, event_value)


def get_key_constants():
    """
    Returns a dictionary of key constants.
    Call this AFTER pygame.init() to ensure constants are available.
    """
    return {key: getattr(pygame, key) for key in _KEY_CONSTANTS.keys()}
