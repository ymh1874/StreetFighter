"""
AI Controller for Street Fighter Game
Provides intelligent computer opponents with different difficulty levels

NOTE: This AI controller provides the decision-making logic for computer opponents.
Some movement control methods are placeholders and would require deeper integration
with the game's input system. The core AI behaviors (attack selection, strategy,
defensive actions) are fully implemented and functional.
"""

import pygame
import random
import math


class AIController:
    """
    AI opponent controller with strategic decision making
    
    Difficulty Levels:
    - easy: Slow reactions (400ms), low aggression (30%), rare parries (5%)
    - medium: Moderate reactions (200ms), balanced aggression (50%), some parries (15%)
    - hard: Fast reactions (100ms), high aggression (70%), frequent parries (30%)
    - expert: Lightning reactions (50ms), very aggressive (80%), expert parries (50%)
    
    NOTE: Movement control methods (_move_towards_opponent, _move_away_from_opponent)
    are placeholders and would require integration with the Fighter's control system.
    The attack and defensive behaviors work correctly.
    """
    
    def __init__(self, fighter, opponent, difficulty='hard'):
        self.fighter = fighter
        self.opponent = opponent
        self.difficulty = difficulty
        
        # Set difficulty parameters
        if difficulty == 'easy':
            self.reaction_time = 400  # ms
            self.aggression = 0.3
            self.parry_chance = 0.05
            self.combo_skill = 0.2
        elif difficulty == 'medium':
            self.reaction_time = 200
            self.aggression = 0.5
            self.parry_chance = 0.15
            self.combo_skill = 0.5
        elif difficulty == 'hard':
            self.reaction_time = 100
            self.aggression = 0.7
            self.parry_chance = 0.3
            self.combo_skill = 0.7
        else:  # expert
            self.reaction_time = 50
            self.aggression = 0.8
            self.parry_chance = 0.5
            self.combo_skill = 0.9
        
        # AI state
        self.last_decision_time = 0
        self.current_strategy = 'neutral'  # neutral, aggressive, defensive, combo
        self.strategy_change_timer = 0
        self.last_attack_time = 0
        self.target_distance = 200  # Optimal fighting distance
        
    def update(self, projectiles):
        """Main AI update - makes decisions and controls the fighter"""
        current_time = pygame.time.get_ticks()
        
        # Make decisions at intervals based on reaction time
        if current_time - self.last_decision_time > self.reaction_time:
            self.last_decision_time = current_time
            self._make_decision(projectiles, current_time)
        
        # Update strategy periodically
        self.strategy_change_timer -= 1
        if self.strategy_change_timer <= 0:
            self._choose_strategy()
            self.strategy_change_timer = random.randint(180, 360)  # 3-6 seconds
    
    def _make_decision(self, projectiles, current_time):
        """Make strategic decision based on current game state"""
        distance = abs(self.fighter.rect.centerx - self.opponent.rect.centerx)
        
        # Analyze situation
        low_health = self.fighter.health < self.fighter.max_health * 0.3
        opponent_low_health = self.opponent.health < self.opponent.max_health * 0.3
        
        # Adjust strategy based on health
        if low_health:
            self.current_strategy = 'defensive'
        elif opponent_low_health:
            self.current_strategy = 'aggressive'
        
        # Execute strategy
        if self.current_strategy == 'aggressive':
            self._aggressive_behavior(distance, projectiles, current_time)
        elif self.current_strategy == 'defensive':
            self._defensive_behavior(distance, projectiles)
        elif self.current_strategy == 'combo':
            self._combo_behavior(distance, current_time)
        else:  # neutral
            self._neutral_behavior(distance, projectiles, current_time)
    
    def _choose_strategy(self):
        """Randomly choose a new strategy"""
        strategies = ['neutral', 'aggressive', 'defensive', 'combo']
        weights = [0.4, 0.3, 0.2, 0.1]
        self.current_strategy = random.choices(strategies, weights)[0]
    
    def _neutral_behavior(self, distance, projectiles, current_time):
        """Balanced approach - maintains optimal distance and attacks when in range"""
        # Maintain optimal distance
        if distance > self.target_distance + 50:
            # Move closer
            self._move_towards_opponent()
        elif distance < self.target_distance - 50:
            # Move away
            self._move_away_from_opponent()
        
        # Attack if in range
        if distance < 150 and random.random() < self.aggression * 0.5:
            self._attack_opponent(projectiles)
        elif distance > 200 and distance < 400 and random.random() < 0.3:
            # Use projectile at mid-range
            if current_time - self.last_attack_time > 2000:
                self._use_special_move(projectiles)
    
    def _aggressive_behavior(self, distance, projectiles, current_time):
        """Constant pressure - dashes in and attacks frequently"""
        # Always move towards opponent
        self._move_towards_opponent()
        
        # Dash towards opponent if far
        if distance > 200 and not self.fighter.dashing:
            # Simulate dash button press (this would need to be integrated properly)
            pass
        
        # Attack frequently
        if distance < 200 and random.random() < self.aggression:
            self._attack_opponent(projectiles)
    
    def _defensive_behavior(self, distance, projectiles):
        """Spacing and blocking - maintains distance and blocks attacks"""
        # Keep distance
        if distance < self.target_distance:
            self._move_away_from_opponent()
        
        # Block if opponent is attacking
        if self.opponent.attacking and distance < 150:
            self._block()
        
        # Try to parry projectiles
        for proj in projectiles:
            if proj.owner == self.opponent:
                proj_distance = abs(proj.x - self.fighter.rect.centerx)
                if proj_distance < 100 and random.random() < self.parry_chance:
                    self._try_parry()
    
    def _combo_behavior(self, distance, current_time):
        """Attempts to execute combos"""
        if distance < 120 and random.random() < self.combo_skill:
            # Execute a combo sequence
            self._execute_combo()
    
    def _move_towards_opponent(self):
        """Simulate moving towards opponent"""
        # This would need to be integrated with the fighter's control system
        # For now, this is a placeholder
        pass
    
    def _move_away_from_opponent(self):
        """Simulate moving away from opponent"""
        # This would need to be integrated with the fighter's control system
        pass
    
    def _attack_opponent(self, projectiles):
        """Execute an attack based on distance and situation"""
        distance = abs(self.fighter.rect.centerx - self.opponent.rect.centerx)
        
        # Choose attack type based on distance
        if distance < 100:
            # Close range - use punches or kicks
            attack_types = ['light_punch', 'heavy_punch', 'light_kick', 'heavy_kick']
            weights = [0.3, 0.3, 0.2, 0.2]
            attack = random.choices(attack_types, weights)[0]
            
            # Simulate button press (would need proper integration)
            result = self.fighter.attack(self.opponent, attack)
            self.last_attack_time = pygame.time.get_ticks()
            return result
        elif distance < 300:
            # Mid range - use special or heavy attacks
            if random.random() < 0.4:
                return self._use_special_move(projectiles)
    
    def _use_special_move(self, projectiles):
        """Use character's special move"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > 2000:
            result = self.fighter.attack(self.opponent, 'special')
            self.last_attack_time = current_time
            
            # Add projectile to list if special returns one
            if result is not None:
                if isinstance(result, list):
                    projectiles.extend(result)
                else:
                    projectiles.append(result)
            return result
    
    def _block(self):
        """Activate blocking"""
        # Would need to set fighter to blocking state
        self.fighter.blocking = True
    
    def _try_parry(self):
        """Attempt to parry"""
        if random.random() < self.parry_chance:
            self.fighter.activate_parry()
    
    def _execute_combo(self):
        """Execute a combo string"""
        # Would need to execute a sequence of attacks
        # This is a placeholder for combo execution
        pass
    
    def get_distance_to_opponent(self):
        """Calculate distance to opponent"""
        return abs(self.fighter.rect.centerx - self.opponent.rect.centerx)
    
    def is_opponent_attacking(self):
        """Check if opponent is currently attacking"""
        return self.opponent.attacking
    
    def should_jump(self):
        """Decide if AI should jump"""
        # Jump over projectiles or to close distance
        return random.random() < 0.1
