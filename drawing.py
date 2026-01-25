"""
Drawing module for Professor Fighting Game
All characters drawn using pygame primitives (no sprites)
"""

import pygame
import math
import config as c

# Animation constants
SPINNING_KICK_ROTATION_SPEED = 12  # degrees per frame
SPINNING_KICK_FRAME_CYCLE = 30  # frames per full rotation cycle


def draw_khalid(surface, x, y, facing_right, animation_state='idle', frame=0):
    """
    Draw Professor Khalid - The Taekwondo Master
    """
    # Flip x offset based on facing direction
    flip = 1 if facing_right else -1
    
    # Head (circle, dark brown skin)
    head_x = int(x)
    head_y = int(y - 30)
    pygame.draw.circle(surface, c.KHALID_SKIN, (head_x, head_y), 12)
    
    # Hair (curved semicircle)
    hair_rect = pygame.Rect(head_x - 12, head_y - 14, 24, 14)
    pygame.draw.arc(surface, c.BLACK, hair_rect, math.pi, 2 * math.pi, 8)
    
    # Eyes
    eye_offset = 4 if facing_right else -4
    pygame.draw.circle(surface, c.BLACK, (head_x + eye_offset, head_y - 2), 2)
    
    # Torso (orange gi)
    torso_rect = pygame.Rect(x - 15, y - 18, 30, 40)
    pygame.draw.rect(surface, c.KHALID_GI, torso_rect)
    
    # Belt (black)
    belt_rect = pygame.Rect(x - 15, y + 2, 30, 4)
    pygame.draw.rect(surface, c.BLACK, belt_rect)
    
    # Arms (based on animation state)
    if animation_state in ['punch', 'light_punch', 'heavy_punch']:
        # Extended arm (punching)
        arm_start = (x + 15 * flip, y - 10)
        arm_end = (x + 35 * flip, y - 5)
        pygame.draw.line(surface, c.KHALID_SKIN, arm_start, arm_end, 6)
        # Fist
        pygame.draw.circle(surface, c.KHALID_SKIN, arm_end, 5)
        # Other arm
        pygame.draw.line(surface, c.KHALID_SKIN, (x - 10 * flip, y - 10), (x - 15 * flip, y), 5)
    elif animation_state == 'special':
        # Spinning kick pose - arms extended for balance
        arm_left = (x - 25 * flip, y - 8)
        arm_right = (x + 25 * flip, y - 8)
        pygame.draw.line(surface, c.KHALID_SKIN, (x, y - 10), arm_left, 5)
        pygame.draw.line(surface, c.KHALID_SKIN, (x, y - 10), arm_right, 5)
        # Fists for balance
        pygame.draw.circle(surface, c.KHALID_SKIN, arm_left, 4)
        pygame.draw.circle(surface, c.KHALID_SKIN, arm_right, 4)
    else:
        # Normal arms
        pygame.draw.line(surface, c.KHALID_SKIN, (x - 15, y - 10), (x - 20, y + 5), 5)
        pygame.draw.line(surface, c.KHALID_SKIN, (x + 15, y - 10), (x + 20, y + 5), 5)
    
    # Legs (based on animation state)
    if animation_state in ['kick', 'light_kick', 'heavy_kick']:
        # Extended leg (kicking) - high kick for taekwondo
        leg_start = (x, y + 22)
        leg_end = (x + 40 * flip, y + 10)  # Higher kick
        pygame.draw.line(surface, c.KHALID_GI, leg_start, leg_end, 8)
        # Foot
        pygame.draw.circle(surface, c.KHALID_SKIN, leg_end, 6)
        # Other leg - supporting leg
        pygame.draw.line(surface, c.KHALID_GI, (x, y + 22), (x - 5 * flip, y + 45), 7)
    elif animation_state == 'special':
        # Spinning kick - both legs in dynamic position
        # Rotation effect - one leg extended high, one tucked
        # angle_offset creates circular motion: frame cycles through 0-360 degrees
        # Formula: (frame % cycle) * speed gives smooth rotation animation
        angle_offset = (frame % SPINNING_KICK_FRAME_CYCLE) * SPINNING_KICK_ROTATION_SPEED
        kick_leg_x = x + int(35 * math.cos(math.radians(angle_offset))) * flip
        kick_leg_y = y + int(20 - 15 * math.sin(math.radians(angle_offset)))
        pygame.draw.line(surface, c.KHALID_GI, (x, y + 15), (kick_leg_x, kick_leg_y), 8)
        pygame.draw.circle(surface, c.KHALID_SKIN, (kick_leg_x, kick_leg_y), 6)
        # Supporting/tucked leg
        pygame.draw.line(surface, c.KHALID_GI, (x, y + 22), (x - 8 * flip, y + 35), 7)
    else:
        # Normal legs
        pygame.draw.line(surface, c.KHALID_GI, (x - 8, y + 22), (x - 10, y + 45), 7)
        pygame.draw.line(surface, c.KHALID_GI, (x + 8, y + 22), (x + 10, y + 45), 7)
    
    # Feet
    if animation_state not in ['kick', 'light_kick', 'heavy_kick']:
        pygame.draw.circle(surface, c.KHALID_SKIN, (x - 10, y + 45), 5)
        pygame.draw.circle(surface, c.KHALID_SKIN, (x + 10, y + 45), 5)


