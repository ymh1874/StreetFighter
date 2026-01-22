"""
Test combat system mechanics
Tests frame data, combos, damage scaling, and attack recovery
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import pygame
from combat import CombatSystem, FrameData, AttackBuffer, SpecialMoveData
import config as c


class TestFrameData(unittest.TestCase):
    """Test attack frame data"""
    
    def test_light_punch_can_move_early(self):
        """Light punch should allow movement after active frames"""
        # Light punch: startup=3, active=2, so can move after frame 5
        self.assertTrue(FrameData.can_move_during_attack('light_punch', 6))
        self.assertFalse(FrameData.can_move_during_attack('light_punch', 4))
    
    def test_heavy_punch_requires_full_recovery(self):
        """Heavy punch should require full recovery before movement"""
        # Heavy punch: total=27 frames
        self.assertFalse(FrameData.can_move_during_attack('heavy_punch', 20))
        self.assertTrue(FrameData.can_move_during_attack('heavy_punch', 28))
    
    def test_light_kick_can_move_early(self):
        """Light kick should allow movement after active frames"""
        # Light kick: startup=4, active=3, so can move after frame 7
        self.assertTrue(FrameData.can_move_during_attack('light_kick', 8))
        self.assertFalse(FrameData.can_move_during_attack('light_kick', 6))
    
    def test_special_requires_full_recovery(self):
        """Special moves should require full recovery"""
        # Special: total=42 frames
        self.assertFalse(FrameData.can_move_during_attack('special', 30))
        self.assertTrue(FrameData.can_move_during_attack('special', 43))
    
    def test_get_attack_duration(self):
        """Test getting attack durations"""
        self.assertEqual(FrameData.get_attack_duration('light_punch'), 10)
        self.assertEqual(FrameData.get_attack_duration('heavy_punch'), 27)
        self.assertEqual(FrameData.get_attack_duration('light_kick'), 13)
        self.assertEqual(FrameData.get_attack_duration('heavy_kick'), 33)


class TestCombatSystem(unittest.TestCase):
    """Test combo system"""
    
    def setUp(self):
        self.combat = CombatSystem()
        self.combat.register_fighter('p1')
        self.combat.register_fighter('p2')
    
    def test_combo_tracking(self):
        """Test combo hit tracking"""
        self.assertEqual(self.combat.get_combo_count('p1'), 0)
        
        self.combat.increment_combo('p1')
        self.assertEqual(self.combat.get_combo_count('p1'), 1)
        
        self.combat.increment_combo('p1')
        self.assertEqual(self.combat.get_combo_count('p1'), 2)
    
    def test_combo_damage_scaling(self):
        """Test damage scaling on hits 4-5"""
        # First 3 hits should be 100%
        for i in range(3):
            self.combat.increment_combo('p1')
            self.assertEqual(self.combat.get_combo_damage_multiplier('p1'), 1.0)
        
        # Hit 4 should be 80%
        self.combat.increment_combo('p1')
        self.assertEqual(self.combat.get_combo_damage_multiplier('p1'), 0.8)
        
        # Hit 5 should be 80%
        self.combat.increment_combo('p1')
        self.assertEqual(self.combat.get_combo_damage_multiplier('p1'), 0.8)
    
    def test_max_combo_break(self):
        """Test combo breaks after 5 hits"""
        # Add 5 hits
        for i in range(5):
            result = self.combat.increment_combo('p1')
            self.assertTrue(result)
        
        # 6th hit should break combo
        result = self.combat.increment_combo('p1')
        self.assertFalse(result)
        self.assertEqual(self.combat.get_combo_count('p1'), 0)
    
    def test_combo_reset(self):
        """Test manual combo reset"""
        self.combat.increment_combo('p1')
        self.combat.increment_combo('p1')
        self.assertEqual(self.combat.get_combo_count('p1'), 2)
        
        self.combat.reset_combo('p1')
        self.assertEqual(self.combat.get_combo_count('p1'), 0)


class TestAttackBuffer(unittest.TestCase):
    """Test input buffering system"""
    
    def setUp(self):
        self.buffer = AttackBuffer(buffer_window=5)
    
    def test_buffer_attack(self):
        """Test buffering an attack"""
        timestamp = 100
        self.buffer.buffer_attack('p1', 'light_punch', timestamp)
        
        # Should retrieve within window
        result = self.buffer.get_buffered_attack('p1', timestamp + 50)
        self.assertEqual(result, 'light_punch')
    
    def test_buffer_expiration(self):
        """Test buffer expires after window"""
        timestamp = 100
        self.buffer.buffer_attack('p1', 'heavy_punch', timestamp)
        
        # Should expire after window (5 frames at 60fps = ~83ms)
        result = self.buffer.get_buffered_attack('p1', timestamp + 200)
        self.assertIsNone(result)
    
    def test_clear_buffer(self):
        """Test manual buffer clear"""
        self.buffer.buffer_attack('p1', 'light_kick', 100)
        self.buffer.clear_buffer('p1')
        
        result = self.buffer.get_buffered_attack('p1', 120)
        self.assertIsNone(result)


class TestSpecialMoveData(unittest.TestCase):
    """Test special move configurations"""
    
    def test_spinning_kick_data(self):
        """Test Khalid's spinning kick data"""
        data = SpecialMoveData.SPINNING_KICK
        self.assertEqual(data['damage_per_hit'], 8)
        self.assertEqual(data['num_hits'], 3)
        self.assertEqual(data['forward_movement'], 150)
        self.assertEqual(data['cooldown'], 2000)
    
    def test_pizza_throw_data(self):
        """Test Eduardo's pizza throw data"""
        data = SpecialMoveData.PIZZA_THROW
        self.assertEqual(data['damage_per_slice'], 6)
        self.assertEqual(data['num_slices'], 3)
        self.assertEqual(data['speed'], 5)
        self.assertEqual(data['cooldown'], 2000)
    
    def test_fireball_data(self):
        """Test Hasan's fireball data"""
        data = SpecialMoveData.FIREBALL
        self.assertEqual(data['damage'], 15)
        self.assertEqual(data['speed'], 8)  # Fastest
        self.assertEqual(data['cooldown'], 2000)
    
    def test_circuit_board_data(self):
        """Test Hammoud's circuit board data"""
        data = SpecialMoveData.CIRCUIT_BOARD
        self.assertEqual(data['damage'], 20)  # Highest damage
        self.assertEqual(data['speed'], 4)   # Slowest
        self.assertEqual(data['cooldown'], 2000)


if __name__ == '__main__':
    # Initialize pygame for tests that might need it
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    os.environ['SDL_AUDIODRIVER'] = 'dummy'
    pygame.init()
    
    unittest.main()
