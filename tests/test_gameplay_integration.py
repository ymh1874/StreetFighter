"""
Comprehensive integration test simulating real gameplay scenarios
Tests all characters, all combos, special moves, and edge cases
"""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'

import pygame
pygame.init()

from entities import Fighter
from combat import CombatSystem
import config as c

def create_fighter(char_index, player_num, combat_system, fighter_id):
    controls = {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
                'light_punch': pygame.K_j, 'heavy_punch': pygame.K_k,
                'light_kick': pygame.K_l, 'heavy_kick': pygame.K_i, 'special': pygame.K_u}
    return Fighter(100 if player_num == 1 else 700, 400, c.CHARACTERS[char_index], controls, 
                   is_p2=(player_num==2), combat_system=combat_system, fighter_id=fighter_id)

print("=" * 80)
print("COMPREHENSIVE GAMEPLAY INTEGRATION TEST")
print("=" * 80)

# Test 1: All characters can perform all attacks
print("\n=== TEST 1: All Characters Can Perform All Attacks ===")
combat_system = CombatSystem()
combat_system.register_fighter("p1")
combat_system.register_fighter("p2")

char_names = ['PROF. KHALID', 'PROF. EDUARDO', 'PROF. HASAN', 'PROF. HAMMOUD']
attack_types = ['light_punch', 'heavy_punch', 'light_kick', 'heavy_kick', 'special']

test1_passed = True
for i, char_name in enumerate(char_names):
    fighter = create_fighter(i, 1, combat_system, "p1")
    target = create_fighter((i + 1) % 4, 2, combat_system, "p2")
    target.rect.x = fighter.rect.right + 10
    
    for attack_type in attack_types:
        fighter.attacking = False
        fighter.last_attack_time = 0
        fighter.last_special_time = -2000
        
        # Wait a bit for cooldowns
        pygame.time.wait(50)
        
        result = fighter.attack(target, attack_type)
        
        if attack_type == 'special':
            # Special moves return special effects or projectiles
            if result is None:
                print(f"  ❌ {char_name} - {attack_type} FAILED (returned None)")
                test1_passed = False
            else:
                print(f"  ✓ {char_name} - {attack_type}")
        else:
            # Regular attacks return True/False
            if fighter.attack_rect is None:
                print(f"  ❌ {char_name} - {attack_type} FAILED (no attack_rect)")
                test1_passed = False
            else:
                print(f"  ✓ {char_name} - {attack_type}")

print(f"\nTest 1 Result: {'✅ PASSED' if test1_passed else '❌ FAILED'}")

# Test 2: Combo damage scaling works correctly
print("\n=== TEST 2: Combo Damage Scaling ===")
combat_system2 = CombatSystem()
combat_system2.register_fighter("p1")
combat_system2.register_fighter("p2")

attacker = create_fighter(0, 1, combat_system2, "p1")
target = create_fighter(1, 2, combat_system2, "p2")
target.rect.x = attacker.rect.right + 10

expected_damages = [
    (5.0, 1.0),   # Hit 1 - light punch, full damage
    (8.0, 1.0),   # Hit 2 - light kick, full damage
    (12.0, 1.0),  # Hit 3 - heavy punch, full damage
    (5.0, 0.8),   # Hit 4 - light punch, 80% damage
    (15.0, 0.8),  # Hit 5 - heavy kick, 80% damage
]

test2_passed = True
for i, (base_damage, expected_scaling) in enumerate(expected_damages, 1):
    pygame.time.wait(50)
    attacker.attacking = False
    attacker.last_attack_time = 0
    target.rect.x = attacker.rect.right + 10
    
    initial_health = target.health
    
    if i in [1, 4]:
        attacker.attack(target, 'light_punch')
    elif i == 2:
        attacker.attack(target, 'light_kick')
    elif i == 3:
        attacker.attack(target, 'heavy_punch')
    elif i == 5:
        attacker.attack(target, 'heavy_kick')
    
    actual_damage = initial_health - target.health
    expected_damage = base_damage * expected_scaling
    
    if abs(actual_damage - expected_damage) < 0.01:
        print(f"  ✓ Hit {i}: Expected {expected_damage:.1f} damage, got {actual_damage:.1f}")
    else:
        print(f"  ❌ Hit {i}: Expected {expected_damage:.1f} damage, got {actual_damage:.1f}")
        test2_passed = False

print(f"\nTest 2 Result: {'✅ PASSED' if test2_passed else '❌ FAILED'}")