def draw_eduardo(surface, x, y, facing_right, animation_state='idle', frame=0):
    """
    Draw Professor Eduardo - The Pizza Master
    
"""
    flip = 1 if facing_right else -1
    
    # Head (circle, tan skin)
    head_x = int(x)
    head_y = int(y - 30)
    pygame.draw.circle(surface, c.EDUARDO_SKIN, (head_x, head_y), 13)
    
    # Chef hat (white)
    hat_top = pygame.Rect(x - 12, y - 50, 24, 12)
    pygame.draw.rect(surface, c.EDUARDO_HAT, hat_top)
    hat_band = pygame.Rect(x - 14, y - 40, 28, 6)
    pygame.draw.rect(surface, c.EDUARDO_HAT, hat_band)
    

    # Eyes
    eye_offset = 4 if facing_right else -4
    pygame.draw.circle(surface, c.BLACK, (head_x + eye_offset, head_y - 2), 2)
    
    # Torso (white shirt - slightly wider for chubby build)
    torso_rect = pygame.Rect(x - 18, y - 18, 36, 40)
    pygame.draw.rect(surface, c.EDUARDO_HAT, torso_rect)
    
    # Apron (red)
    apron_rect = pygame.Rect(x - 16, y - 10, 32, 35)
    pygame.draw.rect(surface, c.EDUARDO_APRON, apron_rect)
    
    # Apron strings
    pygame.draw.line(surface, c.BLACK, (x - 12, y - 10), (x - 16, y - 18), 2)
    pygame.draw.line(surface, c.BLACK, (x + 12, y - 10), (x + 16, y - 18), 2)
    
    # Arms
    if animation_state in ['punch', 'light_punch', 'heavy_punch']:
        # Extended arm
        arm_start = (x + 18 * flip, y - 10)
        arm_end = (x + 38 * flip, y - 5)
        pygame.draw.line(surface, c.EDUARDO_SKIN, arm_start, arm_end, 6)
        pygame.draw.circle(surface, c.EDUARDO_SKIN, arm_end, 5)
        # Other arm
        pygame.draw.line(surface, c.EDUARDO_SKIN, (x - 12 * flip, y - 10), (x - 18 * flip, y), 5)
    else:
        # Normal arms
        pygame.draw.line(surface, c.EDUARDO_SKIN, (x - 18, y - 10), (x - 22, y + 5), 5)
        pygame.draw.line(surface, c.EDUARDO_SKIN, (x + 18, y - 10), (x + 22, y + 5), 5)
    
    # Legs
    if animation_state in ['kick', 'light_kick', 'heavy_kick']:
        leg_start = (x, y + 22)
        leg_end = (x + 40 * flip, y + 15)
        pygame.draw.line(surface, c.EDUARDO_HAT, leg_start, leg_end, 8)
        pygame.draw.circle(surface, c.EDUARDO_SKIN, leg_end, 6)
        pygame.draw.line(surface, c.EDUARDO_HAT, (x, y + 22), (x - 5 * flip, y + 45), 7)
    else:
        pygame.draw.line(surface, c.EDUARDO_HAT, (x - 8, y + 22), (x - 10, y + 45), 7)
        pygame.draw.line(surface, c.EDUARDO_HAT, (x + 8, y + 22), (x + 10, y + 45), 7)
        pygame.draw.circle(surface, c.EDUARDO_SKIN, (x - 10, y + 45), 5)
        pygame.draw.circle(surface, c.EDUARDO_SKIN, (x + 10, y + 45), 5)


