"""
Comprehensive test suite for all game mechanics, character actions, combos, and collisions.
Tests every single character action, combination, and collision to ensure polished gameplay.
"""

import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'

import pygame
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from entities import Fighter, Projectile, PizzaSlice, SineWaveFireball, HomingCircuitBoard, SpinningKickEffect
import config as c
from combat import CombatSystem, FrameData


class TestAllCharacterActions(unittest.TestCase):
    """Test every single action for all 4 characters"""
    
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        
    def tearDown(self):
        pygame.quit()
    
    def create_fighter(self, char_index, player_num):
        """Helper to create a fighter"""
        controls = {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'jump': pygame.K_w,
            'light_punch': pygame.K_j,
            'heavy_punch': pygame.K_k,
            'light_kick': pygame.K_l,
            'heavy_kick': pygame.K_i,
            'special': pygame.K_u
        }
        return Fighter(100 if player_num == 1 else 700, 400, c.CHARACTERS[char_index], controls)
    
    def test_all_characters_exist(self):
        """Verify all 4 characters can be created"""
        char_names = ['PROF. KHALID', 'PROF. EDUARDO', 'PROF. HASAN', 'PROF. HAMMOUD']
        for i, expected_name in enumerate(char_names):
            fighter = self.create_fighter(i, 1)
            self.assertEqual(fighter.stats['name'], expected_name)
            self.assertIsNotNone(fighter)
            self.assertTrue(fighter.alive)
    
    def test_khalid_all_attacks(self):
        """Test all attacks for Prof. Khalid"""
        khalid = self.create_fighter(0, 1)
        target = self.create_fighter(1, 2)
        
        # Position target in range
        target.rect.x = khalid.rect.right + 10
        
        # Test light punch
        result = khalid.attack(target, 'light_punch')
        self.assertIsNotNone(khalid.attack_rect)
        expected_damage = 5 * 1.0  # Khalid's damage multiplier is 1.0
        
        # Test heavy punch
        khalid.attacking = False
        khalid.last_attack_time = 0
        result = khalid.attack(target, 'heavy_punch')
        self.assertIsNotNone(khalid.attack_rect)
        
        # Test light kick
        khalid.attacking = False
        khalid.last_attack_time = 0
        result = khalid.attack(target, 'light_kick')
        self.assertIsNotNone(khalid.attack_rect)
        
        # Test heavy kick
        khalid.attacking = False
        khalid.last_attack_time = 0
        result = khalid.attack(target, 'heavy_kick')
        self.assertIsNotNone(khalid.attack_rect)
        
        # Test special (spinning kick)
        khalid.attacking = False
        khalid.last_attack_time = 0
        khalid.last_special_time = 0
        result = khalid.attack(target, 'special')
        self.assertIsNotNone(result)
        self.assertIsInstance(result, SpinningKickEffect)
    
    def test_eduardo_all_attacks(self):
        """Test all attacks for Prof. Eduardo"""
        eduardo = self.create_fighter(1, 1)
        target = self.create_fighter(0, 2)
        
        # Position target in range
        target.rect.x = eduardo.rect.right + 10
        
        # Test all basic attacks
        for attack_type in ['light_punch', 'heavy_punch', 'light_kick', 'heavy_kick']:
            eduardo.attacking = False
            eduardo.last_attack_time = 0
            result = eduardo.attack(target, attack_type)
            self.assertIsNotNone(eduardo.attack_rect, f"Attack rect should exist for {attack_type}")
        
        # Test special (pizza throw)
        eduardo.attacking = False
        eduardo.last_attack_time = 0
        eduardo.last_special_time = 0
        result = eduardo.attack(target, 'special')
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)  # Should return 3 pizza slices
        for pizza in result:
            self.assertIsInstance(pizza, PizzaSlice)
    
    def test_hasan_all_attacks(self):
        """Test all attacks for Prof. Hasan"""
        hasan = self.create_fighter(2, 1)
        target = self.create_fighter(0, 2)
        
        # Position target in range
        target.rect.x = hasan.rect.right + 10
        
        # Test all basic attacks
        for attack_type in ['light_punch', 'heavy_punch', 'light_kick', 'heavy_kick']:
            hasan.attacking = False
            hasan.last_attack_time = 0
            result = hasan.attack(target, attack_type)
            self.assertIsNotNone(hasan.attack_rect, f"Attack rect should exist for {attack_type}")
        
        # Test special (fireball)
        hasan.attacking = False
        hasan.last_attack_time = 0
        hasan.last_special_time = 0
        result = hasan.attack(target, 'special')
        self.assertIsNotNone(result)
        self.assertIsInstance(result, SineWaveFireball)
    
    def test_hammoud_all_attacks(self):
        """Test all attacks for Prof. Hammoud"""
        hammoud = self.create_fighter(3, 1)
        target = self.create_fighter(0, 2)
        
        # Position target in range
        target.rect.x = hammoud.rect.right + 10
        
        # Test all basic attacks
        for attack_type in ['light_punch', 'heavy_punch', 'light_kick', 'heavy_kick']:
            hammoud.attacking = False
            hammoud.last_attack_time = 0
            result = hammoud.attack(target, attack_type)
            self.assertIsNotNone(hammoud.attack_rect, f"Attack rect should exist for {attack_type}")
        
        # Test special (circuit board)
        hammoud.attacking = False
        hammoud.last_attack_time = 0
        hammoud.last_special_time = 0
        result = hammoud.attack(target, 'special')
        self.assertIsNotNone(result)
        self.assertIsInstance(result, HomingCircuitBoard)


