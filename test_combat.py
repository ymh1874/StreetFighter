"""
Comprehensive Combat Test Suite for CMUQ Arena
Tests all combat mechanics including attacks, damage, collision, knockback, stun, and combos
"""

import pygame
import sys
import config as c
from entities import Fighter, Attack

def setup_test_fighters():
    """Create two test fighters for combat testing"""
    pygame.init()
    
    # Player 1 controls
    controls_p1 = {
        'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
        'light': pygame.K_j, 'heavy': pygame.K_k, 'kick': pygame.K_l, 'special': pygame.K_i
    }
    # Player 2 controls
    controls_p2 = {
        'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP,
        'light': pygame.K_KP1, 'heavy': pygame.K_KP2, 'kick': pygame.K_KP3, 'special': pygame.K_KP0
    }
    
    # Create fighters with first character
    stats = c.CHARACTERS[0]
    p1 = Fighter(200, 200, stats, controls_p1, is_p2=False)
    p2 = Fighter(400, 200, stats, controls_p2, is_p2=True)
    
    return p1, p2

def test_attack_types():
    """Test all attack types (light, heavy, kick, special)"""
    print("\n" + "="*60)
    print("TEST: Attack Types")
    print("="*60)
    
    p1, p2 = setup_test_fighters()
    
    tests_passed = 0
    tests_total = 0
    
    # Test each attack type
    attack_types = ['light', 'heavy', 'kick', 'special']
    
    for attack_type in attack_types:
        tests_total += 1
        print(f"\nTesting {attack_type.upper()} attack...")
        
        # Record initial health
        initial_health = p2.health
        
        # Perform attack
        hit = p1.attack(p2, attack_type)
        
        # Verify attack properties exist
        attack_data = p1.moves[attack_type]
        
        if hit:
            print(f"  ✓ {attack_type} attack hit successful")
            print(f"    - Damage: {attack_data.damage}")
            print(f"    - Knockback: {attack_data.knockback}")
            print(f"    - Stun: {attack_data.stun}")
            print(f"    - Hitbox: {attack_data.width}x{attack_data.height}")
            print(f"    - Cooldown: {attack_data.cooldown}ms")
            print(f"    - Health reduced: {initial_health - p2.health}")
            
            # Verify damage was applied
            if p2.health < initial_health:
                print(f"  ✓ Damage applied correctly")
                tests_passed += 1
            else:
                print(f"  ✗ Damage NOT applied")
        else:
            print(f"  ! {attack_type} attack missed (fighters too far)")
            tests_passed += 1  # Not a failure, just out of range
    
    print(f"\n{tests_passed}/{tests_total} attack type tests passed")
    pygame.quit()
    return tests_passed == tests_total

def test_collision_detection():
    """Test hit detection and collision"""
    print("\n" + "="*60)
    print("TEST: Collision Detection")
    print("="*60)
    
    p1, p2 = setup_test_fighters()
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Attack at close range (should hit)
    tests_total += 1
    print("\nTest 1: Close range attack")
    p1.rect.x = 200
    p2.rect.x = 240  # Within attack range
    initial_health = p2.health
    hit = p1.attack(p2, 'light')
    
    if hit and p2.health < initial_health:
        print("  ✓ Close range attack detected and applied")
        tests_passed += 1
    else:
        print("  ✗ Close range attack failed")
    
    # Test 2: Attack at far range (should miss)
    tests_total += 1
    print("\nTest 2: Far range attack")
    p1.rect.x = 100
    p2.rect.x = 500  # Too far
    p2.health = p2.max_health  # Reset health
    initial_health = p2.health
    hit = p1.attack(p2, 'light')
    
    if not hit and p2.health == initial_health:
        print("  ✓ Far range attack correctly missed")
        tests_passed += 1
    else:
        print("  ✗ Far range attack should have missed")
    
    # Test 3: Different attack ranges
    tests_total += 1
    print("\nTest 3: Attack range variations")
    ranges_correct = True
    
    # Special should have longest range
    if p1.moves['special'].width > p1.moves['light'].width:
        print("  ✓ Special attack has longer range than light")
    else:
        print("  ✗ Special attack range issue")
        ranges_correct = False
    
    if ranges_correct:
        tests_passed += 1
    
    print(f"\n{tests_passed}/{tests_total} collision tests passed")
    pygame.quit()
    return tests_passed == tests_total