def draw_hasan(surface, x, y, facing_right, animation_state='idle', frame=0):
    """
    Draw Professor Hasan - The Pyromancer

    """
    flip = 1 if facing_right else -1
    
    # Head (circle, medium brown skin)
    head_x = int(x)
    head_y = int(y - 30)
    pygame.draw.circle(surface, c.HASAN_SKIN, (head_x, head_y), 12)
    
    # Bald head shine
    pygame.draw.circle(surface, c.WHITE, (head_x - 3, head_y - 6), 3)
    
    # Eyes (glowing if special)
    eye_offset = 4 if facing_right else -4
    if animation_state == 'special':
        pygame.draw.circle(surface, c.ORANGE, (head_x + eye_offset, head_y - 2), 3)
        pygame.draw.circle(surface, c.YELLOW, (head_x + eye_offset, head_y - 2), 2)
    else:
        pygame.draw.circle(surface, c.BLACK, (head_x + eye_offset, head_y - 2), 2)
    
    # Wizard robes (floor-length, yellow/orange)
    # Main robe body
    robe_points = [
        (x - 20, y - 15),
        (x + 20, y - 15),
        (x + 25, y + 45),
        (x - 25, y + 45)
    ]
    pygame.draw.polygon(surface, c.HASAN_ROBE, robe_points)
    
    # Robe collar
    collar_rect = pygame.Rect(x - 18, y - 18, 36, 8)
    pygame.draw.rect(surface, c.ORANGE, collar_rect)
    
    # Arms (visible through robe)
    if animation_state in ['punch', 'light_punch', 'heavy_punch', 'special']:
        # Extended arm
        arm_start = (x + 20 * flip, y - 10)
        arm_end = (x + 40 * flip, y - 5)
        pygame.draw.line(surface, c.HASAN_ROBE, arm_start, arm_end, 8)
        # Hand
        pygame.draw.circle(surface, c.HASAN_SKIN, arm_end, 6)
        # Magical effect on hand if special
        if animation_state == 'special':
            pygame.draw.circle(surface, c.ORANGE, arm_end, 8, 2)
            pygame.draw.circle(surface, c.YELLOW, arm_end, 10, 1)
    else:
        # Arms at side (barely visible)
        pygame.draw.line(surface, c.HASAN_SKIN, (x - 18, y), (x - 20, y + 10), 4)
        pygame.draw.line(surface, c.HASAN_SKIN, (x + 18, y), (x + 20, y + 10), 4)


