"""
AI System for CMUQ Arena
Implements computer-controlled opponent with multiple difficulty levels
"""

import pygame
import random
import config as c

class AIController:
    """
    AI controller for computer-controlled fighters
    Implements different difficulty levels and behaviors
    """
    
    def __init__(self, difficulty='medium'):
        """
        Initialize AI controller
        
        Args:
            difficulty: 'easy', 'medium', or 'hard'
        """
        self.difficulty = difficulty
        
        # Difficulty settings
        if difficulty == 'easy':
            self.reaction_time = 500  # ms
            self.attack_probability = 0.3
            self.block_probability = 0.2
            self.combo_probability = 0.1
        elif difficulty == 'hard':
            self.reaction_time = 100  # ms
            self.attack_probability = 0.8
            self.block_probability = 0.7
            self.combo_probability = 0.6
        else:  # medium
            self.reaction_time = 300  # ms
            self.attack_probability = 0.5
            self.block_probability = 0.4
            self.combo_probability = 0.3
        
        # AI state
        self.last_decision = 0
        self.current_action = None
        self.target_distance = 0
    
    def update(self, ai_fighter, opponent, screen_width, screen_height):
        """
        Update AI logic and return simulated key presses
        
        Args:
            ai_fighter: The Fighter controlled by AI
            opponent: The opponent Fighter
            screen_width: Screen width for bounds
            screen_height: Screen height for bounds
            
        Returns:
            Dictionary of simulated key states
        """
        current_time = pygame.time.get_ticks()
        
        # Only make decisions at reaction time intervals
        if current_time - self.last_decision < self.reaction_time:
            return self._execute_current_action(ai_fighter, opponent)
        
        self.last_decision = current_time
        
        # Calculate distance to opponent
        self.target_distance = abs(ai_fighter.rect.centerx - opponent.rect.centerx)
        
        # Decide action based on game state
        if ai_fighter.hit_stun > 0:
            # Can't act while stunned
            self.current_action = 'stunned'
        elif self.target_distance < 80:
            # Close range - attack or retreat
            self.current_action = self._decide_close_range(ai_fighter, opponent)
        elif self.target_distance < 200:
            # Medium range - approach and attack
            self.current_action = self._decide_medium_range(ai_fighter, opponent)
        else:
            # Far range - approach
            self.current_action = 'approach'
        
        return self._execute_current_action(ai_fighter, opponent)
    
    def _decide_close_range(self, ai_fighter, opponent):
        """Decide action when close to opponent"""
        # If opponent is attacking, try to block or retreat
        if opponent.attacking and random.random() < self.block_probability:
            return 'retreat'
        
        # Random attack choice
        if random.random() < self.attack_probability:
            # Choose attack type based on difficulty
            if random.random() < self.combo_probability:
                return 'special'
            else:
                return random.choice(['light', 'heavy', 'kick'])
        
        # Sometimes jump over opponent
        if random.random() < 0.2:
            return 'jump'
        
        return 'approach'
    
    def _decide_medium_range(self, ai_fighter, opponent):
        """Decide action at medium range"""
        # Approach for attack
        if random.random() < self.attack_probability * 0.7:
            return 'approach'
        
        # Or attempt long-range attack
        if random.random() < 0.3:
            return 'kick'
        
        return 'approach'
    
    def _execute_current_action(self, ai_fighter, opponent):
        """
        Execute the current action and return simulated keys
        
        Returns:
            Dictionary mapping control keys to their pressed state
        """
        keys = {
            'left': False,
            'right': False,
            'jump': False,
            'light': False,
            'heavy': False,
            'kick': False,
            'special': False
        }
        
        if self.current_action == 'stunned':
            return keys
        
        # Movement
        if self.current_action == 'approach':
            if ai_fighter.rect.centerx < opponent.rect.centerx:
                keys['right'] = True
            else:
                keys['left'] = True
        
        elif self.current_action == 'retreat':
            if ai_fighter.rect.centerx < opponent.rect.centerx:
                keys['left'] = True
            else:
                keys['right'] = True
        
        elif self.current_action == 'jump':
            keys['jump'] = True
            # Continue moving toward opponent while jumping
            if ai_fighter.rect.centerx < opponent.rect.centerx:
                keys['right'] = True
            else:
                keys['left'] = True
        
        # Attacks
        elif self.current_action == 'light':
            keys['light'] = True
        
        elif self.current_action == 'heavy':
            keys['heavy'] = True
        
        elif self.current_action == 'kick':
            keys['kick'] = True
        
        elif self.current_action == 'special':
            keys['special'] = True
        
        return keys
    
    def apply_to_fighter(self, ai_fighter, opponent, screen_width, screen_height):
        """
        Apply AI control to a fighter by simulating key presses
        
        Args:
            ai_fighter: Fighter to control
            opponent: Opponent fighter
            screen_width: Screen width
            screen_height: Screen height
        """
        # Get AI decision
        ai_keys = self.update(ai_fighter, opponent, screen_width, screen_height)
        
        # Simulate pressing keys
        # Note: This modifies the pygame key state temporarily
        # In practice, you'd integrate this directly into the Fighter's move() method
        
        return ai_keys
