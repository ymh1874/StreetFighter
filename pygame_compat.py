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
if not pygame.get_init():
    pygame.init()

# Export commonly used pygame constants for convenience
# These are accessed after pygame.init() to ensure they exist

def get_key_constants():
    """
    Returns a dictionary of key constants.
    Call this AFTER pygame.init() to ensure constants are available.
    """
    return {
        # Letters
        'K_a': pygame.K_a,
        'K_b': pygame.K_b,
        'K_c': pygame.K_c,
        'K_d': pygame.K_d,
        'K_e': pygame.K_e,
        'K_f': pygame.K_f,
        'K_g': pygame.K_g,
        'K_h': pygame.K_h,
        'K_i': pygame.K_i,
        'K_j': pygame.K_j,
        'K_k': pygame.K_k,
        'K_l': pygame.K_l,
        'K_m': pygame.K_m,
        'K_n': pygame.K_n,
        'K_o': pygame.K_o,
        'K_p': pygame.K_p,
        'K_q': pygame.K_q,
        'K_r': pygame.K_r,
        'K_s': pygame.K_s,
        'K_t': pygame.K_t,
        'K_u': pygame.K_u,
        'K_v': pygame.K_v,
        'K_w': pygame.K_w,
        'K_x': pygame.K_x,
        'K_y': pygame.K_y,
        'K_z': pygame.K_z,
        # Arrows
        'K_UP': pygame.K_UP,
        'K_DOWN': pygame.K_DOWN,
        'K_LEFT': pygame.K_LEFT,
        'K_RIGHT': pygame.K_RIGHT,
        # Modifiers
        'K_LSHIFT': pygame.K_LSHIFT,
        'K_RSHIFT': pygame.K_RSHIFT,
        'K_LCTRL': pygame.K_LCTRL,
        'K_RCTRL': pygame.K_RCTRL,
        'K_LALT': pygame.K_LALT,
        'K_RALT': pygame.K_RALT,
        'K_SPACE': pygame.K_SPACE,
        'K_RETURN': pygame.K_RETURN,
        'K_ESCAPE': pygame.K_ESCAPE,
        # Numpad
        'K_KP0': pygame.K_KP0,
        'K_KP1': pygame.K_KP1,
        'K_KP2': pygame.K_KP2,
        'K_KP3': pygame.K_KP3,
        'K_KP4': pygame.K_KP4,
        'K_KP5': pygame.K_KP5,
        'K_KP6': pygame.K_KP6,
        'K_KP7': pygame.K_KP7,
        'K_KP8': pygame.K_KP8,
        'K_KP9': pygame.K_KP9,
    }