# Test 3: Special moves work immediately at game start
print("\n=== TEST 3: Special Moves Work Immediately ===")
test3_passed = True

for i, char_name in enumerate(char_names):
    combat_system3 = CombatSystem()
    combat_system3.register_fighter("p1")
    
    fighter = create_fighter(i, 1, combat_system3, "p1")
    target = create_fighter(0, 2, combat_system3, "p2")
    
    # Try special move immediately (should work with last_special_time = -2000)
    fighter.attacking = False
    fighter.last_attack_time = 0
    # Don't modify last_special_time - it should be -2000 by default
    
    result = fighter.attack(target, 'special')
    
    if result is not None:
        print(f"  ✓ {char_name} special works immediately")
    else:
        print(f"  ❌ {char_name} special FAILED")
        test3_passed = False

print(f"\nTest 3 Result: {'✅ PASSED' if test3_passed else '❌ FAILED'}")

# Test 4: Combo resets when defender gets hit
print("\n=== TEST 4: Combo Reset on Hit ===")
combat_system4 = CombatSystem()
combat_system4.register_fighter("p1")
combat_system4.register_fighter("p2")

p1 = create_fighter(0, 1, combat_system4, "p1")
p2 = create_fighter(1, 2, combat_system4, "p2")

# P1 builds a combo
p2.rect.x = p1.rect.right + 10
for _ in range(3):
    pygame.time.wait(50)
    p1.attacking = False
    p1.last_attack_time = 0
    p2.rect.x = p1.rect.right + 10
    p1.attack(p2, 'light_punch')

p1_combo_before = combat_system4.get_combo_count("p1")

# P2 hits P1 (should reset P1's combo)
p1.rect.x = p2.rect.left - 60
p2.attacking = False
p2.last_attack_time = 0
p2.attack(p1, 'light_punch')

p1_combo_after = combat_system4.get_combo_count("p1")

if p1_combo_before > 0 and p1_combo_after == 0:
    print(f"  ✓ P1 combo reset correctly (was {p1_combo_before}, now {p1_combo_after})")
    test4_passed = True
else:
    print(f"  ❌ P1 combo did not reset (was {p1_combo_before}, now {p1_combo_after})")
    test4_passed = False

print(f"\nTest 4 Result: {'✅ PASSED' if test4_passed else '❌ FAILED'}")

# Test 5: All character matchups work
print("\n=== TEST 5: All Character Matchups ===")
test5_passed = True
matchup_count = 0

for i in range(4):
    for j in range(4):
        combat_system5 = CombatSystem()
        combat_system5.register_fighter("p1")
        combat_system5.register_fighter("p2")
        
        p1 = create_fighter(i, 1, combat_system5, "p1")
        p2 = create_fighter(j, 2, combat_system5, "p2")
        
        p2.rect.x = p1.rect.right + 10
        
        p1.attacking = False
        p1.last_attack_time = 0
        
        initial_health = p2.health
        result = p1.attack(p2, 'light_punch')
        
        if result and p2.health < initial_health:
            matchup_count += 1
        else:
            print(f"  ❌ {char_names[i]} vs {char_names[j]} FAILED")
            test5_passed = False

if test5_passed:
    print(f"  ✓ All 16 character matchups work correctly")

print(f"\nTest 5 Result: {'✅ PASSED' if test5_passed else '❌ FAILED'}")

# Final Summary
print("\n" + "=" * 80)
print("FINAL SUMMARY")
print("=" * 80)
all_passed = test1_passed and test2_passed and test3_passed and test4_passed and test5_passed
print(f"Test 1 (All Attacks): {'✅ PASSED' if test1_passed else '❌ FAILED'}")
print(f"Test 2 (Combo Scaling): {'✅ PASSED' if test2_passed else '❌ FAILED'}")
print(f"Test 3 (Immediate Specials): {'✅ PASSED' if test3_passed else '❌ FAILED'}")
print(f"Test 4 (Combo Reset): {'✅ PASSED' if test4_passed else '❌ FAILED'}")
print(f"Test 5 (All Matchups): {'✅ PASSED' if test5_passed else '❌ FAILED'}")
print()
if all_passed:
    print("🎮 ✅ ALL TESTS PASSED - GAME MECHANICS ARE WORKING PERFECTLY!")
else:
    print("⚠️ SOME TESTS FAILED - SEE DETAILS ABOVE")
print("=" * 80)