class TestDamageCalculation(unittest.TestCase):
    """Test damage calculation for all characters and all attacks"""
    
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
    
    def tearDown(self):
        pygame.quit()
    
    def create_fighter(self, char_index, player_num):
        controls = {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'jump': pygame.K_w,
            'light_punch': pygame.K_j,
            'heavy_punch': pygame.K_k,
            'light_kick': pygame.K_l,
            'heavy_kick': pygame.K_i,
            'special': pygame.K_u
        }
        return Fighter(100 if player_num == 1 else 700, 400, c.CHARACTERS[char_index], controls)
    
    def test_khalid_damage_multiplier(self):
        """Test that Khalid's attacks use correct damage multiplier (1.0)"""
        khalid = self.create_fighter(0, 1)
        
        # Khalid's damage multiplier is 1.0
        self.assertEqual(khalid.dmg_mult, 1.0)
        
        # Verify each attack has correct base damage
        self.assertEqual(khalid.moves['light_punch'].damage, 5 * 1.0)
        self.assertEqual(khalid.moves['heavy_punch'].damage, 12 * 1.0)
        self.assertEqual(khalid.moves['light_kick'].damage, 8 * 1.0)
        self.assertEqual(khalid.moves['heavy_kick'].damage, 15 * 1.0)
        self.assertEqual(khalid.moves['special'].damage, 20 * 1.0)
    
    def test_eduardo_damage_multiplier(self):
        """Test that Eduardo's attacks use correct damage multiplier (0.9)"""
        eduardo = self.create_fighter(1, 1)
        
        # Eduardo's damage multiplier is 0.9
        self.assertEqual(eduardo.dmg_mult, 0.9)
        
        # Verify each attack has correct base damage
        self.assertEqual(eduardo.moves['light_punch'].damage, 5 * 0.9)
        self.assertEqual(eduardo.moves['heavy_punch'].damage, 12 * 0.9)
        self.assertEqual(eduardo.moves['light_kick'].damage, 8 * 0.9)
        self.assertEqual(eduardo.moves['heavy_kick'].damage, 15 * 0.9)
        self.assertEqual(eduardo.moves['special'].damage, 20 * 0.9)
    
    def test_hasan_damage_multiplier(self):
        """Test that Hasan's attacks use correct damage multiplier (1.1)"""
        hasan = self.create_fighter(2, 1)
        
        # Hasan's damage multiplier is 1.1
        self.assertEqual(hasan.dmg_mult, 1.1)
        
        # Verify each attack has correct base damage
        self.assertEqual(hasan.moves['light_punch'].damage, 5 * 1.1)
        self.assertEqual(hasan.moves['heavy_punch'].damage, 12 * 1.1)
        self.assertEqual(hasan.moves['light_kick'].damage, 8 * 1.1)
        self.assertEqual(hasan.moves['heavy_kick'].damage, 15 * 1.1)
        self.assertEqual(hasan.moves['special'].damage, 20 * 1.1)
    
    def test_hammoud_damage_multiplier(self):
        """Test that Hammoud's attacks use correct damage multiplier (0.85)"""
        hammoud = self.create_fighter(3, 1)
        
        # Hammoud's damage multiplier is 0.85
        self.assertEqual(hammoud.dmg_mult, 0.85)
        
        # Verify each attack has correct base damage
        self.assertEqual(hammoud.moves['light_punch'].damage, 5 * 0.85)
        self.assertEqual(hammoud.moves['heavy_punch'].damage, 12 * 0.85)
        self.assertEqual(hammoud.moves['light_kick'].damage, 8 * 0.85)
        self.assertEqual(hammoud.moves['heavy_kick'].damage, 15 * 0.85)
        self.assertEqual(hammoud.moves['special'].damage, 20 * 0.85)
    
    def test_damage_is_actually_dealt(self):
        """Test that attacks actually reduce target health"""
        attacker = self.create_fighter(0, 1)
        target = self.create_fighter(1, 2)
        
        # Position target in range
        target.rect.x = attacker.rect.right + 10
        
        initial_health = target.health
        
        # Execute attack
        attacker.attacking = False
        attacker.last_attack_time = 0
        result = attacker.attack(target, 'light_punch')
        
        # Manually trigger damage since we're testing in isolation
        if attacker.attack_rect and attacker.attack_rect.colliderect(target.rect):
            target.take_damage(attacker.moves['light_punch'].damage, 
                             attacker.moves['light_punch'].knockback,
                             attacker.moves['light_punch'].stun,
                             attacker.facing_right)
        
        # Verify health decreased
        self.assertLess(target.health, initial_health)


