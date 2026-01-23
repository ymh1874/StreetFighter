"""
Comprehensive Test Suite for CMUQ Arena
Tests every character, move, combo, projectile, and game mechanic
"""

import pygame
import sys
import config as c
from entities import Fighter, Particle, PizzaSlice, Fireball, CircuitBoard, StickFigure, Attack

pygame.init()

print("=" * 80)
print("CMUQ ARENA - COMPREHENSIVE TEST SUITE")
print("=" * 80)

test_results = {
    'passed': 0,
    'failed': 0,
    'errors': []
}

def test(name, condition, error_msg=""):
    """Helper function to run a test"""
    global test_results
    if condition:
        print(f"✓ {name}")
        test_results['passed'] += 1
        return True
    else:
        print(f"✗ {name}")
        if error_msg:
            print(f"  ERROR: {error_msg}")
            test_results['errors'].append(f"{name}: {error_msg}")
        test_results['failed'] += 1
        return False

# ============================================================================
# TEST 1: Configuration
# ============================================================================
print("\n" + "=" * 80)
print("TEST 1: CONFIGURATION")
print("=" * 80)

test("Config has 4 characters", len(c.CHARACTERS) == 4)
test("Screen width is 800", c.SCREEN_WIDTH == 800)
test("Screen height is 600", c.SCREEN_HEIGHT == 600)
test("FPS is 60", c.FPS == 60)
test("Gravity constant exists", hasattr(c, 'GRAVITY'))
test("Floor Y position exists", hasattr(c, 'FLOOR_Y'))

# ============================================================================
# TEST 2: Character Definitions
# ============================================================================
print("\n" + "=" * 80)
print("TEST 2: CHARACTER DEFINITIONS")
print("=" * 80)

required_keys = ['name', 'desc', 'health', 'speed', 'color', 'special_name', 'special_type', 'combos']

for i, char in enumerate(c.CHARACTERS):
    char_name = char.get('name', f'Character {i}')
    print(f"\nTesting {char_name}:")
    
    # Check required keys
    for key in required_keys:
        test(f"  {char_name} has '{key}'", key in char, f"Missing {key}")
    
    # Check data types
    if 'health' in char:
        test(f"  {char_name} health is number", isinstance(char['health'], (int, float)))
    if 'speed' in char:
        test(f"  {char_name} speed is number", isinstance(char['speed'], (int, float)))
    if 'combos' in char:
        test(f"  {char_name} combos is list", isinstance(char['combos'], list))
        test(f"  {char_name} has 2+ combos", len(char['combos']) >= 2)
        
        # Test each combo
        for j, combo in enumerate(char['combos']):
            combo_name = combo.get('name', f'Combo {j}')
            test(f"    {combo_name} has inputs", 'inputs' in combo)
            test(f"    {combo_name} has damage_mult", 'damage_mult' in combo)

# ============================================================================
# TEST 3: Projectile Classes
# ============================================================================
print("\n" + "=" * 80)
print("TEST 3: PROJECTILE CLASSES")
print("=" * 80)

projectile_classes = [
    ('PizzaSlice', PizzaSlice),
    ('Fireball', Fireball),
    ('CircuitBoard', CircuitBoard)
]

for name, ProjectileClass in projectile_classes:
    print(f"\nTesting {name}:")
    try:
        proj = ProjectileClass(400, 300, 1, 'neutral', None)
        
        test(f"  {name} instantiates", True)
        test(f"  {name} has rect attribute", hasattr(proj, 'rect'), "Missing rect attribute")
        test(f"  {name} has damage attribute", hasattr(proj, 'damage'))
        test(f"  {name} has owner attribute", hasattr(proj, 'owner'))
        test(f"  {name} has color attribute", hasattr(proj, 'color'))
        test(f"  {name} has update method", callable(getattr(proj, 'update', None)))
        test(f"  {name} has draw method", callable(getattr(proj, 'draw', None)))
        test(f"  {name} has on_hit method", callable(getattr(proj, 'on_hit', None)))
        
        # Test rect is valid
        if hasattr(proj, 'rect'):
            test(f"  {name} rect is pygame.Rect", isinstance(proj.rect, pygame.Rect))
            test(f"  {name} rect has position", hasattr(proj.rect, 'x') and hasattr(proj.rect, 'y'))
        
    except Exception as e:
        test(f"  {name} instantiation", False, str(e))

