import pygame
import config as c

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
    def __init__(self, x, y, stats, controls, is_p2=False):
        self.rect = pygame.Rect(x, y, c.P_WIDTH, c.P_HEIGHT)
        self.stats = stats
        self.color = stats['color']
        self.controls = controls 
        self.is_p2 = is_p2
        
        # Physics from stats
        self.speed = stats['speed']
        self.jump_force = stats['jump']
        self.max_health = stats['health']
        self.health = self.max_health
        self.dmg_mult = stats['dmg_mult']
        
        # Power Bar System
        self.max_power = 100
        self.power = 0
        
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
        self.attack_rect = None
        self.color_flash = 0 
        
        # Combo System
        self.combo_count = 0
        self.last_hit_time = 0

        # Attack Definitions
        self.moves = {
            'light': Attack('Light', 5 * self.dmg_mult, 300, 60, 20, 5, 10),
            'heavy': Attack('Heavy', 12 * self.dmg_mult, 700, 70, 40, 15, 20),
            'kick': Attack('Kick', 8 * self.dmg_mult, 500, 80, 30, 10, 15),
            'special': Attack('Special', 20 * self.dmg_mult, 2000, 120, 60, 25, 30)
        }

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

        key = pygame.key.get_pressed()

        # Input Handling
        if not self.attacking:
            if key[self.controls['left']]:
                dx = -self.speed
                self.facing_right = False
            if key[self.controls['right']]:
                dx = self.speed
                self.facing_right = True
            
            if key[self.controls['jump']] and not self.jumping:
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

        # Attacks
        current_time = pygame.time.get_ticks()
        if not self.attacking and current_time - self.last_attack_time > self.attack_cooldown:
            attack_key = None
            # PRIORITY: Special > Heavy > Kick > Light
            if key[self.controls['special']]: attack_key = 'special'
            elif key[self.controls['heavy']]: attack_key = 'heavy'
            elif key[self.controls['kick']]: attack_key = 'kick'
            elif key[self.controls['light']]: attack_key = 'light'

            if attack_key:
                self.attack(target, attack_key)

        self.rect.x += dx
        self.rect.y += dy

    def attack(self, target, type_key):
        self.attacking = True
        move_data = self.moves[type_key]
        self.attack_type = type_key
        self.last_attack_time = pygame.time.get_ticks()
        self.attack_cooldown = move_data.cooldown
        
        hitbox_x = self.rect.right if self.facing_right else self.rect.left - move_data.width
        hitbox_y = self.rect.y + 10
        
        self.attack_rect = pygame.Rect(hitbox_x, hitbox_y, move_data.width, move_data.height)
        
        if self.attack_rect.colliderect(target.rect):
            # Check if this continues a combo
            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time < 2000:  # 2 second window
                self.combo_count += 1
            else:
                self.combo_count = 1
            
            self.last_hit_time = current_time
            
            # Apply damage and gain power
            target.take_damage(move_data.damage, move_data.knockback, move_data.stun, self.facing_right, self)
            
            # Gain power for landing hit
            self.gain_power(5 if type_key == 'light' else 10)
            
            return True 
        else:
            # Reset combo on miss
            self.combo_count = 0
        return False 

    def take_damage(self, amount, knockback, stun, attacker_facing_right, attacker=None):
        self.health -= amount
        self.hit_stun = stun
        self.attacking = False 
        self.color_flash = 5 
        
        # Gain power when hit (defensive gain) - only if we have power bar
        if hasattr(self, 'power'):
            self.gain_power(8)
        
        # Reset combo when hit - only if we have combo system
        if hasattr(self, 'combo_count'):
            self.combo_count = 0
        
        direction = 1 if attacker_facing_right else -1
        self.rect.x += knockback * direction * 2 
        
        if self.health <= 0:
            self.health = 0
            self.alive = False
    
    def gain_power(self, amount):
        """Gain power for special moves"""
        self.power = min(self.max_power, self.power + amount)

    def update(self):
        if self.attacking:
            # Animation duration override
            if pygame.time.get_ticks() - self.last_attack_time > 200:
                self.attacking = False
                self.attack_rect = None

        if self.color_flash > 0:
            self.color_flash -= 1

    def draw(self, surface):
        # Shadow
        pygame.draw.ellipse(surface, (20,20,20), (self.rect.x, c.FLOOR_Y - 10, c.P_WIDTH, 20))
        
        # Body
        color = c.WHITE if self.color_flash > 0 else self.color
        pygame.draw.rect(surface, color, self.rect)
        
        # Eyes
        eye_x = self.rect.right - 15 if self.facing_right else self.rect.left + 5
        pygame.draw.rect(surface, c.BLACK, (eye_x, self.rect.y + 15, 10, 5))
        
        # Hitbox Debug View
        if self.attacking and self.attack_rect:
            s = pygame.Surface((self.attack_rect.width, self.attack_rect.height))
            s.set_alpha(100)
            s.fill(c.RED)
            surface.blit(s, (self.attack_rect.x, self.attack_rect.y))