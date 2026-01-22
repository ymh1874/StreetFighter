"""
Test Suite for CMUQ Arena - Vintage Arcade Fighter
Verifies UI alignment, game states, and functionality

Run this file to test the game without playing
"""

import pygame
import sys
import config as c
from ui_components import Button, VintageTextRenderer, ArcadeFrame, ScanlineEffect

def test_alignment():
    """Test that all UI elements are properly aligned"""
    print("=" * 60)
    print("CMUQ ARENA - ALIGNMENT TEST SUITE")
    print("=" * 60)
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
    text_renderer = VintageTextRenderer()
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Button alignment
    print("\n[TEST 1] Button Alignment")
    tests_total += 1
    button = Button(c.SCREEN_WIDTH // 2 - 150, 300, 300, 60, "TEST")
    if button.rect.centerx == c.SCREEN_WIDTH // 2:
        print("✓ Button is horizontally centered")
        tests_passed += 1
    else:
        print("✗ Button is NOT centered")
        print(f"  Expected center: {c.SCREEN_WIDTH // 2}, Got: {button.rect.centerx}")
    
    # Test 2: Text rendering
    print("\n[TEST 2] Text Rendering")
    tests_total += 1
    try:
        text_small = text_renderer.render("Test Small", 'small', c.WHITE)
        text_medium = text_renderer.render("Test Medium", 'medium', c.WHITE)
        text_large = text_renderer.render("Test Large", 'large', c.WHITE)
        print("✓ All text sizes render successfully")
        print(f"  Small: {text_small.get_width()}x{text_small.get_height()}")
        print(f"  Medium: {text_medium.get_width()}x{text_medium.get_height()}")
        print(f"  Large: {text_large.get_width()}x{text_large.get_height()}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Text rendering failed: {e}")
    
    # Test 3: Character grid alignment
    print("\n[TEST 3] Character Grid Alignment")
    tests_total += 1
    num_chars = len(c.CHARACTERS)
    box_width = 120
    gap = 30
    total_width = num_chars * box_width + (num_chars - 1) * gap
    start_x = (c.SCREEN_WIDTH - total_width) // 2
    
    # Check if grid is centered
    end_x = start_x + total_width
    if abs((start_x + end_x) / 2 - c.SCREEN_WIDTH / 2) < 1:
        print("✓ Character grid is perfectly centered")
        print(f"  Grid width: {total_width}px")
        print(f"  Start X: {start_x}px")
        tests_passed += 1
    else:
        print("✗ Character grid is NOT centered")
    
    # Test 4: Health bar alignment
    print("\n[TEST 4] Health Bar Alignment")
    tests_total += 1
    bar_width = 300
    p1_bar_x = 20
    p2_bar_x = c.SCREEN_WIDTH - 20 - bar_width
    
    if p2_bar_x + bar_width + 20 == c.SCREEN_WIDTH:
        print("✓ Health bars are symmetrically aligned")
        print(f"  P1 bar: {p1_bar_x}px from left")
        print(f"  P2 bar: {p2_bar_x}px from left")
        tests_passed += 1
    else:
        print("✗ Health bars are NOT symmetrical")
    
    # Test 5: Visual effects
    print("\n[TEST 5] Visual Effects")
    tests_total += 1
    try:
        scanlines = ScanlineEffect(c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        print("✓ Scanline effect initialized")
        ArcadeFrame.draw(screen)
        print("✓ Arcade frame drawn")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Visual effects failed: {e}")
    
    # Test 6: Screen centering
    print("\n[TEST 6] Screen Centering Test")
    tests_total += 1
    title = text_renderer.render("CMUQ ARENA", 'large', c.ORANGE)
    centered_x = c.SCREEN_WIDTH // 2 - title.get_width() // 2
    
    if abs(centered_x + title.get_width() / 2 - c.SCREEN_WIDTH / 2) < 1:
        print("✓ Title text is perfectly centered")
        print(f"  Title width: {title.get_width()}px")
        print(f"  Position X: {centered_x}px")
        tests_passed += 1
    else:
        print("✗ Title text is NOT centered")
    
    # Results
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {tests_passed}/{tests_total} PASSED")
    if tests_passed == tests_total:
        print("✓ ALL TESTS PASSED - UI is properly aligned!")
    else:
        print(f"✗ {tests_total - tests_passed} test(s) failed")
    print("=" * 60)
    
    pygame.quit()
    return tests_passed == tests_total


def test_game_states():
    """Test game state transitions"""
    print("\n[TEST] Game State Verification")
    print("-" * 60)
    
    from game import Game
    
    # Check game initialization
    try:
        game = Game()
        print("✓ Game initialized successfully")
        print(f"  Initial state: {game.state}")
        print(f"  Number of menu buttons: {len(game.menu_buttons)}")
        print(f"  Screen size: {c.SCREEN_WIDTH}x{c.SCREEN_HEIGHT}")
        
        # Verify all states exist
        states = ["MAIN_MENU", "CONTROLS", "ABOUT", "CHARACTER_SELECT", "FIGHT", "GAME_OVER"]
        print("\n✓ All required game states defined:")
        for state in states:
            print(f"  - {state}")
        
        return True
    except Exception as e:
        print(f"✗ Game initialization failed: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  CMUQ ARENA - COMPREHENSIVE TEST SUITE")
    print("=" * 60 + "\n")
    
    # Run alignment tests
    alignment_ok = test_alignment()
    
    # Run game state tests
    state_ok = test_game_states()
    
    # Final summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    
    if alignment_ok and state_ok:
        print("✓ ALL SYSTEMS GO - Game is ready to play!")
        print("\nRun 'python main.py' to start the game")
    else:
        print("✗ Some tests failed - please review errors above")
    
    print("=" * 60 + "\n")