# ============================================================================
# TEST 4: StickFigure Animation
# ============================================================================
print("\n" + "=" * 80)
print("TEST 4: STICK FIGURE ANIMATION")
print("=" * 80)

animation_states = [
    'idle', 'walk', 'dash', 'jump', 'crouch', 'block',
    'light_punch', 'heavy_punch', 'light_kick', 'heavy_kick', 'special',
    'hit', 'knockdown', 'victory', 'defeat'
]

try:
    stick = StickFigure((255, 0, 0))
    test("StickFigure instantiates", True)
    test("StickFigure has color", hasattr(stick, 'color'))
    test("StickFigure has draw method", callable(getattr(stick, 'draw', None)))
    
    # Test each animation state
    screen = pygame.Surface((100, 100))
    for state in animation_states:
        try:
            stick.draw(screen, 50, 50, state, True)
            test(f"  Animation '{state}' works", True)
        except Exception as e:
            test(f"  Animation '{state}' works", False, str(e))
            
except Exception as e:
    test("StickFigure instantiation", False, str(e))

# ============================================================================
# TEST 5: Fighter Class
# ============================================================================
print("\n" + "=" * 80)
print("TEST 5: FIGHTER CLASS")
print("=" * 80)

controls_test = {
    'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w, 'crouch': pygame.K_s,
    'light': pygame.K_j, 'heavy': pygame.K_k, 'kick': pygame.K_l, 'special': pygame.K_i
}

for i, char in enumerate(c.CHARACTERS):
    char_name = char['name']
    print(f"\nTesting Fighter: {char_name}")
    
    try:
        fighter = Fighter(200, 200, char, controls_test, is_p2=False)
        
        test(f"  {char_name} Fighter instantiates", True)
        
        # Test attributes
        attributes = [
            'rect', 'health', 'max_health', 'speed', 'alive', 'attacking',
            'super_meter', 'combo_buffer', 'dashing', 'blocking', 'parry_window',
            'knockdown', 'invincible', 'animation_state', 'combo_hits', 'moves'
        ]
        
        for attr in attributes:
            test(f"    Has {attr}", hasattr(fighter, attr), f"Missing {attr}")
        
        # Test methods
        methods = [
            'move', 'attack', 'update', 'draw', 'dash', 'block', 'parry',
            'shoot_projectile', 'add_to_combo_buffer', 'detect_combo',
            'gain_super_meter', 'can_use_super', 'apply_knockdown', 'get_up'
        ]
        
        for method in methods:
            test(f"    Has {method}()", callable(getattr(fighter, method, None)), f"Missing {method}")
        
        # Test moves dictionary
        if hasattr(fighter, 'moves'):
            test(f"    Has moves dictionary", isinstance(fighter.moves, dict))
            expected_moves = ['light_punch', 'heavy_punch', 'light_kick', 'heavy_kick', 'special']
            for move in expected_moves:
                test(f"      Has '{move}' attack", move in fighter.moves)
        
        # Test initial values
        test(f"    Initial health > 0", fighter.health > 0)
        test(f"    Initial super_meter is 0", fighter.super_meter == 0)
        test(f"    Initially alive", fighter.alive == True)
        test(f"    Initially not attacking", fighter.attacking == False)
        
    except Exception as e:
        test(f"  {char_name} Fighter instantiation", False, str(e))

# ============================================================================
# TEST 6: Combat Mechanics
# ============================================================================
print("\n" + "=" * 80)
print("TEST 6: COMBAT MECHANICS")
print("=" * 80)