def draw_hammoud(surface, x, y, facing_right, animation_state='idle', frame=0):
    """
    Draw Professor Hammoud - The Tech Wizard

    """
    flip = 1 if facing_right else -1
    
    # Head (circle, light tan skin)
    head_x = int(x)
    head_y = int(y - 30)
    pygame.draw.circle(surface, c.HAMMOUD_SKIN, (head_x, head_y), 12)
    
    # Buzz cut hair (short, dark)
    pygame.draw.circle(surface, c.BLACK, (head_x, head_y - 3), 11)
    pygame.draw.circle(surface, c.HAMMOUD_SKIN, (head_x, head_y + 2), 11)
    
    # Glasses (rectangular, modern)
    glass_offset = 4 if facing_right else -4
    # Frame
    glass_rect = pygame.Rect(head_x + glass_offset - 5, head_y - 4, 10, 6)
    pygame.draw.rect(surface, c.BLACK, glass_rect, 1)
    # Lens
    pygame.draw.rect(surface, c.WHITE, (head_x + glass_offset - 4, head_y - 3, 8, 4))
    # Bridge (connect left and right sides)
    if facing_right:
        pygame.draw.line(surface, c.BLACK, (head_x + glass_offset - 5, head_y - 1), 
                        (head_x - 5, head_y - 1), 1)
    else:
        pygame.draw.line(surface, c.BLACK, (head_x + glass_offset + 5, head_y - 1), 
                        (head_x + 5, head_y - 1), 1)
    
    # Eyes behind glasses
    pygame.draw.circle(surface, c.BLACK, (head_x + glass_offset, head_y - 1), 1)
    
    # Torso (white shirt)
    torso_rect = pygame.Rect(x - 14, y - 18, 28, 40)
    pygame.draw.rect(surface, c.WHITE, torso_rect)
    
    # Lab coat (green)
    coat_left = pygame.Rect(x - 16, y - 18, 10, 42)
    coat_right = pygame.Rect(x + 6, y - 18, 10, 42)
    pygame.draw.rect(surface, c.HAMMOUD_COAT, coat_left)
    pygame.draw.rect(surface, c.HAMMOUD_COAT, coat_right)
    
    # Coat collar
    pygame.draw.rect(surface, c.HAMMOUD_COAT, (x - 12, y - 18, 24, 5))
    
    # Arms
    if animation_state in ['punch', 'light_punch', 'heavy_punch', 'special']:
        # Extended arm
        arm_start = (x + 16 * flip, y - 10)
        arm_end = (x + 36 * flip, y - 5)
        pygame.draw.line(surface, c.HAMMOUD_COAT, arm_start, arm_end, 7)
        pygame.draw.circle(surface, c.HAMMOUD_SKIN, arm_end, 5)
        # Circuit effect if special
        if animation_state == 'special':
            pygame.draw.circle(surface, c.GREEN, arm_end, 8, 2)
            pygame.draw.line(surface, c.GREEN, arm_end, (arm_end[0] + 5, arm_end[1] - 5), 1)
            pygame.draw.line(surface, c.GREEN, arm_end, (arm_end[0] + 5, arm_end[1] + 5), 1)
        # Other arm
        pygame.draw.line(surface, c.HAMMOUD_COAT, (x - 10 * flip, y - 10), (x - 16 * flip, y), 5)
    else:
        # Normal arms
        pygame.draw.line(surface, c.HAMMOUD_COAT, (x - 16, y - 10), (x - 20, y + 5), 5)
        pygame.draw.line(surface, c.HAMMOUD_COAT, (x + 16, y - 10), (x + 20, y + 5), 5)
    
    # Legs (dark pants)
    if animation_state in ['kick', 'light_kick', 'heavy_kick']:
        leg_start = (x, y + 24)
        leg_end = (x + 40 * flip, y + 15)
        pygame.draw.line(surface, c.BLACK, leg_start, leg_end, 7)
        pygame.draw.circle(surface, c.HAMMOUD_SKIN, leg_end, 5)
        pygame.draw.line(surface, c.BLACK, (x, y + 24), (x - 5 * flip, y + 45), 6)
    else:
        pygame.draw.line(surface, c.BLACK, (x - 7, y + 24), (x - 9, y + 45), 6)
        pygame.draw.line(surface, c.BLACK, (x + 7, y + 24), (x + 9, y + 45), 6)
        pygame.draw.circle(surface, c.HAMMOUD_SKIN, (x - 9, y + 45), 5)
        pygame.draw.circle(surface, c.HAMMOUD_SKIN, (x + 9, y + 45), 5)


def draw_pizza_slice(surface, x, y, rotation):
    """Draw a pizza slice projectile with rotation"""
    # Create pizza slice as triangle
    size = 16
    angle_rad = math.radians(rotation)
    
    # Triangle points (pizza slice shape)
    points = [
        (size * math.cos(angle_rad), size * math.sin(angle_rad)),
        (size * math.cos(angle_rad + 2.5), size * math.sin(angle_rad + 2.5)),
        (0, 0)
    ]
    
    # Translate to position
    translated_points = [(x + px, y + py) for px, py in points]
    
    # Draw pizza
    pygame.draw.polygon(surface, c.ORANGE, translated_points)
    pygame.draw.polygon(surface, c.RED, translated_points, 2)
    
    # Cheese circles
    pygame.draw.circle(surface, c.YELLOW, (int(x + points[0][0] * 0.4), int(y + points[0][1] * 0.4)), 2)
    pygame.draw.circle(surface, c.YELLOW, (int(x + points[1][0] * 0.4), int(y + points[1][1] * 0.4)), 2)


def draw_fireball(surface, x, y, frame):
    """Draw a fireball with flame effects"""
    # Main fireball (orange/yellow gradient effect)
    pygame.draw.circle(surface, c.ORANGE, (int(x), int(y)), 12)
    pygame.draw.circle(surface, c.YELLOW, (int(x), int(y)), 8)
    pygame.draw.circle(surface, c.WHITE, (int(x), int(y)), 4)
    
    # Flame particles around edge (animated based on frame)
    for i in range(6):
        angle = (frame * 10 + i * 60) % 360
        angle_rad = math.radians(angle)
        offset_x = 14 * math.cos(angle_rad)
        offset_y = 14 * math.sin(angle_rad)
        pygame.draw.circle(surface, c.ORANGE, (int(x + offset_x), int(y + offset_y)), 3)