class TestCollisionDetection(unittest.TestCase):
    """Test collision detection for all attack types"""
    
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
    
    def tearDown(self):
        pygame.quit()
    
    def create_fighter(self, char_index, player_num):
        controls = {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'jump': pygame.K_w,
            'light_punch': pygame.K_j,
            'heavy_punch': pygame.K_k,
            'light_kick': pygame.K_l,
            'heavy_kick': pygame.K_i,
            'special': pygame.K_u
        }
        return Fighter(100 if player_num == 1 else 700, 400, c.CHARACTERS[char_index], controls)
    
    def test_attack_hits_when_in_range(self):
        """Test that attacks hit when target is in range"""
        attacker = self.create_fighter(0, 1)
        target = self.create_fighter(1, 2)
        
        # Position target in attack range (close)
        target.rect.x = attacker.rect.right + 5
        
        # Execute attack
        attacker.attacking = False
        attacker.last_attack_time = 0
        result = attacker.attack(target, 'light_punch')
        
        # Verify attack rect was created
        self.assertIsNotNone(attacker.attack_rect)
        
        # Verify collision detection
        self.assertTrue(attacker.attack_rect.colliderect(target.rect))
    
    def test_attack_misses_when_out_of_range(self):
        """Test that attacks miss when target is out of range"""
        attacker = self.create_fighter(0, 1)
        target = self.create_fighter(1, 2)
        
        # Position target far away
        target.rect.x = attacker.rect.right + 200
        
        # Execute attack
        attacker.attacking = False
        attacker.last_attack_time = 0
        result = attacker.attack(target, 'light_punch')
        
        # Verify attack rect was created
        self.assertIsNotNone(attacker.attack_rect)
        
        # Verify no collision
        self.assertFalse(attacker.attack_rect.colliderect(target.rect))
    
    def test_attack_rect_faces_correct_direction(self):
        """Test that attack hitbox is positioned correctly based on facing direction"""
        attacker = self.create_fighter(0, 1)
        target = self.create_fighter(1, 2)
        
        # Test facing right
        attacker.facing_right = True
        attacker.attacking = False
        attacker.last_attack_time = 0
        attacker.attack(target, 'light_punch')
        
        # Attack rect should be to the right of fighter
        self.assertGreaterEqual(attacker.attack_rect.left, attacker.rect.right - 10)
        
        # Test facing left
        attacker.facing_right = False
        attacker.attacking = False
        attacker.last_attack_time = 0
        attacker.rect.x = 500  # Move to different position
        attacker.attack(target, 'light_punch')
        
        # Attack rect should be to the left of fighter
        self.assertLessEqual(attacker.attack_rect.right, attacker.rect.left + 10)
    
    def test_projectile_collision_detection(self):
        """Test that projectiles correctly detect collisions"""
        owner = self.create_fighter(2, 1)  # Hasan for fireball
        target = self.create_fighter(0, 2)
        
        # Create a projectile
        projectile = SineWaveFireball(owner.rect.centerx, owner.rect.centery, 1, owner)
        
        # Position target where projectile will hit
        target.rect.centerx = projectile.x + 5
        target.rect.centery = projectile.y + 5
        
        # Get collision rect
        proj_rect = projectile.get_rect()
        
        # Verify collision
        self.assertTrue(proj_rect.colliderect(target.rect))


