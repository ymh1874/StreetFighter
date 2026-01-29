"""
Pygame compatibility layer for CMU Arcade Box

This module handles the case where a fake/shim pygame (from cmu_graphics)
shadows the real pygame. It detects, purges, and reloads the real pygame.

Usage: from pygame_compat import pygame
"""

import sys
import os

def _debug_log(msg):
    """Print debug info - helps diagnose issues on arcade machine"""
    print(f"[pygame_compat] {msg}")

def load_robust_pygame():
    """
    Attempts to import the REAL pygame.
    If a shim/wrapper (like cmu_graphics) is detected, it purges it 
    from sys.modules and sys.path, then retries.
    """
    
    _debug_log(f"Python executable: {sys.executable}")
    _debug_log(f"Python version: {sys.version}")
    
    # 1. First, check if there's a local pygame.py file shadowing the real one
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_pygame_file = os.path.join(script_dir, 'pygame.py')
    local_pygame_folder = os.path.join(script_dir, 'pygame')
    
    if os.path.exists(local_pygame_file):
        _debug_log(f"WARNING: Found local pygame.py at {local_pygame_file} - this may shadow real pygame!")
    if os.path.exists(local_pygame_folder):
        _debug_log(f"WARNING: Found local pygame/ folder at {local_pygame_folder} - this may shadow real pygame!")
    
    # 2. Clean sys.path BEFORE first import - remove cmu_graphics paths
    bad_paths = []
    for p in sys.path[:]:  # Iterate copy
        if 'cmu_graphics' in p or 'cmu-graphics' in p:
            bad_paths.append(p)
            sys.path.remove(p)
    
    if bad_paths:
        _debug_log(f"Removed bad paths: {bad_paths}")
    
    # 3. Clear any cached pygame imports (but preserve our own module)
    pygame_modules = [key for key in list(sys.modules.keys()) 
                      if 'pygame' in key.lower() and key != 'pygame_compat']
    for mod in pygame_modules:
        _debug_log(f"Removing cached module: {mod}")
        del sys.modules[mod]
    
    # 4. Try standard import
    pygame = None
    try:
        import pygame as _pygame
        pygame = _pygame
        _debug_log(f"Imported pygame from: {getattr(pygame, '__file__', 'unknown')}")
        _debug_log(f"Pygame version: {getattr(pygame, '__version__', 'unknown')}")
    except ImportError as e:
        _debug_log(f"First import failed: {e}")
        pygame = None

    # 5. Check if this is the "Imposter" Pygame
    if pygame and (not hasattr(pygame, 'init') or not hasattr(pygame, 'display')):
        _debug_log("WARNING: 'Imposter' pygame detected (missing init/display). Purging...")
        
        bad_file = getattr(pygame, '__file__', '')
        bad_path = os.path.dirname(bad_file) if bad_file else ''
        _debug_log(f"Bad pygame location: {bad_file}")
        
        # Remove the bad module from memory (except our own)
        pygame_modules = [key for key in list(sys.modules.keys()) 
                          if 'pygame' in key.lower() and key != 'pygame_compat']
        for mod in pygame_modules:
            del sys.modules[mod]
        
        # Remove the bad path from sys.path
        if bad_path and bad_path in sys.path:
            sys.path.remove(bad_path)
        
        # Force re-import
        pygame = None
        try:
            import pygame as _pygame
            pygame = _pygame
            _debug_log(f"Re-imported pygame from: {getattr(pygame, '__file__', 'unknown')}")
        except ImportError as e:
            _debug_log(f"Re-import failed: {e}")

    # 6. Final verification
    if pygame is None or not hasattr(pygame, 'init'):
        _debug_log("ERROR: Could not load valid pygame!")
        _debug_log(f"Pygame object: {pygame}")
        _debug_log(f"Has init: {hasattr(pygame, 'init') if pygame else False}")
        _debug_log(f"Has display: {hasattr(pygame, 'display') if pygame else False}")
        _debug_log("--- SYS.PATH ---")
        for p in sys.path:
            _debug_log(f"  {p}")
        
        raise ImportError(
            f"Failed to load valid pygame. "
            f"Loaded module: {pygame}. "
            f"File: {getattr(pygame, '__file__', 'unknown') if pygame else 'None'}. "
            "Ensure pygame is installed: pip install pygame"
        )
    
    _debug_log(f"SUCCESS: Valid pygame loaded with init() and display")
    return pygame


# Load the verified pygame
pygame = load_robust_pygame()

# Initialize pygame
pygame.init()
_debug_log("pygame.init() called successfully")

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
