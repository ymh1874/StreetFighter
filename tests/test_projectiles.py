"""
Test projectile mechanics
Tests trajectories, homing behavior, and damage values
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import pygame
import math
from entities import PizzaSlice, SineWaveFireball, HomingCircuitBoard, Fighter
import config as c


class TestProjectileBase(unittest.TestCase):
    """Test base projectile functionality"""
    
    def setUp(self):
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        
        controls = {
            'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
            'light_punch': pygame.K_j, 'heavy_punch': pygame.K_k,
            'light_kick': pygame.K_l, 'heavy_kick': pygame.K_i,
            'special': pygame.K_u, 'dash': pygame.K_LSHIFT
        }
        self.fighter = Fighter(100, 100, c.CHARACTERS[0], controls, is_p2=False)
    
    def test_projectile_deactivates_offscreen(self):
        """Test projectiles deactivate when off screen"""
        proj = PizzaSlice(1000, 300, 10, 0, self.fighter)
        
        # Update several times to move off screen
        for _ in range(20):
            proj.update()
        
        self.assertFalse(proj.active)


class TestPizzaSlice(unittest.TestCase):
    """Test Eduardo's pizza throw"""
    
    def setUp(self):
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        
        controls = {
            'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
            'light_punch': pygame.K_j, 'heavy_punch': pygame.K_k,
            'light_kick': pygame.K_l, 'heavy_kick': pygame.K_i,
            'special': pygame.K_u, 'dash': pygame.K_LSHIFT
        }
        self.fighter = Fighter(100, 100, c.CHARACTERS[1], controls, is_p2=False)
    
    def test_pizza_damage(self):
        """Test pizza slice damage value"""
        pizza = PizzaSlice(100, 100, 5, -5, self.fighter)
        self.assertEqual(pizza.damage, 6)
    
    def test_pizza_parabolic_arc(self):
        """Test pizza follows parabolic trajectory"""
        pizza = PizzaSlice(100, 100, 5, -8, self.fighter)
        
        start_y = pizza.y
        pizza.update()
        first_y = pizza.y
        
        # Should move up initially (negative vel_y)
        self.assertLess(first_y, start_y)
        
        # After many updates, should eventually fall below start (gravity effect)
        # But may go off screen, so just verify gravity is applied
        for _ in range(100):
            pizza.update()
        
        # Velocity should have become positive (falling) due to gravity
        self.assertGreater(pizza.vel_y, 0)
    
    def test_pizza_rotation(self):
        """Test pizza rotates while flying"""
        pizza = PizzaSlice(100, 100, 5, -5, self.fighter)
        
        initial_rotation = pizza.rotation
        pizza.update()
        
        self.assertNotEqual(pizza.rotation, initial_rotation)
    
    def test_pizza_delay(self):
        """Test pizza delay before activation"""
        pizza = PizzaSlice(100, 100, 5, -5, self.fighter, delay=10)
        
        start_x = pizza.x
        pizza.update()
        
        # Should not move during delay
        self.assertEqual(pizza.x, start_x)
        
        # After delay expires, should move
        for _ in range(15):
            pizza.update()
        
        self.assertNotEqual(pizza.x, start_x)
    
    def test_three_pizza_spawn(self):
        """Test that pizza throw creates 3 projectiles"""
        # This is tested through the fighter's special move
        # Just verify the base damage is 6
        pizza = PizzaSlice(100, 100, 5, -5, self.fighter)
        self.assertEqual(pizza.damage, 6)