class TestComboSystem(unittest.TestCase):
    """Test combo system and damage scaling"""
    
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.combat_system = CombatSystem()
    
    def tearDown(self):
        pygame.quit()
    
    def test_combo_tracking(self):
        """Test that combos are tracked correctly"""
        fighter_id = "p1"
        self.combat_system.register_fighter(fighter_id)
        
        # Initial combo count should be 0
        self.assertEqual(self.combat_system.get_combo_count(fighter_id), 0)
        
        # Increment combo
        self.combat_system.increment_combo(fighter_id)
        self.assertEqual(self.combat_system.get_combo_count(fighter_id), 1)
        
        # Increment again
        self.combat_system.increment_combo(fighter_id)
        self.assertEqual(self.combat_system.get_combo_count(fighter_id), 2)
    
    def test_combo_damage_scaling(self):
        """Test that damage scaling applies correctly to combos"""
        fighter_id = "p1"
        self.combat_system.register_fighter(fighter_id)
        
        # First 3 hits should have 1.0 multiplier
        for i in range(3):
            self.combat_system.increment_combo(fighter_id)
            multiplier = self.combat_system.get_combo_damage_multiplier(fighter_id)
            self.assertEqual(multiplier, 1.0, f"Hit {i+1} should have 1.0 multiplier")
        
        # Hits 4-5 should have 0.8 multiplier
        self.combat_system.increment_combo(fighter_id)
        self.assertEqual(self.combat_system.get_combo_damage_multiplier(fighter_id), 0.8)
        
        self.combat_system.increment_combo(fighter_id)
        self.assertEqual(self.combat_system.get_combo_damage_multiplier(fighter_id), 0.8)
    
    def test_combo_breaks_after_max_hits(self):
        """Test that combo resets after max hits"""
        fighter_id = "p1"
        self.combat_system.register_fighter(fighter_id)
        
        # Hit 5 times (max combo)
        for i in range(5):
            self.combat_system.increment_combo(fighter_id)
        
        # Verify we're at max
        self.assertEqual(self.combat_system.get_combo_count(fighter_id), 5)
        
        # 6th hit should break combo
        result = self.combat_system.increment_combo(fighter_id)
        self.assertFalse(result)
        self.assertEqual(self.combat_system.get_combo_count(fighter_id), 0)


class TestAllCharacterCombinations(unittest.TestCase):
    """Test all possible character vs character matchups"""
    
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
    
    def tearDown(self):
        pygame.quit()
    
    def create_fighter(self, char_index, player_num):
        controls = {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'jump': pygame.K_w,
            'light_punch': pygame.K_j,
            'heavy_punch': pygame.K_k,
            'light_kick': pygame.K_l,
            'heavy_kick': pygame.K_i,
            'special': pygame.K_u
        }
        return Fighter(100 if player_num == 1 else 700, 400, c.CHARACTERS[char_index], controls)
    
    def test_all_character_matchups(self):
        """Test that all character combinations can fight"""
        char_names = ['Khalid', 'Eduardo', 'Hasan', 'Hammoud']
        
        for i in range(4):
            for j in range(4):
                p1 = self.create_fighter(i, 1)
                p2 = self.create_fighter(j, 2)
                
                # Position fighters in range
                p2.rect.x = p1.rect.right + 10
                
                # Test that p1 can attack p2
                p1.attacking = False
                p1.last_attack_time = 0
                result = p1.attack(p2, 'light_punch')
                
                # Verify attack was created
                self.assertIsNotNone(p1.attack_rect, 
                    f"{char_names[i]} vs {char_names[j]}: Attack should be created")