try:
    fighter1 = Fighter(200, 200, c.CHARACTERS[0], controls_test, is_p2=False)
    fighter2 = Fighter(400, 200, c.CHARACTERS[1], controls_test, is_p2=True)
    projectiles = []
    
    print("\nTesting Attack System:")
    
    # Test basic attack
    initial_cooldown = fighter1.attack_cooldown
    fighter1.attack('light_punch', fighter2, projectiles)
    test("  Attack executes", fighter1.attacking or fighter1.attack_cooldown != initial_cooldown)
    
    # Test projectile creation
    if c.CHARACTERS[1].get('special_type', '').startswith('projectile'):
        fighter2.attack('special', fighter1, projectiles)
        test("  Projectile created", len(projectiles) > 0)
        
        if len(projectiles) > 0:
            proj = projectiles[0]
            test("    Projectile has rect", hasattr(proj, 'rect'))
            test("    Projectile has damage", hasattr(proj, 'damage'))
            test("    Projectile has owner", hasattr(proj, 'owner'))
    
    print("\nTesting Super Meter:")
    fighter1.super_meter = 0
    fighter1.gain_super_meter(50)
    test("  Meter increases", fighter1.super_meter == 50)
    
    fighter1.super_meter = c.SUPER_METER_MAX
    test("  Can use super when full", fighter1.can_use_super())
    
    print("\nTesting Combo System:")
    fighter1.combo_buffer = []
    fighter1.add_to_combo_buffer('light')
    test("  Combo buffer adds input", len(fighter1.combo_buffer) > 0)
    
    print("\nTesting Knockdown:")
    fighter1.apply_knockdown()
    test("  Knockdown activates", fighter1.knockdown == True)
    test("  Knockdown sets frames", fighter1.knockdown_frames > 0)
    
    fighter1.get_up()
    test("  Get up deactivates knockdown", fighter1.knockdown == False)
    test("  Get up grants invincibility", fighter1.invincible == True)
    
except Exception as e:
    test("Combat mechanics test", False, str(e))

# ============================================================================
# TEST 7: Movement System
# ============================================================================
print("\n" + "=" * 80)
print("TEST 7: MOVEMENT SYSTEM")
print("=" * 80)

try:
    fighter = Fighter(200, 200, c.CHARACTERS[0], controls_test, is_p2=False)
    opponent = Fighter(400, 200, c.CHARACTERS[1], controls_test, is_p2=True)
    
    initial_x = fighter.rect.x
    fighter.move(opponent, 800, 600)
    test("  Move method executes", True)
    
    # Test dash
    if hasattr(fighter, 'dash') and callable(fighter.dash):
        fighter.dash_cooldown = 0
        fighter.on_ground = True
        fighter.dash()
        test("  Dash activates", fighter.dashing == True)
        test("  Dash timer set", fighter.dash_timer > 0)
    
    # Test block
    if hasattr(fighter, 'block') and callable(fighter.block):
        fighter.block()
        test("  Block activates", fighter.blocking == True)
    
except Exception as e:
    test("Movement system test", False, str(e))

# ============================================================================
# TEST 8: Particle System
# ============================================================================
print("\n" + "=" * 80)
print("TEST 8: PARTICLE SYSTEM")
print("=" * 80)

try:
    particle = Particle(400, 300, (255, 0, 0), (5, -5))
    test("Particle instantiates", True)
    test("Particle has x, y", hasattr(particle, 'x') and hasattr(particle, 'y'))
    test("Particle has velocity", hasattr(particle, 'vx') and hasattr(particle, 'vy'))
    test("Particle has update method", callable(getattr(particle, 'update', None)))
    test("Particle has draw method", callable(getattr(particle, 'draw', None)))
    
    # Test update
    initial_y = particle.y
    particle.update()
    test("Particle moves on update", particle.y != initial_y)
    
except Exception as e:
    test("Particle system test", False, str(e))

# ============================================================================
# TEST 9: Game Constants
# ============================================================================
print("\n" + "=" * 80)
print("TEST 9: GAME CONSTANTS")
print("=" * 80)