def draw_circuit_board(surface, x, y, frame):
    """Draw a circuit board projectile with binary code"""
    # Base green rectangle
    base_rect = pygame.Rect(int(x) - 10, int(y) - 10, 20, 20)
    pygame.draw.rect(surface, c.HAMMOUD_COAT, base_rect)
    pygame.draw.rect(surface, c.GREEN, base_rect, 2)
    
    # Circuit lines
    pygame.draw.line(surface, c.GREEN, (x - 8, y - 5), (x + 8, y - 5), 1)
    pygame.draw.line(surface, c.GREEN, (x - 8, y), (x + 8, y), 1)
    pygame.draw.line(surface, c.GREEN, (x - 8, y + 5), (x + 8, y + 5), 1)
    pygame.draw.line(surface, c.GREEN, (x - 5, y - 8), (x - 5, y + 8), 1)
    pygame.draw.line(surface, c.GREEN, (x + 5, y - 8), (x + 5, y + 8), 1)
    
    # Small circuit nodes
    pygame.draw.circle(surface, c.GREEN, (int(x - 5), int(y - 5)), 2)
    pygame.draw.circle(surface, c.GREEN, (int(x + 5), int(y - 5)), 2)
    pygame.draw.circle(surface, c.GREEN, (int(x - 5), int(y + 5)), 2)
    pygame.draw.circle(surface, c.GREEN, (int(x + 5), int(y + 5)), 2)
    
    # Glow effect (cyan outline)
    if frame % 2 == 0:
        pygame.draw.rect(surface, (0, 255, 255), base_rect.inflate(4, 4), 1)


def draw_hit_effect(surface, x, y, effect_type='light', color=c.YELLOW, frame=0):
    """
    Draw comic book style hit effects
    
    effect_type: 'light' (POW!), 'heavy' (BOOM!), 'special' (WHAM!), 'ko' (K.O!)
    """
    # Create star burst background
    num_points = 12
    for i in range(num_points):
        angle = (360 / num_points) * i + (frame * 5)
        angle_rad = math.radians(angle)
        
        # Alternating long/short points for star
        if i % 2 == 0:
            radius = 30
        else:
            radius = 15
        
        end_x = x + radius * math.cos(angle_rad)
        end_y = y + radius * math.sin(angle_rad)
        
        pygame.draw.line(surface, color, (x, y), (end_x, end_y), 3)
    
    # Text based on type (will be rendered by game using text renderer)
    # This just draws the background burst


def draw_victory_pose_khalid(surface, x, y, frame):
    """Draw Khalid's victory pose - Traditional martial arts bow"""
    # Tilted forward body
    draw_khalid(surface, x, y + 10, True, 'idle', frame)
    
    # Draw additional bow indicators
    # Tilted head/torso would be handled in animation state


def draw_victory_pose_eduardo(surface, x, y, frame):
    """Draw Eduardo's victory pose - Eating pizza"""
    draw_eduardo(surface, x, y, True, 'idle', frame)
    
    # Pizza slice in hand
    draw_pizza_slice(surface, x + 25, y - 15, frame * 2)


def draw_victory_pose_hasan(surface, x, y, frame):
    """Draw Hasan's victory pose - Arms crossed with flames"""
    draw_hasan(surface, x, y, True, 'idle', frame)
    
    # Flame particles orbiting
    for i in range(8):
        angle = (frame * 5 + i * 45) % 360
        angle_rad = math.radians(angle)
        orbit_x = x + 40 * math.cos(angle_rad)
        orbit_y = y + 40 * math.sin(angle_rad)
        pygame.draw.circle(surface, c.ORANGE, (int(orbit_x), int(orbit_y)), 4)
        pygame.draw.circle(surface, c.YELLOW, (int(orbit_x), int(orbit_y)), 2)


def draw_victory_pose_hammoud(surface, x, y, frame):
    """Draw Hammoud's victory pose - Adjusting glasses"""
    draw_hammoud(surface, x, y, True, 'idle', frame)
    
    # Binary code rain effect
    for i in range(5):
        text_x = x - 30 + i * 15
        text_y = (y - 50 + (frame * 2 + i * 10) % 100)
        # Binary digits would be rendered by game