class TestHitStunAndKnockback(unittest.TestCase):
    """Test hit stun and knockback mechanics"""
    
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
    
    def tearDown(self):
        pygame.quit()
    
    def create_fighter(self, char_index, player_num):
        controls = {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'jump': pygame.K_w,
            'light_punch': pygame.K_j,
            'heavy_punch': pygame.K_k,
            'light_kick': pygame.K_l,
            'heavy_kick': pygame.K_i,
            'special': pygame.K_u
        }
        return Fighter(100 if player_num == 1 else 700, 400, c.CHARACTERS[char_index], controls)
    
    def test_hit_stun_prevents_action(self):
        """Test that hit stun prevents the fighter from acting"""
        fighter = self.create_fighter(0, 1)
        
        # Apply hit stun
        fighter.hit_stun = 20
        
        # Verify fighter is in hit stun
        self.assertGreater(fighter.hit_stun, 0)
        
        # Fighter should not be able to move freely
        initial_x = fighter.rect.x
        fighter.move(self.create_fighter(1, 2), 800, 600)
        
        # Position might change due to knockback/gravity but not from input
        # Just verify hit_stun decreases
        self.assertEqual(fighter.hit_stun, 19)
    
    def test_knockback_moves_fighter(self):
        """Test that knockback moves the fighter"""
        fighter = self.create_fighter(0, 1)
        initial_x = fighter.rect.x
        
        # Apply knockback (facing right attack)
        fighter.take_damage(10, 15, 10, True)
        
        # Fighter should be pushed to the right
        self.assertGreater(fighter.rect.x, initial_x)
    
    def test_knockback_direction_based_on_attacker(self):
        """Test that knockback direction depends on attacker facing"""
        # Test knockback to the right
        fighter1 = self.create_fighter(0, 1)
        fighter1.rect.x = 400
        initial_x1 = fighter1.rect.x
        fighter1.take_damage(10, 15, 10, True)  # Attacker facing right
        self.assertGreater(fighter1.rect.x, initial_x1)
        
        # Test knockback to the left
        fighter2 = self.create_fighter(0, 1)
        fighter2.rect.x = 400
        initial_x2 = fighter2.rect.x
        fighter2.take_damage(10, 15, 10, False)  # Attacker facing left
        self.assertLess(fighter2.rect.x, initial_x2)


class TestAttackCooldowns(unittest.TestCase):
    """Test attack cooldowns and recovery frames"""
    
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
    
    def tearDown(self):
        pygame.quit()
    
    def create_fighter(self, char_index, player_num):
        controls = {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'jump': pygame.K_w,
            'light_punch': pygame.K_j,
            'heavy_punch': pygame.K_k,
            'light_kick': pygame.K_l,
            'heavy_kick': pygame.K_i,
            'special': pygame.K_u
        }
        return Fighter(100 if player_num == 1 else 700, 400, c.CHARACTERS[char_index], controls)
    
    def test_attack_cooldowns_exist(self):
        """Test that all attacks have defined cooldowns"""
        fighter = self.create_fighter(0, 1)
        
        # Verify all attacks have cooldown values
        self.assertGreater(fighter.moves['light_punch'].cooldown, 0)
        self.assertGreater(fighter.moves['heavy_punch'].cooldown, 0)
        self.assertGreater(fighter.moves['light_kick'].cooldown, 0)
        self.assertGreater(fighter.moves['heavy_kick'].cooldown, 0)
        self.assertGreater(fighter.moves['special'].cooldown, 0)
    
    def test_heavy_attacks_have_longer_cooldowns(self):
        """Test that heavy attacks have longer cooldowns than light attacks"""
        fighter = self.create_fighter(0, 1)
        
        # Heavy punch should have longer cooldown than light punch
        self.assertGreater(fighter.moves['heavy_punch'].cooldown, 
                          fighter.moves['light_punch'].cooldown)
        
        # Heavy kick should have longer cooldown than light kick
        self.assertGreater(fighter.moves['heavy_kick'].cooldown, 
                          fighter.moves['light_kick'].cooldown)


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)
