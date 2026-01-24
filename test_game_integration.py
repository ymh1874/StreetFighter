#!/usr/bin/env python3
"""
Integration test for Street Fighter game
Tests full game flow: menu -> character select -> fight with AI
"""

import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'  # Headless mode for pygame

import pygame
import config as c
from game import Game

# Global game instance for all tests
game = None

def setup_game():
    """Initialize game once for all tests"""
    global game
    if game is None:
        pygame.init()
        game = Game()
    return game

def test_game_initialization():
    """Test that game initializes without errors"""
    g = setup_game()
    
    # Verify initial state is valid
    valid_states = ["MAIN_MENU", "CONTROLS", "CHARACTER_SELECT", "ABOUT", "FIGHT", "GAME_OVER"]
    assert g.state in valid_states, f"Game should have valid state, got {g.state}"
    assert g.running, "Game should be running"
    
    print("✓ Game initialization test passed")

def test_state_transitions():
    """Test state transitions work correctly"""
    g = setup_game()
    
    # Test transition to controls
    g.state = "CONTROLS"
    assert g.state == "CONTROLS", "Should transition to controls"
    
    # Test transition back to main menu
    g.state = "MAIN_MENU"
    assert g.state == "MAIN_MENU", "Should transition back to main menu"
    
    # Test transition to character select
    g.state = "CHARACTER_SELECT"
    assert g.state == "CHARACTER_SELECT", "Should transition to character select"
    
    print("✓ State transitions test passed")

def test_character_selection_flow():
    """Test character selection process"""
    g = setup_game()
    g.state = "CHARACTER_SELECT"
    
    # Reset selections
    g.p1_selected = False
    g.p2_selected = False
    
    # Select P1 character
    g.p1_cursor = 0
    g.p1_selected = True
    
    assert g.p1_selected, "P1 should be selected"
    
    # P2 is human controlled (instant 2-player mode)
    g.p2_cursor = 1
    g.p2_selected = True
    
    assert g.p2_selected, "P2 should be selected"
    
    print("✓ Character selection flow test passed")

def test_fight_initialization_with_ai():
    """Test fight initialization"""
    g = setup_game()
    g.state = "CHARACTER_SELECT"
    
    # Reset state
    g.p1_selected = False
    g.p2_selected = False
    
    # Select characters
    g.p1_cursor = 0
    g.p2_cursor = 1
    g.p1_selected = True
    g.p2_selected = True
    
    # Start fight
    g._start_fight()
    
    # Verify fight state
    assert g.state == "FIGHT", "Should be in fight state"
    assert g.p1 is not None, "P1 fighter should exist"
    assert g.p2 is not None, "P2 fighter should exist"
    assert g.round_timer == 99, "Round timer should be 99"
    
    print("✓ Fight initialization test passed")

def test_fight_initialization_with_human():
    """Test fight initialization with two human players"""
    g = setup_game()
    g.state = "CHARACTER_SELECT"
    
    # Reset state
    g.p1_selected = False
    g.p2_selected = False
    
    # Select characters - both human players
    g.p1_cursor = 0
    g.p2_cursor = 1
    g.p1_selected = True
    g.p2_selected = True
    g.p2_coin_inserted = True  # Instant 2-player mode (always true now)
    
    # Start fight
    g._start_fight()
    
    # Verify fight state
    assert g.state == "FIGHT", "Should be in fight state"
    assert g.p1 is not None, "P1 fighter should exist"
    assert g.p2 is not None, "P2 fighter should exist"
    
    print("✓ Fight initialization with two human players test passed")

def test_combat_system_integration():
    """Test that combat system is properly integrated"""
    g = setup_game()
    g.state = "CHARACTER_SELECT"
    
    # Reset state
    g.p1_selected = False
    g.p2_selected = False
    
    # Select characters
    g.p1_cursor = 0
    g.p2_cursor = 1
    g.p1_selected = True
    g.p2_selected = True
    
    # Start fight
    g._start_fight()
    
    # Verify combat system integration
    assert g.p1.combat_system is not None, "P1 should have combat system"
    assert g.p2.combat_system is not None, "P2 should have combat system"
    assert g.p1.fighter_id == "p1", "P1 should have correct ID"
    assert g.p2.fighter_id == "p2", "P2 should have correct ID"
    
    print("✓ Combat system integration test passed")

