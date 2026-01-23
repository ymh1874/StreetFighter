"""
Test visual rendering functions
Tests character drawing and effect rendering
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import pygame
import drawing
import config as c


class TestCharacterDrawing(unittest.TestCase):
    """Test character drawing functions exist and work"""
    
    def setUp(self):
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        self.surface = pygame.Surface((800, 600))
    
    def test_draw_khalid_exists(self):
        """Test draw_khalid function exists"""
        self.assertTrue(hasattr(drawing, 'draw_khalid'))
        
        # Should not raise exception
        drawing.draw_khalid(self.surface, 400, 400, True, 'idle', 0)
    
    def test_draw_eduardo_exists(self):
        """Test draw_eduardo function exists"""
        self.assertTrue(hasattr(drawing, 'draw_eduardo'))
        
        # Should not raise exception
        drawing.draw_eduardo(self.surface, 400, 400, True, 'idle', 0)
    
    def test_draw_hasan_exists(self):
        """Test draw_hasan function exists"""
        self.assertTrue(hasattr(drawing, 'draw_hasan'))
        
        # Should not raise exception
        drawing.draw_hasan(self.surface, 400, 400, True, 'idle', 0)
    
    def test_draw_hammoud_exists(self):
        """Test draw_hammoud function exists"""
        self.assertTrue(hasattr(drawing, 'draw_hammoud'))
        
        # Should not raise exception
        drawing.draw_hammoud(self.surface, 400, 400, True, 'idle', 0)
    
    def test_all_characters_have_drawing_functions(self):
        """Test all characters have corresponding drawing functions"""
        character_names = ['KHALID', 'EDUARDO', 'HASAN', 'HAMMOUD']
        
        for name in character_names:
            func_name = f'draw_{name.lower()}'
            self.assertTrue(hasattr(drawing, func_name), 
                          f"Missing drawing function for {name}")


class TestProjectileDrawing(unittest.TestCase):
    """Test projectile drawing functions"""
    
    def setUp(self):
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        self.surface = pygame.Surface((800, 600))
    
    def test_draw_pizza_slice(self):
        """Test pizza slice drawing function"""
        self.assertTrue(hasattr(drawing, 'draw_pizza_slice'))
        
        # Should not raise exception
        drawing.draw_pizza_slice(self.surface, 400, 300, 45)
    
    def test_draw_fireball(self):
        """Test fireball drawing function"""
        self.assertTrue(hasattr(drawing, 'draw_fireball'))
        
        # Should not raise exception
        drawing.draw_fireball(self.surface, 400, 300, 0)
    
    def test_draw_circuit_board(self):
        """Test circuit board drawing function"""
        self.assertTrue(hasattr(drawing, 'draw_circuit_board'))
        
        # Should not raise exception
        drawing.draw_circuit_board(self.surface, 400, 300, 0)


class TestHitEffects(unittest.TestCase):
    """Test hit effect rendering"""
    
    def setUp(self):
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        self.surface = pygame.Surface((800, 600))
    
    def test_draw_hit_effect(self):
        """Test hit effect drawing function"""
        self.assertTrue(hasattr(drawing, 'draw_hit_effect'))
        
        # Should not raise exception for different effect types
        drawing.draw_hit_effect(self.surface, 400, 300, 'light', c.YELLOW, 0)
        drawing.draw_hit_effect(self.surface, 400, 300, 'heavy', c.RED, 0)
        drawing.draw_hit_effect(self.surface, 400, 300, 'special', c.ORANGE, 0)


class TestVictoryPoses(unittest.TestCase):
    """Test victory pose drawing functions"""
    
    def setUp(self):
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        self.surface = pygame.Surface((800, 600))
    
    def test_victory_pose_functions_exist(self):
        """Test victory pose functions exist for all characters"""
        victory_functions = [
            'draw_victory_pose_khalid',
            'draw_victory_pose_eduardo',
            'draw_victory_pose_hasan',
            'draw_victory_pose_hammoud'
        ]
        
        for func_name in victory_functions:
            self.assertTrue(hasattr(drawing, func_name), 
                          f"Missing victory pose function: {func_name}")


class TestAnimationStates(unittest.TestCase):
    """Test different animation states render correctly"""
    
    def setUp(self):
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        self.surface = pygame.Surface((800, 600))
    
    def test_khalid_animation_states(self):
        """Test Khalid renders in different animation states"""
        states = ['idle', 'punch', 'kick', 'special', 'light_punch', 'heavy_kick']
        
        for state in states:
            # Should not raise exception
            drawing.draw_khalid(self.surface, 400, 400, True, state, 0)
    
    def test_facing_direction(self):
        """Test characters render facing both directions"""
        # Should not raise exception
        drawing.draw_khalid(self.surface, 400, 400, True, 'idle', 0)
        drawing.draw_khalid(self.surface, 400, 400, False, 'idle', 0)


class TestColorConstants(unittest.TestCase):
    """Test all required color constants exist"""
    
    def test_skin_tone_colors_exist(self):
        """Test skin tone colors are defined"""
        self.assertTrue(hasattr(c, 'KHALID_SKIN'))
        self.assertTrue(hasattr(c, 'EDUARDO_SKIN'))
        self.assertTrue(hasattr(c, 'HASAN_SKIN'))
        self.assertTrue(hasattr(c, 'HAMMOUD_SKIN'))
    
    def test_outfit_colors_exist(self):
        """Test outfit colors are defined"""
        self.assertTrue(hasattr(c, 'KHALID_GI'))
        self.assertTrue(hasattr(c, 'EDUARDO_APRON'))
        self.assertTrue(hasattr(c, 'HASAN_ROBE'))
        self.assertTrue(hasattr(c, 'HAMMOUD_COAT'))
    
    def test_effect_colors_exist(self):
        """Test effect colors are defined"""
        self.assertTrue(hasattr(c, 'COMIC_TEXT'))
        self.assertTrue(hasattr(c, 'COMIC_OUTLINE'))
        self.assertTrue(hasattr(c, 'DIRT_BROWN'))


if __name__ == '__main__':
    unittest.main()
