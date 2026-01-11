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

class Projectile:
    """Fireball logic"""
    def __init__(self, x, y, direction, owner, move_data):
        self.rect = pygame.Rect(x, y, 40, 30)
        self.direction = direction
        self.speed = c.FIREBALL_SPEED
        self.owner = owner # To prevent self-damage
        self.move_data = move_data
        self.active = True
        self.timer = 100 # Frames until it fizzles out

    def update(self):
        self.rect.x += self.speed * self.direction
        self.timer -= 1
        if self.timer <= 0:
            self.active = False
            
    def draw(self, surface):
        # Fireball Core
        pygame.draw.circle(surface, c.YELLOW, self.rect.center, 15)
        # Fireball Outline
        pygame.draw.circle(surface, c.ORANGE, self.rect.center, 18, 3)

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

        # Attack Definitions
        self.moves = {
            'light': Attack('Light', 5 * self.dmg_mult, 300, 60, 20, 5, 10),
            'heavy': Attack('Heavy', 12 * self.dmg_mult, 700, 70, 40, 15, 20),
            'kick': Attack('Kick', 8 * self.dmg_mult, 500, 80, 30, 10, 15),
            'special': Attack('Special', 15 * self.dmg_mult, 1500, 0, 0, 25, 30) # Projectile
        }

    def move(self, target, width, height, projectile_list):
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
            if key[self.controls['special']]: attack_key = 'special'
            elif key[self.controls['heavy']]: attack_key = 'heavy'
            elif key[self.controls['kick']]: attack_key = 'kick'
            elif key[self.controls['light']]: attack_key = 'light'

            if attack_key:
                self.attack(target, attack_key, projectile_list)

        self.rect.x += dx
        self.rect.y += dy

    def attack(self, target, type_key, projectile_list):
        self.attacking = True
        move_data = self.moves[type_key]
        self.attack_type = type_key
        self.last_attack_time = pygame.time.get_ticks()
        self.attack_cooldown = move_data.cooldown
        
        # PROJECTILE LOGIC
        if type_key == 'special':
            start_x = self.rect.right if self.facing_right else self.rect.left - 40
            direction = 1 if self.facing_right else -1
            # Add new projectile to the shared list
            proj = Projectile(start_x, self.rect.centery - 20, direction, self, move_data)
            projectile_list.append(proj)
            return False # No immediate hit

        # MELEE LOGIC
        hitbox_x = self.rect.right if self.facing_right else self.rect.left - move_data.width
        hitbox_y = self.rect.y + 10
        
        self.attack_rect = pygame.Rect(hitbox_x, hitbox_y, move_data.width, move_data.height)
        
        if self.attack_rect.colliderect(target.rect):
            target.take_damage(move_data.damage, move_data.knockback, move_data.stun, self.facing_right)
            return True 
        return False 

    def take_damage(self, amount, knockback, stun, attacker_facing_right):
        self.health -= amount
        self.hit_stun = stun
        self.attacking = False 
        self.color_flash = 5 
        
        direction = 1 if attacker_facing_right else -1
        self.rect.x += knockback * direction * 2 
        
        if self.health <= 0:
            self.health = 0
            self.alive = False

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
        
        # Hitbox Debug View (Melee only)
        if self.attacking and self.attack_rect and self.attack_type != 'special':
            s = pygame.Surface((self.attack_rect.width, self.attack_rect.height))
            s.set_alpha(100)
            s.fill(c.RED)
            surface.blit(s, (self.attack_rect.x, self.attack_rect.y))