constants = [
    'DASH_COOLDOWN', 'PARRY_WINDOW', 'COMBO_INPUT_WINDOW', 'KNOCKDOWN_FRAMES',
    'SUPER_METER_MAX', 'BLOCK_DAMAGE_REDUCTION', 'BLOCK_STARTUP_FRAMES',
    'PARRY_VULNERABLE_FRAMES', 'GETUP_INVINCIBILITY'
]

for const in constants:
    test(f"Constant {const} exists", hasattr(c, const))
    if hasattr(c, const):
        value = getattr(c, const)
        test(f"  {const} is numeric", isinstance(value, (int, float)))

# ============================================================================
# TEST 10: All Combos
# ============================================================================
print("\n" + "=" * 80)
print("TEST 10: ALL CHARACTER COMBOS")
print("=" * 80)

total_combos = 0
for char in c.CHARACTERS:
    char_name = char['name']
    combos = char.get('combos', [])
    
    print(f"\n{char_name} - {len(combos)} combos:")
    total_combos += len(combos)
    
    for combo in combos:
        combo_name = combo.get('name', 'Unknown')
        inputs = combo.get('inputs', [])
        damage_mult = combo.get('damage_mult', 1.0)
        
        test(f"  {combo_name}: {inputs}", len(inputs) > 0)
        test(f"    Damage multiplier: {damage_mult}", damage_mult >= 1.0)

test(f"\nTotal combos across all characters", total_combos >= 8, f"Only {total_combos} combos")

# ============================================================================
# TEST 11: Projectile Updates
# ============================================================================
print("\n" + "=" * 80)
print("TEST 11: PROJECTILE UPDATES")
print("=" * 80)

for name, ProjectileClass in projectile_classes:
    try:
        proj = ProjectileClass(400, 300, 1, 'neutral', None)
        
        if hasattr(proj, 'rect'):
            initial_x = proj.rect.x
            proj.update()
            test(f"{name} moves on update", proj.rect.x != initial_x)
        
        # Test collision rect exists
        test(f"{name} collision rect valid", hasattr(proj, 'rect') and isinstance(proj.rect, pygame.Rect))
        
    except Exception as e:
        test(f"{name} update test", False, str(e))

# ============================================================================
# TEST 12: Attack Class
# ============================================================================
print("\n" + "=" * 80)
print("TEST 12: ATTACK CLASS")
print("=" * 80)

try:
    attack = Attack('Test Attack', 10, 200, 50, 20, 5, 10, knockdown=False)
    test("Attack instantiates", True)
    test("Attack has name", hasattr(attack, 'name'))
    test("Attack has damage", hasattr(attack, 'damage'))
    test("Attack has cooldown", hasattr(attack, 'cooldown'))
    test("Attack has width", hasattr(attack, 'width'))
    test("Attack has height", hasattr(attack, 'height'))
    test("Attack has stun", hasattr(attack, 'stun'))
    test("Attack has knockback", hasattr(attack, 'knockback'))
    test("Attack has knockdown flag", hasattr(attack, 'knockdown'))
except Exception as e:
    test("Attack class test", False, str(e))

# ============================================================================
# FINAL RESULTS
# ============================================================================
print("\n" + "=" * 80)
print("TEST RESULTS SUMMARY")
print("=" * 80)

total_tests = test_results['passed'] + test_results['failed']
pass_rate = (test_results['passed'] / total_tests * 100) if total_tests > 0 else 0

print(f"\nTotal Tests Run: {total_tests}")
print(f"✓ Passed: {test_results['passed']}")
print(f"✗ Failed: {test_results['failed']}")
print(f"Pass Rate: {pass_rate:.1f}%")

if test_results['failed'] > 0:
    print(f"\n{'=' * 80}")
    print("ERRORS FOUND:")
    print("=" * 80)
    for error in test_results['errors']:
        print(f"  - {error}")

print("\n" + "=" * 80)

if test_results['failed'] == 0:
    print("✅ ALL TESTS PASSED!")
else:
    print(f"⚠️  {test_results['failed']} TESTS FAILED - FIXING REQUIRED")

print("=" * 80)

sys.exit(0 if test_results['failed'] == 0 else 1)
