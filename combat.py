"""
Combat system for Professor Fighting Game
Handles frame data, combos, and attack mechanics
"""

import pygame
import config as c


class CombatSystem:
    """Manages combat mechanics including combos and frame data"""
    
    def __init__(self):
        self.combo_hits = {}  # Track combo hits per fighter
        
    def register_fighter(self, fighter_id):
        """Register a fighter for combo tracking"""
        self.combo_hits[fighter_id] = 0
        
    def reset_combo(self, fighter_id):
        """Reset combo counter for a fighter"""
        self.combo_hits[fighter_id] = 0
        
    def increment_combo(self, fighter_id):
        """Increment combo counter"""
        self.combo_hits[fighter_id] += 1
        
        # Auto-break combo after max hits
        if self.combo_hits[fighter_id] > c.MAX_COMBO_HITS:
            self.reset_combo(fighter_id)
            return False  # Combo broken
        return True  # Combo continues
    
    def get_combo_damage_multiplier(self, fighter_id):
        """Get damage multiplier based on current combo count"""
        hits = self.combo_hits.get(fighter_id, 0)
        return c.COMBO_DAMAGE_SCALING.get(hits, 1.0)
    
    def get_combo_count(self, fighter_id):
        """Get current combo count"""
        return self.combo_hits.get(fighter_id, 0)


class AttackBuffer:
    """
    Input buffering system for smooth attack canceling
    Allows queuing next attack during current attack
    """
    
    def __init__(self, buffer_window=5):
        """
        Initialize attack buffer
        
        Args:
            buffer_window: Number of frames to buffer input
        """
        self.buffer_window = buffer_window
        self.buffered_attacks = {}
        
    def buffer_attack(self, fighter_id, attack_type, timestamp):
        """Buffer an attack input"""
        self.buffered_attacks[fighter_id] = {
            'type': attack_type,
            'timestamp': timestamp
        }
        
    def get_buffered_attack(self, fighter_id, current_time):
        """Get buffered attack if within window"""
        if fighter_id not in self.buffered_attacks:
            return None
            
        buffered = self.buffered_attacks[fighter_id]
        time_diff = current_time - buffered['timestamp']
        
        # Check if within buffer window (convert frames to ms at 60fps)
        if time_diff <= (self.buffer_window * 1000 / 60):
            # Clear buffer and return attack
            attack_type = buffered['type']
            del self.buffered_attacks[fighter_id]
            return attack_type
            
        # Buffer expired
        if time_diff > (self.buffer_window * 1000 / 60):
            del self.buffered_attacks[fighter_id]
        
        return None
    
    def clear_buffer(self, fighter_id):
        """Clear buffered attack"""
        if fighter_id in self.buffered_attacks:
            del self.buffered_attacks[fighter_id]


class FrameData:
    """
    Manages attack frame data and recovery
    Determines when a fighter can move based on attack state
    """
    
    @staticmethod
    def can_move_during_attack(attack_type, frames_elapsed):
        """
        Determine if fighter can move during attack
        
        Args:
            attack_type: Type of attack being performed
            frames_elapsed: Frames since attack started
            
        Returns:
            True if fighter can move, False otherwise
        """
        if attack_type not in c.FRAME_DATA:
            return True
        
        data = c.FRAME_DATA[attack_type]
        
        # Light attacks can move after active frames
        if data.get('can_move_early', False):
            active_end = data['startup'] + data['active']
            return frames_elapsed >= active_end
        
        # Heavy attacks must complete full recovery
        return frames_elapsed >= data['total']
    
    @staticmethod
    def get_attack_duration(attack_type):
        """Get total duration of attack in frames"""
        if attack_type not in c.FRAME_DATA:
            return 10  # Default
        return c.FRAME_DATA[attack_type]['total']
    
    @staticmethod
    def is_in_active_frames(attack_type, frames_elapsed):
        """Check if attack is in active (hitting) frames"""
        if attack_type not in c.FRAME_DATA:
            return False
        
        data = c.FRAME_DATA[attack_type]
        startup = data['startup']
        active_end = startup + data['active']
        
        return startup <= frames_elapsed < active_end