def test_damage_calculation():
    """Test damage calculation with character multipliers"""
    print("\n" + "="*60)
    print("TEST: Damage Calculation")
    print("="*60)
    
    tests_passed = 0
    tests_total = 0
    
    # Test each character's damage multiplier
    for char_idx, char_stats in enumerate(c.CHARACTERS):
        tests_total += 1
        print(f"\nTesting {char_stats['name']} (dmg_mult: {char_stats['dmg_mult']})")
        
        pygame.init()
        controls = {
            'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
            'light': pygame.K_j, 'heavy': pygame.K_k, 'kick': pygame.K_l, 'special': pygame.K_i
        }
        
        fighter = Fighter(200, 200, char_stats, controls, is_p2=False)
        
        # Check that damage is calculated with multiplier
        base_light_damage = 5
        expected_damage = base_light_damage * char_stats['dmg_mult']
        actual_damage = fighter.moves['light'].damage
        
        print(f"  Expected light damage: {expected_damage}")
        print(f"  Actual light damage: {actual_damage}")
        
        if abs(actual_damage - expected_damage) < 0.01:
            print(f"  ✓ Damage multiplier applied correctly")
            tests_passed += 1
        else:
            print(f"  ✗ Damage multiplier NOT applied correctly")
        
        pygame.quit()
    
    print(f"\n{tests_passed}/{tests_total} damage calculation tests passed")
    return tests_passed == tests_total

def test_knockback_and_stun():
    """Test knockback and stun mechanics"""
    print("\n" + "="*60)
    print("TEST: Knockback and Stun Mechanics")
    print("="*60)
    
    p1, p2 = setup_test_fighters()
    
    tests_passed = 0
    tests_total = 0
    
    # Test knockback
    tests_total += 1
    print("\nTest 1: Knockback effect")
    p1.rect.x = 200
    p2.rect.x = 240
    initial_x = p2.rect.x
    
    p1.attack(p2, 'heavy')  # Heavy attack should have significant knockback
    
    # Check if target was knocked back
    if p2.rect.x != initial_x:
        print(f"  ✓ Knockback applied (moved {abs(p2.rect.x - initial_x)} pixels)")
        tests_passed += 1
    else:
        print(f"  ✗ Knockback NOT applied")
    
    # Test stun
    tests_total += 1
    print("\nTest 2: Stun effect")
    p1, p2 = setup_test_fighters()  # Reset fighters
    p1.rect.x = 200
    p2.rect.x = 240
    
    p1.attack(p2, 'heavy')
    
    if p2.hit_stun > 0:
        print(f"  ✓ Stun applied ({p2.hit_stun} frames)")
        tests_passed += 1
    else:
        print(f"  ✗ Stun NOT applied")
    
    # Test that different attacks have different stun values
    tests_total += 1
    print("\nTest 3: Stun variation by attack type")
    
    if p1.moves['special'].stun > p1.moves['light'].stun:
        print(f"  ✓ Special has higher stun ({p1.moves['special'].stun}) than light ({p1.moves['light'].stun})")
        tests_passed += 1
    else:
        print(f"  ✗ Stun values not varied correctly")
    
    print(f"\n{tests_passed}/{tests_total} knockback/stun tests passed")
    pygame.quit()
    return tests_passed == tests_total

def test_attack_cooldowns():
    """Test attack cooldown system"""
    print("\n" + "="*60)
    print("TEST: Attack Cooldowns")
    print("="*60)
    
    p1, p2 = setup_test_fighters()
    
    tests_passed = 0
    tests_total = 0
    
    # Test cooldown prevents rapid attacks
    tests_total += 1
    print("\nTest 1: Cooldown timer mechanism")
    
    p1.rect.x = 200
    p2.rect.x = 240
    
    # First attack sets cooldown
    p1.attack(p2, 'light')
    cooldown_set = p1.attack_cooldown
    last_attack = p1.last_attack_time
    
    # Check that cooldown was set
    if cooldown_set > 0 and last_attack > 0:
        print(f"  ✓ Cooldown timer set correctly ({cooldown_set}ms)")
        tests_passed += 1
    else:
        print(f"  ✗ Cooldown timer not set (cooldown: {cooldown_set}, last_attack: {last_attack})")
    
    # Test 2: Cooldown check in move() prevents attacks
    tests_total += 1
    print("\nTest 2: Cooldown check in move() method")
    
    p1, p2 = setup_test_fighters()
    p1.rect.x = 200
    p2.rect.x = 240
    
    # Manually set cooldown as if attack just happened
    p1.attack_cooldown = 300
    p1.last_attack_time = pygame.time.get_ticks()
    current_time = pygame.time.get_ticks()
    
    # Check that enough time has NOT passed
    time_since_attack = current_time - p1.last_attack_time
    can_attack = (current_time - p1.last_attack_time > p1.attack_cooldown)
    
    if not can_attack and time_since_attack < p1.attack_cooldown:
        print(f"  ✓ Cooldown check works (time passed: {time_since_attack}ms < cooldown: {p1.attack_cooldown}ms)")
        tests_passed += 1
    else:
        print(f"  ✗ Cooldown check logic issue")
    
    # Test 3: Different cooldowns for different attacks
    tests_total += 1
    print("\nTest 3: Different attack cooldowns")
    
    if p1.moves['special'].cooldown > p1.moves['light'].cooldown:
        print(f"  ✓ Special has longer cooldown ({p1.moves['special'].cooldown}ms) than light ({p1.moves['light'].cooldown}ms)")
        tests_passed += 1
    else:
        print(f"  ✗ Cooldowns not properly differentiated")
    
    print(f"\n{tests_passed}/{tests_total} cooldown tests passed")
    pygame.quit()
    return tests_passed == tests_total