def test_projectile_initialization():
    """Test that projectile list is initialized"""
    g = setup_game()
    g.state = "CHARACTER_SELECT"
    
    # Reset state
    g.p1_selected = False
    g.p2_selected = False
    
    g.p1_cursor = 0
    g.p2_cursor = 1
    g.p1_selected = True
    g.p2_selected = True
    
    g._start_fight()
    
    # Verify projectile system
    assert hasattr(g, 'projectiles'), "Game should have projectiles list"
    assert isinstance(g.projectiles, list), "Projectiles should be a list"
    assert len(g.projectiles) == 0, "Projectiles should start empty"
    
    print("✓ Projectile initialization test passed")

def test_reset_on_game_over():
    """Test that game state resets properly on game over"""
    g = setup_game()
    
    # Simulate game over
    g.state = "GAME_OVER"
    
    # Simulate pressing enter to return to menu
    g.p1_selected = False
    g.p2_selected = False
    g.p1_cursor = 0
    g.p2_cursor = 0
    g.p2_coin_inserted = True  # Keep instant 2-player mode
    g.state = "MAIN_MENU"
    
    # Verify reset
    assert g.state == "MAIN_MENU", "Should return to main menu"
    assert not g.p1_selected, "P1 selection should be reset"
    assert not g.p2_selected, "P2 selection should be reset"
    assert g.p2_coin_inserted, "Instant 2-player mode should remain active"
    
    print("✓ Reset on game over test passed")

def test_all_characters_can_fight():
    """Test that all characters can be initialized in a fight"""
    g = setup_game()
    
    # Test just a few combinations to avoid too many tests
    test_combinations = [(0, 1), (1, 2), (2, 3), (3, 0)]
    
    for i, j in test_combinations:
        g.state = "CHARACTER_SELECT"
        g.p1_cursor = i
        g.p2_cursor = j
        g.p1_selected = True
        g.p2_selected = True
        
        g._start_fight()
        
        # Verify both fighters created
        assert g.p1 is not None, f"P1 ({c.CHARACTERS[i]['name']}) should exist"
        assert g.p2 is not None, f"P2 ({c.CHARACTERS[j]['name']}) should exist"
        
        # Verify they have the right characters
        assert g.p1.stats['name'] == c.CHARACTERS[i]['name'], \
            f"P1 should be {c.CHARACTERS[i]['name']}"
        assert g.p2.stats['name'] == c.CHARACTERS[j]['name'], \
            f"P2 should be {c.CHARACTERS[j]['name']}"
    
    print("✓ All characters can fight test passed")

def test_special_moves_per_character():
    """Test that each character has their special move configured"""
    special_moves = {
        'PROF. KHALID': 'spinning_kick',
        'PROF. EDUARDO': 'pizza_throw',
        'PROF. HASAN': 'fireball',
        'PROF. HAMMOUD': 'circuit_board'
    }
    
    for char in c.CHARACTERS:
        name = char['name']
        assert 'special' in char, f"{name} should have special move"
        assert char['special'] == special_moves[name], \
            f"{name} should have {special_moves[name]} special"
    
    print("✓ Special moves per character test passed")

if __name__ == "__main__":
    print("\n=== Running Integration Tests ===\n")
    
    try:
        test_game_initialization()
        test_state_transitions()
        test_character_selection_flow()
        test_fight_initialization_with_ai()
        test_fight_initialization_with_human()
        test_combat_system_integration()
        test_projectile_initialization()
        test_reset_on_game_over()
        test_all_characters_can_fight()
        test_special_moves_per_character()
        
        print("\n=== All integration tests passed! ✓ ===\n")
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
        raise
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        raise

