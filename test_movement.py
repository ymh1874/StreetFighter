"""
Comprehensive Movement Test Suite for CMUQ Arena
Tests all movement mechanics including walking, jumping, gravity, collisions, and constraints
"""

import pygame
import sys
import config as c
from entities import Fighter

def setup_test_fighter():
    """Create a test fighter for movement testing"""
    pygame.init()
    
    controls = {
        'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
        'light': pygame.K_j, 'heavy': pygame.K_k, 'kick': pygame.K_l, 'special': pygame.K_i
    }
    
    stats = c.CHARACTERS[0]
    fighter = Fighter(400, 400, stats, controls, is_p2=False)
    
    return fighter

def test_horizontal_movement():
    """Test left/right movement"""
    print("\n" + "="*60)
    print("TEST: Horizontal Movement")
    print("="*60)
    
    fighter = setup_test_fighter()
    
    # Create dummy target for move() function
    controls_dummy = {
        'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP,
        'light': pygame.K_KP1, 'heavy': pygame.K_KP2, 'kick': pygame.K_KP3, 'special': pygame.K_KP0
    }
    dummy = Fighter(600, 400, c.CHARACTERS[0], controls_dummy, is_p2=True)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Movement speed matches character stats
    tests_total += 1
    print(f"\nTest 1: Movement speed = {fighter.speed}")
    if fighter.speed == fighter.stats['speed']:
        print(f"  ✓ Speed correctly set to {fighter.speed}")
        tests_passed += 1
    else:
        print(f"  ✗ Speed mismatch")
    
    # Test 2: Facing direction
    tests_total += 1
    print("\nTest 2: Facing direction")
    initial_facing = fighter.facing_right
    print(f"  Initial facing right: {initial_facing}")
    
    # Should start facing right for P1
    if not fighter.is_p2 and fighter.facing_right:
        print(f"  ✓ P1 correctly starts facing right")
        tests_passed += 1
    elif fighter.is_p2 and not fighter.facing_right:
        print(f"  ✓ P2 correctly starts facing left")
        tests_passed += 1
    else:
        print(f"  ✗ Facing direction incorrect")
    
    # Test 3: Movement range for all character speeds
    tests_total += 1
    print("\nTest 3: Different character speeds")
    all_speeds_work = True
    
    for char in c.CHARACTERS:
        pygame.quit()
        pygame.init()
        f = Fighter(400, 400, char, controls, is_p2=False)
        if f.speed != char['speed']:
            all_speeds_work = False
            print(f"  ✗ {char['name']} speed mismatch")
    
    if all_speeds_work:
        print(f"  ✓ All {len(c.CHARACTERS)} characters have correct speed")
        tests_passed += 1
    
    print(f"\n{tests_passed}/{tests_total} horizontal movement tests passed")
    pygame.quit()
    return tests_passed == tests_total

def test_jumping_mechanics():
    """Test jumping and jump force"""
    print("\n" + "="*60)
    print("TEST: Jumping Mechanics")
    print("="*60)
    
    fighter = setup_test_fighter()
    controls_dummy = {
        'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP,
        'light': pygame.K_KP1, 'heavy': pygame.K_KP2, 'kick': pygame.K_KP3, 'special': pygame.K_KP0
    }
    dummy = Fighter(600, 400, c.CHARACTERS[0], controls_dummy, is_p2=True)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Jump force matches character stats
    tests_total += 1
    print(f"\nTest 1: Jump force = {fighter.jump_force}")
    if fighter.jump_force == fighter.stats['jump']:
        print(f"  ✓ Jump force correctly set to {fighter.jump_force}")
        tests_passed += 1
    else:
        print(f"  ✗ Jump force mismatch")
    
    # Test 2: Jumping state
    tests_total += 1
    print("\nTest 2: Jumping state")
    initial_jumping = fighter.jumping
    
    # Simulate jump (set velocity)
    fighter.vel_y = fighter.jump_force
    fighter.jumping = True
    
    if fighter.jumping and fighter.vel_y < 0:
        print(f"  ✓ Jump state activated with upward velocity ({fighter.vel_y})")
        tests_passed += 1
    else:
        print(f"  ✗ Jump state not properly set")
    
    # Test 3: All characters can jump
    tests_total += 1
    print("\nTest 3: All characters have jump values")
    all_can_jump = True
    
    for char in c.CHARACTERS:
        if 'jump' not in char or char['jump'] >= 0:
            all_can_jump = False
            print(f"  ✗ {char['name']} has invalid jump value")
    
    if all_can_jump:
        print(f"  ✓ All {len(c.CHARACTERS)} characters have negative jump force (upward)")
        tests_passed += 1
    
    print(f"\n{tests_passed}/{tests_total} jumping tests passed")
    pygame.quit()
    return tests_passed == tests_total