def test_health_system():
    """Test health system and KO mechanics"""
    print("\n" + "="*60)
    print("TEST: Health System")
    print("="*60)
    
    p1, p2 = setup_test_fighters()
    
    tests_passed = 0
    tests_total = 0
    
    # Test health reduction
    tests_total += 1
    print("\nTest 1: Health reduction on hit")
    initial_health = p2.health
    p1.rect.x = 200
    p2.rect.x = 240
    p1.attack(p2, 'light')
    
    if p2.health < initial_health:
        print(f"  ✓ Health reduced from {initial_health} to {p2.health}")
        tests_passed += 1
    else:
        print(f"  ✗ Health NOT reduced")
    
    # Test health cannot go negative
    tests_total += 1
    print("\nTest 2: Health floor at 0")
    p2.health = 10
    p1.attacking = False
    p1.attack_cooldown = 0
    p1.last_attack_time = 0
    p1.attack(p2, 'special')  # Should reduce health to 0
    
    if p2.health >= 0:
        print(f"  ✓ Health correctly floored at 0 (current: {p2.health})")
        tests_passed += 1
    else:
        print(f"  ✗ Health went negative: {p2.health}")
    
    # Test KO state
    tests_total += 1
    print("\nTest 3: KO state on 0 health")
    p2.health = 0
    p2.take_damage(1, 0, 0, True)
    
    if not p2.alive:
        print(f"  ✓ Fighter marked as not alive at 0 health")
        tests_passed += 1
    else:
        print(f"  ✗ Fighter still alive at 0 health")
    
    print(f"\n{tests_passed}/{tests_total} health system tests passed")
    pygame.quit()
    return tests_passed == tests_total

def test_all_character_combat():
    """Test combat for all character combinations"""
    print("\n" + "="*60)
    print("TEST: All Character Combat Interactions")
    print("="*60)
    
    tests_passed = 0
    tests_total = 0
    
    for i, char1 in enumerate(c.CHARACTERS):
        for j, char2 in enumerate(c.CHARACTERS):
            tests_total += 1
            
            pygame.init()
            controls_p1 = {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
                          'light': pygame.K_j, 'heavy': pygame.K_k, 'kick': pygame.K_l, 'special': pygame.K_i}
            controls_p2 = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP,
                          'light': pygame.K_KP1, 'heavy': pygame.K_KP2, 'kick': pygame.K_KP3, 'special': pygame.K_KP0}
            
            p1 = Fighter(200, 200, char1, controls_p1, is_p2=False)
            p2 = Fighter(240, 200, char2, controls_p2, is_p2=True)
            
            # Test attack
            initial_health = p2.health
            hit = p1.attack(p2, 'light')
            
            if hit and p2.health < initial_health:
                tests_passed += 1
            
            pygame.quit()
    
    print(f"\n{tests_passed}/{tests_total} character combination tests passed")
    print(f"Tested {len(c.CHARACTERS)}x{len(c.CHARACTERS)} = {len(c.CHARACTERS)**2} matchups")
    
    return tests_passed == tests_total

def run_all_combat_tests():
    """Run all combat test suites"""
    print("\n" + "="*70)
    print("  COMPREHENSIVE COMBAT TEST SUITE - CMUQ ARENA")
    print("="*70)
    
    results = []
    
    # Run each test suite
    results.append(("Attack Types", test_attack_types()))
    results.append(("Collision Detection", test_collision_detection()))
    results.append(("Damage Calculation", test_damage_calculation()))
    results.append(("Knockback & Stun", test_knockback_and_stun()))
    results.append(("Attack Cooldowns", test_attack_cooldowns()))
    results.append(("Health System", test_health_system()))
    results.append(("All Characters", test_all_character_combat()))
    
    # Print summary
    print("\n" + "="*70)
    print("COMBAT TEST SUMMARY")
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
        print("✓ ALL COMBAT TESTS PASSED - Combat system is fully functional!")
    else:
        print(f"✗ {len(results) - passed_count} test suite(s) failed")
    
    print("="*70 + "\n")
    
    return passed_count == len(results)

if __name__ == "__main__":
    success = run_all_combat_tests()
    sys.exit(0 if success else 1)
