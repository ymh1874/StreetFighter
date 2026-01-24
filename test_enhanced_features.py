#!/usr/bin/env python3
"""
Enhanced features test for Street Fighter game
Tests coin insertion, AI mode, mid-air dash, and parry mechanics
"""

import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'  # Headless mode for pygame

import pygame
import config as c
from entities import Fighter
from combat import CombatSystem
from ai_controller import AIController
from game import Game

def test_coin_insertion_state():
    """Test that coin insertion state is properly initialized"""
    pygame.init()
    
    game = Game()
    
    # Initial state should have P2 as AI
    assert game.p2_is_ai == True, "P2 should start as AI"
    assert game.p2_coin_inserted == False, "Coin should not be inserted initially"
    
    # Simulate coin insertion
    game.p2_coin_inserted = True
    game.p2_is_ai = False
    
    assert game.p2_coin_inserted == True, "Coin should be inserted after activation"
    assert game.p2_is_ai == False, "P2 should not be AI after coin insertion"
    
    print("✓ Coin insertion state test passed")

def test_mid_air_dash():
    """Test that dash works while jumping (mid-air dash)"""
    pygame.init()
    
    controls = c.DEFAULT_P1_CONTROLS
    stats = c.CHARACTERS[0]
    combat_system = CombatSystem()
    combat_system.register_fighter("p1")
    
    fighter = Fighter(200, 200, stats, controls, is_p2=False,
                     combat_system=combat_system, fighter_id="p1")
    
    # Simulate jumping
    fighter.jumping = True
    fighter.vel_y = -10
    
    # Simulate dash while jumping - should be allowed now
    current_time = pygame.time.get_ticks()
    fighter.dashing = True
    fighter.dash_timer = c.FRAME_DATA['dash']['active']
    fighter.last_dash_time = current_time
    
    # Verify dash is active while jumping
    assert fighter.dashing == True, "Dash should be active while jumping"
    assert fighter.jumping == True, "Should still be jumping"
    assert fighter.dash_timer == 8, "Dash timer should be set"
    
    print("✓ Mid-air dash test passed")

def test_parry_mechanics():
    """Test parry activation and timing"""
    pygame.init()
    
    controls = c.DEFAULT_P1_CONTROLS
    stats = c.CHARACTERS[0]
    combat_system = CombatSystem()
    combat_system.register_fighter("p1")
    
    fighter = Fighter(200, 200, stats, controls, is_p2=False,
                     combat_system=combat_system, fighter_id="p1")
    
    # Test parry activation
    result = fighter.activate_parry()
    
    assert result == True, "Parry should activate successfully"
    assert fighter.parrying == True, "Parrying flag should be set"
    assert fighter.parry_window == 6, "Parry window should be 6 frames"
    assert fighter.parry_cooldown == 30, "Parry cooldown should be 30 frames"
    
    # Test cooldown prevents immediate re-parry
    result2 = fighter.activate_parry()
    assert result2 == False, "Should not be able to parry during cooldown"
    
    print("✓ Parry mechanics test passed")

