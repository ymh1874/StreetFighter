import pygame
import math
import config as c
from combat import FrameData, CombatSystem, SpecialMoveData
import drawing

class Particle:
    """Simple hit particle effect"""
    def __init__(self, x, y, color, velocity):
        self.x = x
        self.y = y
        self.color = color
        self.vel_x = velocity[0]
        self.vel_y = velocity[1]
        self.timer = 20

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.5
        self.timer -= 1

    def draw(self, surface):
        if self.timer > 0:
            pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), 4, 4))


class Projectile:
    """Base projectile class"""
    def __init__(self, x, y, damage, vel_x, vel_y, owner):
        self.x = x
        self.y = y
        self.damage = damage
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.owner = owner  # Fighter who shot it
        self.active = True
        self.frame = 0
        
    def update(self):
        """Update projectile position"""
        self.x += self.vel_x
        self.y += self.vel_y
        self.frame += 1
        
        # Deactivate if off screen
        if self.x < -50 or self.x > c.SCREEN_WIDTH + 50:
            self.active = False
        if self.y < -50 or self.y > c.SCREEN_HEIGHT + 50:
            self.active = False
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x - 10, self.y - 10, 20, 20)
    
    def draw(self, surface):
        """Override in subclass"""
        pass


class PizzaSlice(Projectile):
    """Eduardo's pizza slice projectile"""
    def __init__(self, x, y, vel_x, vel_y, owner, delay=0):
        super().__init__(x, y, 6, vel_x, vel_y, owner)
        self.rotation = 0
        self.delay = delay  # Delay before becoming active
        self.gravity = 0.2
        
    def update(self):
        # Wait for delay
        if self.delay > 0:
            self.delay -= 1
            self.frame += 1
            return
            
        # Parabolic arc
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += self.gravity
        
        # Rotation
        self.rotation = (self.rotation + 15) % 360
        self.frame += 1
        
        # Deactivate if off screen
        if self.x < -50 or self.x > c.SCREEN_WIDTH + 50:
            self.active = False
        if self.y > c.SCREEN_HEIGHT + 50:
            self.active = False
    
    def draw(self, surface):
        import drawing
        if self.delay <= 0:  # Only draw if active
            drawing.draw_pizza_slice(surface, self.x, self.y, self.rotation)


class SineWaveFireball(Projectile):
    """Hasan's sine wave fireball"""
    def __init__(self, x, y, direction, owner):
        speed = 8
        vel_x = speed * direction
        super().__init__(x, y, 15, vel_x, 0, owner)
        self.start_y = y
        self.distance_traveled = 0
        self.amplitude = 30
        self.wavelength = 50
        
    def update(self):
        # Horizontal movement
        self.x += self.vel_x
        self.distance_traveled += abs(self.vel_x)
        
        # Vertical oscillation (sine wave)
        self.y = self.start_y + self.amplitude * math.sin(self.distance_traveled / self.wavelength)
        
        self.frame += 1
        
        # Deactivate if off screen
        if self.x < -50 or self.x > c.SCREEN_WIDTH + 50:
            self.active = False
    
    def draw(self, surface):
        import drawing
        drawing.draw_fireball(surface, self.x, self.y, self.frame)


class HomingCircuitBoard(Projectile):
    """Hammoud's homing circuit board"""
    def __init__(self, x, y, direction, owner, target):
        speed = 4
        vel_x = speed * direction
        super().__init__(x, y, 20, vel_x, 0, owner)
        self.target = target
        self.homing_strength = 0.05
        
    def update(self):
        # Calculate angle to target
        if self.target and self.target.alive:
            dx = self.target.rect.centerx - self.x
            dy = self.target.rect.centery - self.y
            target_angle = math.atan2(dy, dx)
            
            # Current angle
            current_angle = math.atan2(self.vel_y, self.vel_x)
            
            # Gradually adjust toward target
            angle_diff = target_angle - current_angle
            # Normalize angle difference to [-pi, pi]
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi
            
            # Apply correction (limited turning speed)
            correction = max(-self.homing_strength, min(self.homing_strength, angle_diff))
            new_angle = current_angle + correction
            
            # Update velocity
            speed = 4
            self.vel_x = speed * math.cos(new_angle)
            self.vel_y = speed * math.sin(new_angle)
        
        # Move
        self.x += self.vel_x
        self.y += self.vel_y
        self.frame += 1
        
        # Deactivate if off screen
        if self.x < -50 or self.x > c.SCREEN_WIDTH + 50:
            self.active = False
        if self.y < -50 or self.y > c.SCREEN_HEIGHT + 50:
            self.active = False
    
    def draw(self, surface):
        import drawing
        drawing.draw_circuit_board(surface, self.x, self.y, self.frame)