def draw_blood_puddle(surface, x, y, size=60):
    """Draw a blood puddle on the ground"""
    # Main puddle (dark red)
    blood_color = (139, 0, 0)  # Dark red
    # Draw irregular puddle with overlapping circles
    pygame.draw.ellipse(surface, blood_color, (x - size // 2, y - size // 4, size, size // 2))
    pygame.draw.ellipse(surface, blood_color, (x - size // 3, y - size // 5, size * 2 // 3, size // 3))
    pygame.draw.ellipse(surface, blood_color, (x - size // 4, y - size // 6, size // 2, size // 4))
    
    # Darker spots for depth
    darker_blood = (100, 0, 0)
    pygame.draw.ellipse(surface, darker_blood, (x - size // 4, y - size // 8, size // 3, size // 6))


def draw_defeated_character(surface, x, y, char_name, skin_color, outfit_color):
    """Draw a character laying on the ground (defeated)"""
    # Character laying down on their back
    # Body (horizontal)
    body_rect = pygame.Rect(x - 40, y - 15, 60, 25)
    pygame.draw.rect(surface, outfit_color, body_rect)
    
    # Head (tilted to side)
    head_x = int(x + 35)
    head_y = int(y - 10)
    pygame.draw.circle(surface, skin_color, (head_x, head_y), 10)
    
    # Closed eyes (X marks)
    pygame.draw.line(surface, c.BLACK, (head_x - 3, head_y - 2), (head_x - 1, head_y), 2)
    pygame.draw.line(surface, c.BLACK, (head_x - 1, head_y - 2), (head_x - 3, head_y), 2)
    pygame.draw.line(surface, c.BLACK, (head_x + 1, head_y - 2), (head_x + 3, head_y), 2)
    pygame.draw.line(surface, c.BLACK, (head_x + 3, head_y - 2), (head_x + 1, head_y), 2)
    
    # Arms (spread out)
    pygame.draw.line(surface, skin_color, (x - 10, y - 10), (x - 30, y - 25), 5)
    pygame.draw.line(surface, skin_color, (x + 10, y - 10), (x + 20, y - 25), 5)
    
    # Legs (spread out)
    pygame.draw.line(surface, outfit_color, (x - 20, y + 10), (x - 35, y + 25), 6)
    pygame.draw.line(surface, outfit_color, (x - 5, y + 10), (x + 5, y + 30), 6)


def draw_victory_dance(surface, x, y, char_name, skin_color, outfit_color, frame):
    """Draw character doing a victory dance (bouncing up and down)"""
    # Calculate bounce offset (up and down motion)
    bounce_offset = int(math.sin(frame * 0.3) * 15)
    
    # Draw character at bounced position
    dance_y = y + bounce_offset
    
    # Use appropriate character draw function
    if 'KHALID' in char_name:
        draw_khalid(surface, x, dance_y, True, 'idle', frame)
    elif 'EDUARDO' in char_name:
        draw_eduardo(surface, x, dance_y, True, 'idle', frame)
    elif 'HASAN' in char_name:
        draw_hasan(surface, x, dance_y, True, 'idle', frame)
    elif 'HAMMOUD' in char_name:
        draw_hammoud(surface, x, dance_y, True, 'idle', frame)
    
    # Add victory sparkles around character
    for i in range(3):
        sparkle_angle = (frame * 10 + i * 120) % 360
        sparkle_rad = math.radians(sparkle_angle)
        sparkle_x = x + 30 * math.cos(sparkle_rad)
        sparkle_y = dance_y - 40 + 30 * math.sin(sparkle_rad)
        pygame.draw.circle(surface, c.YELLOW, (int(sparkle_x), int(sparkle_y)), 3)


def draw_dash_particles(surface, x, y, facing_right, frame):
    """Draw air particles for dash effect"""
    # Direction opposite to dash
    direction = -1 if facing_right else 1
    
    # Spawn particles trailing behind
    for i in range(5):
        particle_x = x + (direction * (10 + i * 8))
        particle_y = y - 20 + (i % 3) * 10
        
        # Fade based on distance
        alpha = 255 - (i * 40)
        if alpha > 0:
            size = 6 - i
            if size > 0:
                # Create particle with fade effect
                particle_color = (200, 200, 255)
                pygame.draw.circle(surface, particle_color, (int(particle_x), int(particle_y)), size)