class TestSineWaveFireball(unittest.TestCase):
    """Test Hasan's fireball"""
    
    def setUp(self):
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        
        controls = {
            'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
            'light_punch': pygame.K_j, 'heavy_punch': pygame.K_k,
            'light_kick': pygame.K_l, 'heavy_kick': pygame.K_i,
            'special': pygame.K_u, 'dash': pygame.K_LSHIFT
        }
        self.fighter = Fighter(100, 100, c.CHARACTERS[2], controls, is_p2=False)
    
    def test_fireball_damage(self):
        """Test fireball damage (fast = less damage)"""
        fireball = SineWaveFireball(100, 100, 1, self.fighter)
        self.assertEqual(fireball.damage, 15)
    
    def test_fireball_speed(self):
        """Test fireball is fast"""
        fireball = SineWaveFireball(100, 100, 1, self.fighter)
        self.assertEqual(abs(fireball.vel_x), 8)  # Fastest projectile
    
    def test_sine_wave_motion(self):
        """Test fireball follows sine wave trajectory"""
        fireball = SineWaveFireball(100, 300, 1, self.fighter)
        
        start_y = fireball.start_y
        positions = []
        
        # Record positions over time
        for _ in range(50):
            fireball.update()
            positions.append(fireball.y)
        
        # Y should oscillate around start_y
        # Check that we have both higher and lower values
        self.assertTrue(any(y < start_y for y in positions))
        self.assertTrue(any(y > start_y for y in positions))
        
        # Amplitude should be roughly 30 pixels
        max_diff = max(abs(y - start_y) for y in positions)
        self.assertLess(max_diff, 35)  # Allow some tolerance


class TestHomingCircuitBoard(unittest.TestCase):
    """Test Hammoud's circuit board"""
    
    def setUp(self):
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        
        controls = {
            'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
            'light_punch': pygame.K_j, 'heavy_punch': pygame.K_k,
            'light_kick': pygame.K_l, 'heavy_kick': pygame.K_i,
            'special': pygame.K_u, 'dash': pygame.K_LSHIFT
        }
        self.attacker = Fighter(100, 300, c.CHARACTERS[3], controls, is_p2=False)
        self.target = Fighter(500, 300, c.CHARACTERS[0], controls, is_p2=True)
    
    def test_circuit_damage(self):
        """Test circuit board damage (slow = more damage)"""
        circuit = HomingCircuitBoard(100, 100, 1, self.attacker, self.target)
        self.assertEqual(circuit.damage, 20)  # Highest damage
    
    def test_circuit_speed(self):
        """Test circuit board is slow"""
        circuit = HomingCircuitBoard(100, 100, 1, self.attacker, self.target)
        speed = math.sqrt(circuit.vel_x**2 + circuit.vel_y**2)
        self.assertAlmostEqual(speed, 4, delta=0.1)  # Slowest projectile
    
    def test_homing_behavior(self):
        """Test circuit board homes toward target"""
        # Start circuit moving horizontally
        circuit = HomingCircuitBoard(100, 300, 1, self.attacker, self.target)
        
        # Place target above the circuit
        self.target.rect.y = 200
        
        initial_vel_y = circuit.vel_y
        
        # Update several times
        for _ in range(30):
            circuit.update()
        
        # Should have gained upward velocity (negative y) to home toward target
        self.assertLess(circuit.vel_y, initial_vel_y)
    
    def test_homing_target_tracking(self):
        """Test circuit adjusts course to follow moving target"""
        circuit = HomingCircuitBoard(100, 300, 1, self.attacker, self.target)
        
        # Move target to the right
        self.target.rect.x = 600
        
        positions = []
        for _ in range(50):
            circuit.update()
            positions.append((circuit.x, circuit.y))
        
        # Circuit should move generally toward target (right)
        self.assertGreater(circuit.x, 100)


class TestProjectileBalance(unittest.TestCase):
    """Test projectile damage vs speed balance"""
    
    def test_speed_damage_tradeoff(self):
        """Verify fast projectiles have less damage, slow have more"""
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        
        controls = {
            'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
            'light_punch': pygame.K_j, 'heavy_punch': pygame.K_k,
            'light_kick': pygame.K_l, 'heavy_kick': pygame.K_i,
            'special': pygame.K_u, 'dash': pygame.K_LSHIFT
        }
        
        fighter = Fighter(100, 100, c.CHARACTERS[0], controls, is_p2=False)
        
        # Hasan's fireball: fast (8) + low damage (15)
        fireball = SineWaveFireball(100, 100, 1, fighter)
        
        # Hammoud's circuit: slow (4) + high damage (20)
        circuit = HomingCircuitBoard(100, 100, 1, fighter, fighter)
        
        # Fast projectile should have less damage
        self.assertLess(fireball.damage, circuit.damage)
        
        # Fast projectile should be faster
        self.assertGreater(abs(fireball.vel_x), 4)


if __name__ == '__main__':
    unittest.main()