class SpinningKickEffect:
    """Visual effect for Khalid's spinning kick"""
    def __init__(self, fighter, duration=60):
        self.fighter = fighter
        self.duration = duration
        self.frame = 0
        self.active = True
        self.start_x = fighter.rect.x
        self.hits_dealt = 0
        self.hit_cooldown = 0
        
    def update(self):
        self.frame += 1
        if self.frame >= self.duration:
            self.active = False
            
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1
        
        # Move fighter forward
        direction = 1 if self.fighter.facing_right else -1
        move_per_frame = 150 / 60  # Total movement / duration
        self.fighter.rect.x += move_per_frame * direction
    
    def get_rotation_angle(self):
        """Get current rotation angle for visual"""
        # 3 full rotations over duration
        progress = self.frame / self.duration
        return progress * 360 * 3
    
    def can_hit(self):
        """Check if can deal another hit"""
        return self.hits_dealt < 3 and self.hit_cooldown <= 0
    
    def register_hit(self):
        """Register that a hit was dealt"""
        self.hits_dealt += 1
        self.hit_cooldown = 20  # 20 frames between hits


class HitEffect:
    """Comic book style hit effect"""
    def __init__(self, x, y, effect_type='light', color=None):
        self.x = x
        self.y = y
        self.effect_type = effect_type
        self.color = color or c.YELLOW
        self.frame = 0
        self.duration = 15
        self.active = True
        
        # Text based on effect type
        if effect_type == 'light':
            self.text = "POW!"
        elif effect_type == 'heavy':
            self.text = "BOOM!"
        elif effect_type == 'special':
            self.text = "WHAM!"
        elif effect_type == 'ko':
            self.text = "K.O!"
        else:
            self.text = "HIT!"
    
    def update(self):
        self.frame += 1
        if self.frame >= self.duration:
            self.active = False
    
    def draw(self, surface, text_renderer):
        if not self.active:
            return
        
        # Draw starburst background
        import drawing
        drawing.draw_hit_effect(surface, int(self.x), int(self.y), 
                              self.effect_type, self.color, self.frame)
        
        # Draw text
        scale = 1.0 + (self.duration - self.frame) * 0.05  # Shrink over time
        alpha = int(255 * (1.0 - self.frame / self.duration))  # Fade out
        
        text_surf = text_renderer.render(self.text, 'medium', self.color)
        text_x = int(self.x - text_surf.get_width() // 2)
        text_y = int(self.y - text_surf.get_height() // 2)
        
        # Apply fade (simple version - draw with alpha)
        if alpha < 255:
            text_surf.set_alpha(alpha)
        
        surface.blit(text_surf, (text_x, text_y))

class Attack:
    def __init__(self, name, damage, cooldown, hitbox_w, hitbox_h, knockback, stun):
        self.name = name
        self.damage = damage
        self.cooldown = cooldown 
        self.width = hitbox_w
        self.height = hitbox_h
        self.knockback = knockback
        self.stun = stun 

class Fighter:
    def __init__(self, x, y, stats, controls, is_p2=False, combat_system=None, fighter_id=None, joy_input_getter=None):
        self.rect = pygame.Rect(x, y, c.P_WIDTH, c.P_HEIGHT)
        self.stats = stats
        self.color = stats['color']
        self.controls = controls 
        self.is_p2 = is_p2
        self.combat_system = combat_system  # Reference to combat system for combo tracking
        self.fighter_id = fighter_id  # "p1" or "p2" for combo tracking
        self.joy_input_getter = joy_input_getter  # Function to get joystick input state
        
        # Physics from stats
        self.speed = stats['speed']
        self.jump_force = stats['jump']
        self.max_health = stats['health']
        self.health = self.max_health
        self.dmg_mult = stats['dmg_mult']
        
        # Movement State
        self.vel_y = 0
        self.jumping = False
        self.facing_right = not is_p2
        self.alive = True
        
        # Combat State
        self.attacking = False
        self.attack_type = None
        self.attack_cooldown = 0
        self.hit_stun = 0
        self.last_attack_time = 0
        self.attack_start_frame = 0
        self.attack_rect = None
        self.color_flash = 0
        self.animation_state = 'idle'
        self.animation_frame = 0
        self.special_move_cooldown = 0

        self.last_special_time = -6000  # Initialize to -6000 to allow immediate special move use
        
        # Dash State
        self.dashing = False
        self.dash_timer = 0
        self.dash_cooldown = 0
        self.last_dash_time = 0
        
        # Parry State
        self.parrying = False
        self.parry_window = 0  # Frame counter for 6-frame parry window
        self.parry_success = False
        self.parry_cooldown = 0
        
        # Block State
        self.blocking = False
        self.block_start_time = 0  # Track when block started
        self.block_usage_count = 0  # Track how many times block has been used in current session
        self.block_damage_reduction = 1.0  # Start at 100% reduction (1.0 = block all damage)
        
        # Attack history for combos
        self.attack_history = []

        # Attack Definitions
        self.moves = {
            'light_punch': Attack('Light Punch', 5 * self.dmg_mult, 300, 60, 20, 5, 10),
            'heavy_punch': Attack('Heavy Punch', 12 * self.dmg_mult, 700, 70, 40, 15, 20),
            'light_kick': Attack('Light Kick', 8 * self.dmg_mult, 500, 80, 30, 10, 15),
            'heavy_kick': Attack('Heavy Kick', 15 * self.dmg_mult, 900, 90, 40, 20, 25),
            'special': Attack('Special', 20 * self.dmg_mult, 2000, 120, 60, 25, 30)
        }

    def can_move(self):
        """Determine if fighter can move based on current state"""
        if not self.attacking:
            return True
        
        # Check frame data
        current_time = pygame.time.get_ticks()
        frames_elapsed = (current_time - self.attack_start_frame) / (1000 / 60)  # Convert to frames
        
        return FrameData.can_move_during_attack(self.attack_type, frames_elapsed)
    
    def is_action_pressed(self, action):
        """
        Check if an action is currently pressed via keyboard or joystick.
        
        Args:
            action: Action name ('left', 'right', 'jump', 'light_punch', etc.)
            
        Returns:
            True if the action is currently triggered
        """
        # Check keyboard
        key = pygame.key.get_pressed()
        if action in self.controls and key[self.controls[action]]:
            return True
        
        # Check joystick via the getter function
        if self.joy_input_getter:
            joystick_id = 1 if self.is_p2 else 0
            if self.joy_input_getter(action, joystick_id):
                return True
        
        return False
    
    def move(self, target, width, height):
        dx = 0
        dy = 0
        
        # Hit Stun / Gravity
        if self.hit_stun > 0:
            self.hit_stun -= 1
            self.vel_y += c.GRAVITY
            dy += self.vel_y
            if self.rect.bottom + dy > c.FLOOR_Y:
                dy = c.FLOOR_Y - self.rect.bottom
                self.vel_y = 0
            self.rect.x += dx 
            self.rect.y += dy
            if self.rect.left < 0: self.rect.left = 0
            if self.rect.right > width: self.rect.right = width
            return

        # Dash handling - now works in mid-air too
        current_time = pygame.time.get_ticks()
        if self.is_action_pressed('dash') and not self.dashing and current_time - self.last_dash_time > 500:
            self.dashing = True
            self.dash_timer = c.FRAME_DATA['dash']['active']  # 8 frames
            self.last_dash_time = current_time
            self.animation_state = 'dash'
        
        # Update dash
        if self.dashing:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.dashing = False
                self.animation_state = 'idle'
            else:
                # Fast movement during dash
                dash_speed = self.speed * 2.5
                dx = dash_speed if self.facing_right else -dash_speed

        # Input Handling - can move during light attacks (but not during dash)
        if self.can_move() and not self.dashing:
            if self.is_action_pressed('left'):
                dx = -self.speed
                self.facing_right = False
            if self.is_action_pressed('right'):
                dx = self.speed
                self.facing_right = True
            
            if self.is_action_pressed('jump') and not self.jumping:
                self.vel_y = self.jump_force
                self.jumping = True

        # Gravity
        self.vel_y += c.GRAVITY
        dy += self.vel_y

        # Floor Collision
        if self.rect.bottom + dy > c.FLOOR_Y:
            dy = c.FLOOR_Y - self.rect.bottom
            self.vel_y = 0
            self.jumping = False

        # Screen Bounds
        if self.rect.left + dx < 0: dx = -self.rect.left
        if self.rect.right + dx > width: dx = width - self.rect.right

        # Block handling (hold down to block)
        # Block can only last max duration and effectiveness degrades
        current_time = pygame.time.get_ticks()
        if self.is_action_pressed('down') and not self.jumping and not self.attacking:
            if not self.blocking:
                # Starting a new block
                self.blocking = True
                self.block_start_time = current_time
                self.animation_state = 'block'
                # Update block damage reduction based on usage count using config
                usage_idx = min(self.block_usage_count, len(c.BLOCK_EFFECTIVENESS_LEVELS) - 1)
                self.block_damage_reduction = c.BLOCK_EFFECTIVENESS_LEVELS[usage_idx]
            else:
                # Already blocking - check if max duration has passed
                if current_time - self.block_start_time > c.BLOCK_DURATION_MS:
                    self.blocking = False
                    self.animation_state = 'idle'
                    self.block_usage_count += 1
        else:
            if self.blocking:
                # Released block button
                self.blocking = False
                self.animation_state = 'idle'
                self.block_usage_count += 1
        
        # Parry handling (tap down quickly for parry)
        # Update parry window
        if self.parry_window > 0:
            self.parry_window -= 1
            if self.parry_window == 0:
                self.parrying = False

        # Attacks - can't attack while blocking
        current_time = pygame.time.get_ticks()
        if not self.attacking and not self.blocking and current_time - self.last_attack_time > self.attack_cooldown:
            attack_key = None
            # PRIORITY: Parry > Special > Heavy Kick > Heavy Punch > Light Kick > Light Punch
            if self.is_action_pressed('parry'):
                # Activate parry
                self.activate_parry()
            elif self.is_action_pressed('special'): 
                attack_key = 'special'
            elif self.is_action_pressed('heavy_kick'): 
                attack_key = 'heavy_kick'
            elif self.is_action_pressed('heavy_punch'): 
                attack_key = 'heavy_punch'
            elif self.is_action_pressed('light_kick'): 
                attack_key = 'light_kick'
            elif self.is_action_pressed('light_punch'): 
                attack_key = 'light_punch'

            if attack_key:
                return_val = self.attack(target, attack_key)
                if return_val is not None:  # Special move returned projectile
                    return return_val

        self.rect.x += dx
        self.rect.y += dy
        return None

    def attack(self, target, type_key):
        self.attacking = True
        move_data = self.moves.get(type_key)
        if not move_data:
            return None
            
        self.attack_type = type_key
        self.last_attack_time = pygame.time.get_ticks()
        self.attack_start_frame = self.last_attack_time
        self.attack_cooldown = move_data.cooldown
        self.animation_state = type_key
        
        # Add to attack history for combos
        self.attack_history.append(type_key)
        if len(self.attack_history) > 10:
            self.attack_history.pop(0)
        
        # Handle special moves separately
        if type_key == 'special':
            current_time = pygame.time.get_ticks()
            if current_time - self.last_special_time >= 4000:
                self.last_special_time = current_time
                return self.execute_special_move(target)
            else:
                self.attacking = False
                return None
        
        # Regular attacks
        hitbox_x = self.rect.right if self.facing_right else self.rect.left - move_data.width
        # Center hitbox vertically on character (was +10, now centered)
        hitbox_y = self.rect.y + (self.rect.height - move_data.height) // 2
        
        self.attack_rect = pygame.Rect(hitbox_x, hitbox_y, move_data.width, move_data.height)
        
        if self.attack_rect.colliderect(target.rect):
            # Apply combo damage scaling if combat system is available
            damage = move_data.damage
            if self.combat_system and self.fighter_id:
                # Increment combo first, then get multiplier for this hit
                self.combat_system.increment_combo(self.fighter_id)
                combo_multiplier = self.combat_system.get_combo_damage_multiplier(self.fighter_id)
                damage *= combo_multiplier
            
            target.take_damage(damage, move_data.knockback, move_data.stun, self.facing_right)
            return True 
        return False
    
    def execute_special_move(self, target):
        """Execute character-specific special move"""
        special_type = self.stats.get('special', '')
        direction = 1 if self.facing_right else -1
        
        if special_type == 'spinning_kick':
            # Khalid's spinning kick - returns effect object
            return SpinningKickEffect(self, duration=60)
        
        elif special_type == 'pizza_throw':
            # Eduardo's pizza throw - returns 3 projectiles
            projectiles = []
            start_x = self.rect.right if self.facing_right else self.rect.left
            start_y = self.rect.centery
            
            for i in range(3):
                vel_x = 5 * direction
                vel_y = -8 + i * 2  # Slightly different trajectories
                pizza = PizzaSlice(start_x, start_y, vel_x, vel_y, self, delay=i * 5)
                projectiles.append(pizza)
            
            return projectiles
        
        elif special_type == 'fireball':
            # Hasan's fireball
            start_x = self.rect.right if self.facing_right else self.rect.left
            start_y = self.rect.centery
            return SineWaveFireball(start_x, start_y, direction, self)
        
        elif special_type == 'circuit_board':
            # Hammoud's homing circuit board
            start_x = self.rect.right if self.facing_right else self.rect.left
            start_y = self.rect.centery
            return HomingCircuitBoard(start_x, start_y, direction, self, target)
        
        return None 

    def take_damage(self, amount, knockback, stun, attacker_facing_right):
        # Check if blocking
        if self.blocking:
            # Apply damage reduction: 1.0 = 100% blocked (0% damage taken), 0.5 = 50% blocked (50% damage taken), etc.
            amount *= (1.0 - self.block_damage_reduction)
            knockback *= 0.5  # Reduce knockback
            stun = int(stun * 0.3)  # Reduce stun
        
        # Check if parrying (within parry window)
        if self.parrying and self.parry_window > 0:
            # Successful parry! No damage taken
            self.parry_success = True
            self.color_flash = 10  # Longer flash for parry
            return True  # Return True to indicate parry success
        
        self.health -= amount
        self.hit_stun = stun
        self.attacking = False 
        self.blocking = False  # Stop blocking when hit
        self.color_flash = 5 
        
        # Reset this fighter's combo when taking damage
        if self.combat_system and self.fighter_id:
            self.combat_system.reset_combo(self.fighter_id)
        
        direction = 1 if attacker_facing_right else -1
        self.rect.x += knockback * direction * 2 
        
        if self.health <= 0:
            self.health = 0
            self.alive = False
        
        return False  # Return False to indicate normal damage taken
    
    def activate_parry(self):
        """Activate parry with 6-frame window
        
        Can be activated while blocking (as an enhanced defensive option)
        but not while attacking.
        Cooldown is 5 seconds (300 frames at 60fps).
        """
        if not self.attacking and self.parry_cooldown <= 0:
            self.parrying = True
            self.parry_window = c.PARRY_WINDOW_FRAMES
            self.parry_success = False
            self.parry_cooldown = c.PARRY_COOLDOWN_FRAMES
            self.animation_state = 'block'  # Use block animation for parry
            return True
        return False

    def update(self):
        if self.attacking:
            # Use frame data for attack duration
            current_time = pygame.time.get_ticks()
            frames_elapsed = (current_time - self.attack_start_frame) / (1000 / 60)
            
            duration = FrameData.get_attack_duration(self.attack_type)
            if frames_elapsed >= duration:
                self.attacking = False
                self.attack_rect = None
                self.animation_state = 'idle'

        if self.color_flash > 0:
            self.color_flash -= 1
        
        # Update parry cooldown
        if self.parry_cooldown > 0:
            self.parry_cooldown -= 1
        
        self.animation_frame += 1

    def draw(self, surface):
        # Shadow
        pygame.draw.ellipse(surface, (20,20,20), (self.rect.centerx - 25, c.FLOOR_Y - 10, 50, 20))
        
        # Draw dash particles if dashing
        if self.dashing:
            drawing.draw_dash_particles(surface, self.rect.centerx, self.rect.centery, 
                                       self.facing_right, self.animation_frame)
        
        # Draw character based on professor type
        char_name = self.stats.get('name', '')
        
        if 'KHALID' in char_name:
            drawing.draw_khalid(surface, self.rect.centerx, self.rect.bottom, 
                              self.facing_right, self.animation_state, self.animation_frame)
        elif 'EDUARDO' in char_name:
            drawing.draw_eduardo(surface, self.rect.centerx, self.rect.bottom, 
                               self.facing_right, self.animation_state, self.animation_frame)
        elif 'HASAN' in char_name:
            drawing.draw_hasan(surface, self.rect.centerx, self.rect.bottom, 
                             self.facing_right, self.animation_state, self.animation_frame)
        elif 'HAMMOUD' in char_name:
            drawing.draw_hammoud(surface, self.rect.centerx, self.rect.bottom, 
                                self.facing_right, self.animation_state, self.animation_frame)
        else:
            # Fallback to simple rectangle
            color = c.WHITE if self.color_flash > 0 else self.color
            pygame.draw.rect(surface, color, self.rect)
            eye_x = self.rect.right - 15 if self.facing_right else self.rect.left + 5
            pygame.draw.rect(surface, c.BLACK, (eye_x, self.rect.y + 15, 10, 5))
        
        # Draw transparent shield when blocking
        if self.blocking:
            # Calculate pulsing alpha (optimized - avoid creating surface every frame)
            pulse = math.sin(self.animation_frame * 0.3)
            alpha = int(80 + 40 * pulse)
            
            # Create temporary surface for transparency
            shield_w = self.rect.width + 40
            shield_h = self.rect.height + 40
            shield_surface = pygame.Surface((shield_w, shield_h), pygame.SRCALPHA)
            shield_color = (100, 150, 255, alpha)  # Light blue with transparency
            
            # Draw oval shield
            pygame.draw.ellipse(shield_surface, shield_color, (0, 0, shield_w, shield_h))
            # Add border
            pygame.draw.ellipse(shield_surface, (150, 200, 255, 200), (0, 0, shield_w, shield_h), 3)
            
            surface.blit(shield_surface, (self.rect.x - 20, self.rect.y - 20))
        
        # Draw parry indicator when parrying (takes priority over blocking)
        elif self.parrying and self.parry_window > 0:
            # Flash yellow shield during parry window (optimized)
            pulse = math.sin(self.animation_frame * 0.5)
            alpha = int(150 + 105 * pulse)
            
            # Create temporary surface for transparency
            parry_w = self.rect.width + 30
            parry_h = self.rect.height + 30
            parry_surface = pygame.Surface((parry_w, parry_h), pygame.SRCALPHA)
            parry_color = (255, 255, 0, alpha)  # Yellow with transparency
            
            # Draw circular parry indicator
            pygame.draw.ellipse(parry_surface, parry_color, (0, 0, parry_w, parry_h))
            # Add bright border
            pygame.draw.ellipse(parry_surface, (255, 255, 100, 255), (0, 0, parry_w, parry_h), 4)
            
            surface.blit(parry_surface, (self.rect.x - 15, self.rect.y - 15))
        
        # Hitbox Debug View (optional)
        if self.attacking and self.attack_rect:
            s = pygame.Surface((self.attack_rect.width, self.attack_rect.height))
            s.set_alpha(100)
            s.fill(c.RED)
            surface.blit(s, (self.attack_rect.x, self.attack_rect.y))