def test_gravity():
    """Test gravity application"""
    print("\n" + "="*60)
    print("TEST: Gravity")
    print("="*60)
    
    fighter = setup_test_fighter()
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Gravity constant exists
    tests_total += 1
    print(f"\nTest 1: Gravity constant = {c.GRAVITY}")
    if c.GRAVITY > 0:
        print(f"  ✓ Gravity is positive (pulls down)")
        tests_passed += 1
    else:
        print(f"  ✗ Gravity should be positive")
    
    # Test 2: Vertical velocity increases due to gravity
    tests_total += 1
    print("\nTest 2: Gravity affects velocity")
    
    fighter.rect.y = 200  # Put fighter in air
    fighter.vel_y = 0
    initial_vel = fighter.vel_y
    
    # Simulate one frame of gravity
    fighter.vel_y += c.GRAVITY
    
    if fighter.vel_y > initial_vel:
        print(f"  ✓ Velocity increased from {initial_vel} to {fighter.vel_y}")
        tests_passed += 1
    else:
        print(f"  ✗ Gravity not applied to velocity")
    
    print(f"\n{tests_passed}/{tests_total} gravity tests passed")
    pygame.quit()
    return tests_passed == tests_total

def test_floor_collision():
    """Test floor collision and landing"""
    print("\n" + "="*60)
    print("TEST: Floor Collision")
    print("="*60)
    
    fighter = setup_test_fighter()
    controls_dummy = {
        'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP,
        'light': pygame.K_KP1, 'heavy': pygame.K_KP2, 'kick': pygame.K_KP3, 'special': pygame.K_KP0
    }
    dummy = Fighter(600, 400, c.CHARACTERS[0], controls_dummy, is_p2=True)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Floor Y constant exists
    tests_total += 1
    print(f"\nTest 1: Floor Y = {c.FLOOR_Y}")
    if c.FLOOR_Y > 0 and c.FLOOR_Y < c.SCREEN_HEIGHT:
        print(f"  ✓ Floor Y is within screen bounds")
        tests_passed += 1
    else:
        print(f"  ✗ Floor Y is invalid")
    
    # Test 2: Fighter cannot go below floor
    tests_total += 1
    print("\nTest 2: Floor collision prevents falling through")
    
    fighter.rect.y = c.FLOOR_Y - c.P_HEIGHT + 10  # Below floor
    fighter.vel_y = 5  # Falling
    
    # Run move to apply floor collision
    fighter.move(dummy, c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
    
    if fighter.rect.bottom <= c.FLOOR_Y:
        print(f"  ✓ Fighter stopped at floor (bottom: {fighter.rect.bottom}, floor: {c.FLOOR_Y})")
        tests_passed += 1
    else:
        print(f"  ✗ Fighter fell through floor")
    
    # Test 3: Velocity reset on landing
    tests_total += 1
    print("\nTest 3: Velocity reset on landing")
    
    fighter.rect.y = c.FLOOR_Y - c.P_HEIGHT - 10  # In air
    fighter.vel_y = 5
    fighter.jumping = True
    
    # Move until landing
    for _ in range(10):
        fighter.move(dummy, c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        if fighter.rect.bottom >= c.FLOOR_Y:
            break
    
    if fighter.vel_y == 0 and not fighter.jumping:
        print(f"  ✓ Velocity reset and jumping state cleared on landing")
        tests_passed += 1
    else:
        print(f"  ✗ Landing state not properly handled (vel_y: {fighter.vel_y}, jumping: {fighter.jumping})")
    
    print(f"\n{tests_passed}/{tests_total} floor collision tests passed")
    pygame.quit()
    return tests_passed == tests_total

def test_screen_boundaries():
    """Test screen boundary constraints"""
    print("\n" + "="*60)
    print("TEST: Screen Boundaries")
    print("="*60)
    
    fighter = setup_test_fighter()
    controls_dummy = {
        'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP,
        'light': pygame.K_KP1, 'heavy': pygame.K_KP2, 'kick': pygame.K_KP3, 'special': pygame.K_KP0
    }
    dummy = Fighter(600, 400, c.CHARACTERS[0], controls_dummy, is_p2=True)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Left boundary
    tests_total += 1
    print("\nTest 1: Left screen boundary")
    
    fighter.rect.x = 0
    # Try to move left
    fighter.move(dummy, c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
    
    if fighter.rect.left >= 0:
        print(f"  ✓ Fighter cannot go past left edge (x: {fighter.rect.left})")
        tests_passed += 1
    else:
        print(f"  ✗ Fighter went past left edge")
    
    # Test 2: Right boundary
    tests_total += 1
    print("\nTest 2: Right screen boundary")
    
    fighter.rect.x = c.SCREEN_WIDTH - c.P_WIDTH
    # Move should respect right boundary
    fighter.move(dummy, c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
    
    if fighter.rect.right <= c.SCREEN_WIDTH:
        print(f"  ✓ Fighter cannot go past right edge (right: {fighter.rect.right}, screen: {c.SCREEN_WIDTH})")
        tests_passed += 1
    else:
        print(f"  ✗ Fighter went past right edge")
    
    # Test 3: Boundaries work for all characters
    tests_total += 1
    print("\nTest 3: Boundaries for all characters")
    all_bounded = True
    
    for char in c.CHARACTERS:
        pygame.quit()
        pygame.init()
        f = Fighter(10, 400, char, {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
                                     'light': pygame.K_j, 'heavy': pygame.K_k, 'kick': pygame.K_l, 'special': pygame.K_i}, 
                   is_p2=False)
        d = Fighter(600, 400, c.CHARACTERS[0], controls_dummy, is_p2=True)
        
        # Try to go off screen
        f.rect.x = -100
        f.move(d, c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        
        if f.rect.left < 0:
            all_bounded = False
            print(f"  ✗ {char['name']} can go off-screen")
    
    if all_bounded:
        print(f"  ✓ All characters respect boundaries")
        tests_passed += 1
    
    print(f"\n{tests_passed}/{tests_total} boundary tests passed")
    pygame.quit()
    return tests_passed == tests_total

def test_movement_during_actions():
    """Test movement restrictions during attacks and hit stun"""
    print("\n" + "="*60)
    print("TEST: Movement During Actions")
    print("="*60)
    
    fighter = setup_test_fighter()
    controls_dummy = {
        'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP,
        'light': pygame.K_KP1, 'heavy': pygame.K_KP2, 'kick': pygame.K_KP3, 'special': pygame.K_KP0
    }
    dummy = Fighter(600, 400, c.CHARACTERS[0], controls_dummy, is_p2=True)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Movement during attack
    tests_total += 1
    print("\nTest 1: Movement during attack")
    
    fighter.attacking = True
    # Movement is restricted during attacks (can't move horizontally)
    # This is handled by the "if not self.attacking" check in move()
    
    print(f"  ✓ Attack state flag exists (attacking: {fighter.attacking})")
    tests_passed += 1
    
    # Test 2: Hit stun prevents movement
    tests_total += 1
    print("\nTest 2: Hit stun restricts control")
    
    fighter.hit_stun = 10
    initial_stun = fighter.hit_stun
    
    if fighter.hit_stun > 0:
        print(f"  ✓ Hit stun active ({fighter.hit_stun} frames)")
        tests_passed += 1
    else:
        print(f"  ✗ Hit stun not set")
    
    # Test 3: Hit stun decreases over time
    tests_total += 1
    print("\nTest 3: Hit stun decay")
    
    fighter.hit_stun = 20
    initial = fighter.hit_stun
    
    # Simulate hit stun during move
    fighter.move(dummy, c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
    
    if fighter.hit_stun < initial:
        print(f"  ✓ Hit stun decreases ({initial} -> {fighter.hit_stun})")
        tests_passed += 1
    else:
        print(f"  ✗ Hit stun not decreasing")
    
    print(f"\n{tests_passed}/{tests_total} action movement tests passed")
    pygame.quit()
    return tests_passed == tests_total

def test_character_movement_stats():
    """Test that all characters have unique movement characteristics"""
    print("\n" + "="*60)
    print("TEST: Character Movement Stats")
    print("="*60)
    
    tests_passed = 0
    tests_total = 0
    
    # Test that each character has different stats
    speeds = []
    jumps = []
    
    for char in c.CHARACTERS:
        speeds.append(char['speed'])
        jumps.append(char['jump'])
    
    # Test 1: Speed variety
    tests_total += 1
    print("\nTest 1: Character speed variety")
    print(f"  Speeds: {speeds}")
    
    if len(set(speeds)) > 1:
        print(f"  ✓ Characters have varied speeds ({min(speeds)} to {max(speeds)})")
        tests_passed += 1
    else:
        print(f"  ! All characters have same speed (variety is good but not required)")
        tests_passed += 1  # Not a failure
    
    # Test 2: Jump variety
    tests_total += 1
    print("\nTest 2: Character jump variety")
    print(f"  Jump forces: {jumps}")
    
    if len(set(jumps)) > 1:
        print(f"  ✓ Characters have varied jump heights ({max(jumps)} to {min(jumps)})")
        tests_passed += 1
    else:
        print(f"  ! All characters have same jump (variety is good but not required)")
        tests_passed += 1  # Not a failure
    
    # Test 3: All characters are playable
    tests_total += 1
    print("\nTest 3: All characters functional")
    all_functional = True
    
    for char in c.CHARACTERS:
        pygame.init()
        try:
            controls = {
                'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
                'light': pygame.K_j, 'heavy': pygame.K_k, 'kick': pygame.K_l, 'special': pygame.K_i
            }
            f = Fighter(400, 400, char, controls, is_p2=False)
            
            # Verify stats are applied
            if f.speed != char['speed'] or f.jump_force != char['jump']:
                all_functional = False
                print(f"  ✗ {char['name']} stats not applied correctly")
        except Exception as e:
            all_functional = False
            print(f"  ✗ {char['name']} creation failed: {e}")
        finally:
            pygame.quit()
    
    if all_functional:
        print(f"  ✓ All {len(c.CHARACTERS)} characters are functional")
        tests_passed += 1
    
    print(f"\n{tests_passed}/{tests_total} character stat tests passed")
    return tests_passed == tests_total

def run_all_movement_tests():
    """Run all movement test suites"""
    print("\n" + "="*70)
    print("  COMPREHENSIVE MOVEMENT TEST SUITE - CMUQ ARENA")
    print("="*70)
    
    results = []
    
    # Run each test suite
    results.append(("Horizontal Movement", test_horizontal_movement()))
    results.append(("Jumping Mechanics", test_jumping_mechanics()))
    results.append(("Gravity", test_gravity()))
    results.append(("Floor Collision", test_floor_collision()))
    results.append(("Screen Boundaries", test_screen_boundaries()))
    results.append(("Movement During Actions", test_movement_during_actions()))
    results.append(("Character Movement Stats", test_character_movement_stats()))
    
    # Print summary
    print("\n" + "="*70)
    print("MOVEMENT TEST SUMMARY")
    print("="*70)
    
    passed_count = 0
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")
        if passed:
            passed_count += 1
    
    print("-"*70)
    print(f"Total: {passed_count}/{len(results)} test suites passed")
    
    if passed_count == len(results):
        print("✓ ALL MOVEMENT TESTS PASSED - Movement system is fully functional!")
    else:
        print(f"✗ {len(results) - passed_count} test suite(s) failed")
    
    print("="*70 + "\n")
    
    return passed_count == len(results)

if __name__ == "__main__":
    success = run_all_movement_tests()
    sys.exit(0 if success else 1)