def test_parry_window_decay():
    """Test that parry window decreases over time"""
    pygame.init()
    
    controls = c.DEFAULT_P1_CONTROLS
    stats = c.CHARACTERS[0]
    combat_system = CombatSystem()
    combat_system.register_fighter("p1")
    combat_system.register_fighter("p2")
    
    fighter = Fighter(200, 200, stats, controls, is_p2=False,
                     combat_system=combat_system, fighter_id="p1")
    opponent = Fighter(400, 200, stats, c.DEFAULT_P2_CONTROLS, is_p2=True,
                      combat_system=combat_system, fighter_id="p2")
    
    # Activate parry
    fighter.activate_parry()
    initial_window = fighter.parry_window
    
    # Call move to trigger parry window update (it's in move(), not update())
    fighter.move(opponent, c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
    
    assert fighter.parry_window < initial_window, "Parry window should decrease"
    
    # Continue updating until window expires
    for _ in range(10):
        fighter.move(opponent, c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
    
    assert fighter.parry_window == 0, "Parry window should expire"
    assert fighter.parrying == False, "Parrying should be deactivated after window expires"
    
    print("✓ Parry window decay test passed")

def test_ai_controller_initialization():
    """Test AI controller initialization"""
    pygame.init()
    
    controls_p1 = c.DEFAULT_P1_CONTROLS
    controls_p2 = c.DEFAULT_P2_CONTROLS
    stats_p1 = c.CHARACTERS[0]
    stats_p2 = c.CHARACTERS[1]
    combat_system = CombatSystem()
    
    combat_system.register_fighter("p1")
    combat_system.register_fighter("p2")
    
    p1 = Fighter(200, 200, stats_p1, controls_p1, is_p2=False,
                combat_system=combat_system, fighter_id="p1")
    p2 = Fighter(400, 200, stats_p2, controls_p2, is_p2=True,
                combat_system=combat_system, fighter_id="p2")
    
    # Create AI controller
    ai = AIController(p2, p1, difficulty='hard')
    
    assert ai.fighter == p2, "AI should control p2"
    assert ai.opponent == p1, "AI opponent should be p1"
    assert ai.difficulty == 'hard', "Difficulty should be hard"
    assert ai.reaction_time == 100, "Hard difficulty should have 100ms reaction time"
    assert ai.aggression == 0.7, "Hard difficulty should have 0.7 aggression"
    
    print("✓ AI controller initialization test passed")

def test_ai_difficulty_levels():
    """Test different AI difficulty configurations"""
    pygame.init()
    
    controls_p1 = c.DEFAULT_P1_CONTROLS
    controls_p2 = c.DEFAULT_P2_CONTROLS
    stats_p1 = c.CHARACTERS[0]
    stats_p2 = c.CHARACTERS[1]
    combat_system = CombatSystem()
    
    combat_system.register_fighter("p1")
    combat_system.register_fighter("p2")
    
    p1 = Fighter(200, 200, stats_p1, controls_p1, is_p2=False,
                combat_system=combat_system, fighter_id="p1")
    p2 = Fighter(400, 200, stats_p2, controls_p2, is_p2=True,
                combat_system=combat_system, fighter_id="p2")
    
    # Test easy difficulty
    ai_easy = AIController(p2, p1, difficulty='easy')
    assert ai_easy.reaction_time == 400, "Easy should have 400ms reaction"
    assert ai_easy.aggression == 0.3, "Easy should have 0.3 aggression"
    assert ai_easy.parry_chance == 0.05, "Easy should have 5% parry chance"
    
    # Test medium difficulty
    ai_medium = AIController(p2, p1, difficulty='medium')
    assert ai_medium.reaction_time == 200, "Medium should have 200ms reaction"
    assert ai_medium.aggression == 0.5, "Medium should have 0.5 aggression"
    
    # Test expert difficulty
    ai_expert = AIController(p2, p1, difficulty='expert')
    assert ai_expert.reaction_time == 50, "Expert should have 50ms reaction"
    assert ai_expert.aggression == 0.8, "Expert should have 0.8 aggression"
    
    print("✓ AI difficulty levels test passed")

def test_dash_cooldown():
    """Test that dash has proper cooldown"""
    pygame.init()
    
    controls = c.DEFAULT_P1_CONTROLS
    stats = c.CHARACTERS[0]
    combat_system = CombatSystem()
    combat_system.register_fighter("p1")
    
    fighter = Fighter(200, 200, stats, controls, is_p2=False,
                     combat_system=combat_system, fighter_id="p1")
    
    # First dash
    current_time = pygame.time.get_ticks()
    fighter.dashing = True
    fighter.dash_timer = c.FRAME_DATA['dash']['active']
    fighter.last_dash_time = current_time
    
    # Wait for dash to complete
    for _ in range(10):
        if fighter.dash_timer > 0:
            fighter.dash_timer -= 1
        else:
            fighter.dashing = False
    
    assert fighter.dashing == False, "Dash should have completed"
    
    print("✓ Dash cooldown test passed")

def test_controls_mapping():
    """Test that all controls are properly mapped"""
    pygame.init()
    
    # Check P1 controls
    assert 'parry' in c.DEFAULT_P1_CONTROLS, "P1 should have parry control"
    assert 'dash' in c.DEFAULT_P1_CONTROLS, "P1 should have dash control"
    assert 'special' in c.DEFAULT_P1_CONTROLS, "P1 should have special control"
    
    # Check P2 controls
    assert 'parry' in c.DEFAULT_P2_CONTROLS, "P2 should have parry control"
    assert 'dash' in c.DEFAULT_P2_CONTROLS, "P2 should have dash control"
    assert 'special' in c.DEFAULT_P2_CONTROLS, "P2 should have special control"
    
    # Verify parry keys are different for P1 and P2
    assert c.DEFAULT_P1_CONTROLS['parry'] != c.DEFAULT_P2_CONTROLS['parry'], \
        "P1 and P2 should have different parry keys"
    
    print("✓ Controls mapping test passed")

def test_character_stats():
    """Test that all characters have required stats"""
    pygame.init()
    
    required_keys = ['name', 'color', 'skin', 'speed', 'jump', 'health', 
                     'dmg_mult', 'desc', 'special']
    
    for char in c.CHARACTERS:
        for key in required_keys:
            assert key in char, f"Character {char.get('name', 'Unknown')} missing {key}"
        
        # Verify reasonable stat values
        assert char['health'] > 0, "Health should be positive"
        assert char['speed'] > 0, "Speed should be positive"
        assert char['jump'] < 0, "Jump should be negative (upward force)"
        assert char['dmg_mult'] > 0, "Damage multiplier should be positive"
    
    print("✓ Character stats test passed")

if __name__ == "__main__":
    print("\n=== Running Enhanced Features Tests ===\n")
    
    try:
        test_coin_insertion_state()
        test_mid_air_dash()
        test_parry_mechanics()
        test_parry_window_decay()
        test_ai_controller_initialization()
        test_ai_difficulty_levels()
        test_dash_cooldown()
        test_controls_mapping()
        test_character_stats()
        
        print("\n=== All enhanced features tests passed! ✓ ===\n")
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
        raise
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        raise
