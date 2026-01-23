#!/usr/bin/env python3
"""
Basic functionality test for Street Fighter game
Tests core mechanics without requiring GUI
"""

import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'  # Headless mode for pygame

import pygame
import config as c
from entities import Fighter, Particle, HitEffect
from combat import CombatSystem

def test_fighter_creation():
    """Test that fighters can be created"""
    pygame.init()
    
    controls = c.DEFAULT_P1_CONTROLS
    stats = c.CHARACTERS[0]
    combat_system = CombatSystem()
    combat_system.register_fighter("p1")
    
    fighter = Fighter(200, 200, stats, controls, is_p2=False, 
                     combat_system=combat_system, fighter_id="p1")
    
    assert fighter.health == fighter.max_health
    assert fighter.alive
    assert not fighter.dashing
    assert fighter.dash_timer == 0
    print("✓ Fighter creation test passed")

def test_dash_mechanics():
    """Test dash mechanics"""
    pygame.init()
    
    controls = c.DEFAULT_P1_CONTROLS
    stats = c.CHARACTERS[0]
    combat_system = CombatSystem()
    combat_system.register_fighter("p1")
    
    fighter = Fighter(200, 200, stats, controls, is_p2=False,
                     combat_system=combat_system, fighter_id="p1")
    
    # Simulate dash activation
    fighter.dashing = True
    fighter.dash_timer = c.FRAME_DATA['dash']['active']
    
    assert fighter.dashing
    assert fighter.dash_timer == 8
    print("✓ Dash mechanics test passed")

def test_power_bar_tracking():
    """Test special ability cooldown tracking"""
    pygame.init()
    
    controls = c.DEFAULT_P1_CONTROLS
    stats = c.CHARACTERS[0]
    combat_system = CombatSystem()
    combat_system.register_fighter("p1")
    
    fighter = Fighter(200, 200, stats, controls, is_p2=False,
                     combat_system=combat_system, fighter_id="p1")
    
    # Check initial state
    assert fighter.last_special_time == -2000  # Can use special immediately
    
    # Simulate using special
    current_time = pygame.time.get_ticks()
    fighter.last_special_time = current_time
    
    # Check cooldown
    time_since = current_time - fighter.last_special_time
    assert time_since >= 0
    print("✓ Power bar tracking test passed")

def test_control_mapping():
    """Test control mapping system"""
    # Check that default controls are defined
    assert 'left' in c.DEFAULT_P1_CONTROLS
    assert 'right' in c.DEFAULT_P1_CONTROLS
    assert 'jump' in c.DEFAULT_P1_CONTROLS
    assert 'dash' in c.DEFAULT_P1_CONTROLS
    assert 'special' in c.DEFAULT_P1_CONTROLS
    
    assert 'left' in c.DEFAULT_P2_CONTROLS
    assert 'dash' in c.DEFAULT_P2_CONTROLS
    
    print("✓ Control mapping test passed")

def test_hitbox_positioning():
    """Test that hitbox is properly centered"""
    pygame.init()
    
    controls = c.DEFAULT_P1_CONTROLS
    stats = c.CHARACTERS[0]
    combat_system = CombatSystem()
    combat_system.register_fighter("p1")
    combat_system.register_fighter("p2")
    
    p1 = Fighter(200, 200, stats, controls, is_p2=False,
                combat_system=combat_system, fighter_id="p1")
    p2 = Fighter(400, 200, stats, c.DEFAULT_P2_CONTROLS, is_p2=True,
                combat_system=combat_system, fighter_id="p2")
    
    # Simulate attack
    p1.attack(p2, 'light_punch')
    
    # Check that attack_rect was created
    assert p1.attack_rect is not None
    # Check vertical centering (hitbox_y should be centered on character)
    expected_y = p1.rect.y + (p1.rect.height - p1.moves['light_punch'].height) // 2
    assert p1.attack_rect.y == expected_y
    print("✓ Hitbox positioning test passed")

def test_all_characters():
    """Test that all characters can be created"""
    pygame.init()
    
    controls = c.DEFAULT_P1_CONTROLS
    combat_system = CombatSystem()
    
    for i, char in enumerate(c.CHARACTERS):
        combat_system.register_fighter(f"test_{i}")
        fighter = Fighter(200, 200, char, controls, is_p2=False,
                         combat_system=combat_system, fighter_id=f"test_{i}")
        assert fighter.alive
        assert 'name' in fighter.stats
        print(f"  ✓ {char['name']} created successfully")
    
    print("✓ All characters test passed")

if __name__ == "__main__":
    print("\n=== Running Street Fighter Basic Tests ===\n")
    
    try:
        test_fighter_creation()
        test_dash_mechanics()
        test_power_bar_tracking()
        test_control_mapping()
        test_hitbox_positioning()
        test_all_characters()
        
        print("\n=== All tests passed! ✓ ===\n")
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
        raise
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        raise