class SpecialMoveData:
    """Data for special moves"""
    
    # Khalid's Spinning Kick
    SPINNING_KICK = {
        'name': 'Spinning Kick',
        'damage_per_hit': 8,
        'num_hits': 3,
        'forward_movement': 150,  # pixels
        'rotations': 3,
        'cooldown': 2000,
        'duration': 60  # frames
    }
    
    # Eduardo's Pizza Throw
    PIZZA_THROW = {
        'name': 'Pizza Throw',
        'damage_per_slice': 6,
        'num_slices': 3,
        'speed': 5,  # pixels per frame
        'cooldown': 2000,
        'slice_delay': 5  # frames between slices
    }
    
    # Hasan's Fireball
    FIREBALL = {
        'name': 'Fireball',
        'damage': 15,
        'speed': 8,  # pixels per frame
        'amplitude': 30,  # sine wave amplitude
        'wavelength': 50,  # sine wave wavelength
        'cooldown': 2000
    }
    
    # Hammoud's Circuit Board
    CIRCUIT_BOARD = {
        'name': 'Circuit Board',
        'damage': 20,
        'speed': 4,  # pixels per frame
        'homing_strength': 0.05,  # radians per frame
        'cooldown': 2000
    }


def calculate_knockback_velocity(attacker_facing_right, knockback_strength):
    """
    Calculate knockback velocity vector
    
    Args:
        attacker_facing_right: Direction attacker is facing
        knockback_strength: Base knockback strength
        
    Returns:
        (vel_x, vel_y) velocity tuple
    """
    direction = 1 if attacker_facing_right else -1
    vel_x = knockback_strength * direction * 2
    vel_y = -5  # Slight upward knock
    
    return vel_x, vel_y


def check_combo_string(attack_history, combo_string):
    """
    Check if attack history matches a combo string
    
    Args:
        attack_history: List of recent attacks
        combo_string: List of attacks that form combo
        
    Returns:
        True if combo matches, False otherwise
    """
    if len(attack_history) < len(combo_string):
        return False
    
    # Check last N attacks match combo
    recent = attack_history[-len(combo_string):]
    return recent == combo_string


# Character-specific combo definitions
# NOTE: These combo strings are defined for future enhancement
# They can be implemented to provide bonus damage when specific attack sequences are performed
COMBO_STRINGS = {
    'PROF. KHALID': {
        'tornado_kick': {
            'inputs': ['light_kick', 'light_kick', 'heavy_kick'],
            'bonus_damage': 0.3,
            'name': 'TORNADO KICK'
        },
        'flying_axe': {
            'inputs': ['jump', 'heavy_kick'],
            'bonus_damage': 0.3,
            'name': 'FLYING AXE KICK'
        }
    },
    'PROF. EDUARDO': {
        'pizza_barrage': {
            'inputs': ['light_punch', 'light_punch', 'special'],
            'bonus_damage': 0.3,
            'name': 'PIZZA BARRAGE'
        },
        'mega_slice': {
            'inputs': ['heavy_punch', 'special'],
            'bonus_damage': 0.3,
            'name': 'MEGA SLICE'
        }
    },
    'PROF. HASAN': {
        'flame_uppercut': {
            'inputs': ['light_kick', 'heavy_punch', 'special'],
            'bonus_damage': 0.3,
            'name': 'FLAME UPPERCUT'
        }
    },
    'PROF. HAMMOUD': {
        'binary_rush': {
            'inputs': ['light_punch', 'light_punch', 'light_kick', 'heavy_kick'],
            'bonus_damage': 0.3,
            'name': 'BINARY RUSH'
        }
    }
}
