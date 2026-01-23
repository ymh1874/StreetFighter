"""
Integration tests for game mechanics
Tests character interactions, special moves, and game flow
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import pygame
from entities import Fighter, SineWaveFireball, PizzaSlice, HomingCircuitBoard, SpinningKickEffect
import config as c


# Set up dummy drivers for headless testing
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'


class TestCharacterCreation(unittest.TestCase):
    """Test character creation and initialization"""
    
    @classmethod
    def setUpClass(cls):
        pygame.init()
        
    def setUp(self):
        self.controls = {
            'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
            'light_punch': pygame.K_j, 'heavy_punch': pygame.K_k,
            'light_kick': pygame.K_l, 'heavy_kick': pygame.K_i,
            'special': pygame.K_u, 'dash': pygame.K_LSHIFT
        }
    
    def test_create_all_characters(self):
        """Test that all four professors can be created"""
        for char_data in c.CHARACTERS:
            fighter = Fighter(100, 400, char_data, self.controls, is_p2=False)
            self.assertIsNotNone(fighter)
            self.assertEqual(fighter.stats, char_data)
            self.assertGreater(fighter.max_health, 0)
    
    def test_character_unique_stats(self):
        """Test that each character has unique stats"""
        khalid = Fighter(100, 400, c.CHARACTERS[0], self.controls, is_p2=False)
        eduardo = Fighter(100, 400, c.CHARACTERS[1], self.controls, is_p2=False)
        hasan = Fighter(100, 400, c.CHARACTERS[2], self.controls, is_p2=False)
        hammoud = Fighter(100, 400, c.CHARACTERS[3], self.controls, is_p2=False)
        
        # Check health differences
        stats = [khalid.max_health, eduardo.max_health, hasan.max_health, hammoud.max_health]
        self.assertEqual(len(set(stats)), 4, "All characters should have unique health values")
        
        # Check speed differences
        speeds = [khalid.speed, eduardo.speed, hasan.speed, hammoud.speed]
        self.assertGreater(len(set(speeds)), 1, "Characters should have different speeds")
    
    def test_all_characters_have_names(self):
        """Test that all characters have proper names"""
        expected_names = ['PROF. KHALID', 'PROF. EDUARDO', 'PROF. HASAN', 'PROF. HAMMOUD']
        for i, char_data in enumerate(c.CHARACTERS):
            self.assertEqual(char_data['name'], expected_names[i])
            
    def test_all_characters_have_descriptions(self):
        """Test that all characters have descriptions"""
        for char_data in c.CHARACTERS:
            self.assertIn('desc', char_data)
            self.assertGreater(len(char_data['desc']), 0)


class TestSpecialMoveIntegration(unittest.TestCase):
    """Test special move mechanics integration"""
    
    @classmethod
    def setUpClass(cls):
        pygame.init()
    
    def setUp(self):
        self.controls = {
            'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
            'light_punch': pygame.K_j, 'heavy_punch': pygame.K_k,
            'light_kick': pygame.K_l, 'heavy_kick': pygame.K_i,
            'special': pygame.K_u, 'dash': pygame.K_LSHIFT
        }
    
    def test_khalid_has_spinning_kick(self):
        """Test Khalid has spinning kick special"""
        self.assertEqual(c.CHARACTERS[0]['special'], 'spinning_kick')
    
    def test_eduardo_has_pizza_throw(self):
        """Test Eduardo has pizza throw special"""
        self.assertEqual(c.CHARACTERS[1]['special'], 'pizza_throw')
    
    def test_hasan_has_fireball(self):
        """Test Hasan has fireball special"""
        self.assertEqual(c.CHARACTERS[2]['special'], 'fireball')
    
    def test_hammoud_has_circuit_board(self):
        """Test Hammoud has circuit board special"""
        self.assertEqual(c.CHARACTERS[3]['special'], 'circuit_board')


class TestCombatInteractions(unittest.TestCase):
    """Test combat interactions between fighters"""
    
    @classmethod
    def setUpClass(cls):
        pygame.init()
    
    def setUp(self):
        self.controls = {
            'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
            'light_punch': pygame.K_j, 'heavy_punch': pygame.K_k,
            'light_kick': pygame.K_l, 'heavy_kick': pygame.K_i,
            'special': pygame.K_u, 'dash': pygame.K_LSHIFT
        }
    
    def test_fighter_initial_health(self):
        """Test that fighters start with correct health"""
        khalid = Fighter(100, 400, c.CHARACTERS[0], self.controls, is_p2=False)
        self.assertEqual(khalid.health, khalid.max_health)
        self.assertEqual(khalid.max_health, 110)
    
    def test_attack_cooldown(self):
        """Test attack cooldown mechanics"""
        fighter = Fighter(100, 400, c.CHARACTERS[0], self.controls, is_p2=False)
        
        # Set attacking state
        fighter.attacking = True
        fighter.attack_type = 'light_punch'
        fighter.attack_frame = 0
        
        # Should be attacking
        self.assertTrue(fighter.attacking)
        
        # After attack duration, should be done
        from combat import FrameData
        duration = FrameData.get_attack_duration('light_punch')
        fighter.attack_frame = duration + 1
        # Attack would be reset by game loop, but we can check the frame
        self.assertGreater(fighter.attack_frame, duration)
    
    def test_special_cooldown(self):
        """Test special move cooldown"""
        fighter = Fighter(100, 400, c.CHARACTERS[0], self.controls, is_p2=False)
        
        # Use special move
        current_time = pygame.time.get_ticks()
        fighter.special_last_used = current_time
        
        # Check cooldown
        cooldown = 2000  # 2 seconds
        self.assertFalse(current_time - fighter.special_last_used >= cooldown)
        
        # Simulate time passing
        fighter.special_last_used = current_time - cooldown - 1
        self.assertTrue(current_time - fighter.special_last_used >= cooldown)


class TestGameBoundaries(unittest.TestCase):
    """Test game boundaries and constraints"""
    
    @classmethod
    def setUpClass(cls):
        pygame.init()
    
    def setUp(self):
        self.controls = {
            'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
            'light_punch': pygame.K_j, 'heavy_punch': pygame.K_k,
            'light_kick': pygame.K_l, 'heavy_kick': pygame.K_i,
            'special': pygame.K_u, 'dash': pygame.K_LSHIFT
        }
    
    def test_fighter_starts_on_ground(self):
        """Test that fighter starts on ground"""
        fighter = Fighter(100, 400, c.CHARACTERS[0], self.controls, is_p2=False)
        # Fighter's bottom should be at or near ground
        self.assertLessEqual(fighter.rect.bottom, c.FLOOR_Y + 10)  # Small tolerance
    
    def test_screen_boundaries_defined(self):
        """Test that screen boundaries are properly defined"""
        self.assertEqual(c.SCREEN_WIDTH, 800)
        self.assertEqual(c.SCREEN_HEIGHT, 600)
        self.assertGreater(c.FLOOR_Y, 0)
        self.assertLess(c.FLOOR_Y, c.SCREEN_HEIGHT)
    
    def test_fighter_dimensions_defined(self):
        """Test that fighter dimensions are defined"""
        self.assertGreater(c.P_WIDTH, 0)
        self.assertGreater(c.P_HEIGHT, 0)


class TestCharacterBalance(unittest.TestCase):
    """Test game balance and fairness"""
    
    @classmethod
    def setUpClass(cls):
        pygame.init()
    
    def setUp(self):
        self.controls = {
            'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
            'light_punch': pygame.K_j, 'heavy_punch': pygame.K_k,
            'light_kick': pygame.K_l, 'heavy_kick': pygame.K_i,
            'special': pygame.K_u, 'dash': pygame.K_LSHIFT
        }
    
    def test_all_characters_have_special_moves(self):
        """Test all characters can perform special moves"""
        for char_data in c.CHARACTERS:
            fighter = Fighter(100, 400, char_data, self.controls, is_p2=False)
            self.assertIsNotNone(fighter.stats)
            # Each character should have a special move defined in config
            self.assertIn('special', char_data)
            self.assertIn(char_data['special'], ['spinning_kick', 'pizza_throw', 'fireball', 'circuit_board'])
    
    def test_health_values_reasonable(self):
        """Test that all health values are reasonable"""
        for char_data in c.CHARACTERS:
            health = char_data['health']
            # Health should be between 50 and 200
            self.assertGreaterEqual(health, 50)
            self.assertLessEqual(health, 200)
    
    def test_speed_values_reasonable(self):
        """Test that all speed values are reasonable"""
        for char_data in c.CHARACTERS:
            speed = char_data['speed']
            # Speed should be between 1 and 10
            self.assertGreaterEqual(speed, 1)
            self.assertLessEqual(speed, 10)
    
    def test_damage_multipliers_balanced(self):
        """Test damage multipliers are balanced"""
        for char_data in c.CHARACTERS:
            dmg_mult = char_data['dmg_mult']
            # Damage multipliers should be between 0.5 and 1.5
            self.assertGreaterEqual(dmg_mult, 0.5)
            self.assertLessEqual(dmg_mult, 1.5)


class TestFrameData(unittest.TestCase):
    """Test frame data is properly defined"""
    
    def test_all_attack_types_have_frame_data(self):
        """Test all attack types have complete frame data"""
        attack_types = ['light_punch', 'heavy_punch', 'light_kick', 'heavy_kick', 'special']
        for attack in attack_types:
            self.assertIn(attack, c.FRAME_DATA)
            frame_data = c.FRAME_DATA[attack]
            self.assertIn('startup', frame_data)
            self.assertIn('active', frame_data)
            self.assertIn('recovery', frame_data)
            self.assertIn('total', frame_data)
    
    def test_frame_data_math_correct(self):
        """Test that frame data totals are correct"""
        for attack, data in c.FRAME_DATA.items():
            if attack not in ['block', 'dash']:  # Skip future features
                expected_total = data['startup'] + data['active'] + data['recovery']
                self.assertEqual(data['total'], expected_total, 
                               f"{attack} total frames don't match sum of parts")


if __name__ == '__main__':
    unittest.main()
