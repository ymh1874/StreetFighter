"""
AI vs AI Test - Automated match to showcase game mechanics
"""

import pygame
import sys
import config as c
from entities import Fighter
from ai_controller import AIController
import time

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pygame.display.set_caption("AI vs AI Test - CMUQ Arena")
clock = pygame.time.Clock()

# Create fighters
controls_p1 = {
    'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w, 'crouch': pygame.K_s,
    'light': pygame.K_j, 'heavy': pygame.K_k, 'kick': pygame.K_l, 'special': pygame.K_i
}
controls_p2 = {
    'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP, 'crouch': pygame.K_DOWN,
    'light': pygame.K_KP1, 'heavy': pygame.K_KP2, 'kick': pygame.K_KP3, 'special': pygame.K_KP0
}

# Select random characters
import random
p1_char = random.choice(c.CHARACTERS)
p2_char = random.choice(c.CHARACTERS)

print("=" * 60)
print("AI VS AI TEST MATCH")
print("=" * 60)
print(f"Player 1: {p1_char['name']} ({p1_char['desc']})")
print(f"Player 2: {p2_char['name']} ({p2_char['desc']})")
print("=" * 60)

fighter1 = Fighter(200, 200, p1_char, controls_p1, is_p2=False)
fighter2 = Fighter(550, 200, p2_char, controls_p2, is_p2=True)

# Create AI controllers (hard difficulty)
ai1 = AIController(fighter1, fighter2, 'hard')
ai2 = AIController(fighter2, fighter1, 'hard')

# Game state
projectiles = []
particles = []
round_timer = 99
last_timer_update = pygame.time.get_ticks()
running = True
frame_count = 0
max_frames = 3600  # 60 seconds at 60 FPS

# Statistics
stats = {
    'p1_attacks': 0,
    'p2_attacks': 0,
    'p1_hits': 0,
    'p2_hits': 0,
    'projectiles_fired': 0,
    'max_combo_p1': 0,
    'max_combo_p2': 0
}

print("\nMatch Starting...")
print("=" * 60)

# Main loop
while running and frame_count < max_frames:
    clock.tick(c.FPS)
    frame_count += 1
    
    # Handle quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
    
    # Update timer
    if pygame.time.get_ticks() - last_timer_update > 1000:
        round_timer -= 1
        last_timer_update = pygame.time.get_ticks()
        print(f"Time: {round_timer}s | P1 HP: {fighter1.health:.0f} | P2 HP: {fighter2.health:.0f}")
    
    # Check end conditions
    if fighter1.health <= 0 or fighter2.health <= 0 or round_timer <= 0:
        running = False
        break
    
    # Update AI
    ai1.update(projectiles)
    ai2.update(projectiles)
    
    # Track attacks
    prev_p1_attacking = fighter1.attacking
    prev_p2_attacking = fighter2.attacking
    
    # AI makes attack decisions
    if random.random() < ai1.aggression * 0.3:
        old_proj_count = len(projectiles)
        ai1._attack_opponent(projectiles)
        if len(projectiles) > old_proj_count:
            stats['projectiles_fired'] += 1
        if fighter1.attacking and not prev_p1_attacking:
            stats['p1_attacks'] += 1
    
    if random.random() < ai2.aggression * 0.3:
        old_proj_count = len(projectiles)
        ai2._attack_opponent(projectiles)
        if len(projectiles) > old_proj_count:
            stats['projectiles_fired'] += 1
        if fighter2.attacking and not prev_p2_attacking:
            stats['p2_attacks'] += 1
    
    # Update fighters
    fighter1.move(fighter2, c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
    fighter2.move(fighter1, c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
    fighter1.update()
    fighter2.update()
    
    # Track combos
    if fighter1.combo_hits > stats['max_combo_p1']:
        stats['max_combo_p1'] = fighter1.combo_hits
    if fighter2.combo_hits > stats['max_combo_p2']:
        stats['max_combo_p2'] = fighter2.combo_hits
    
    # Update projectiles
    for proj in projectiles[:]:
        proj.update()
        
        # Check collisions
        if proj.owner != fighter1 and proj.rect.colliderect(fighter1.rect):
            if not fighter1.invincible:
                fighter1.health -= proj.damage
                fighter1.hit_stun = 15
                stats['p2_hits'] += 1
            try:
                projectiles.remove(proj)
            except:
                pass
        elif proj.owner != fighter2 and proj.rect.colliderect(fighter2.rect):
            if not fighter2.invincible:
                fighter2.health -= proj.damage
                fighter2.hit_stun = 15
                stats['p1_hits'] += 1
            try:
                projectiles.remove(proj)
            except:
                pass
        
        # Remove off-screen
        if proj.rect.right < 0 or proj.rect.left > c.SCREEN_WIDTH or proj.rect.bottom < 0:
            try:
                projectiles.remove(proj)
            except:
                pass
    
    # Track melee hits
    if fighter1.attacking and fighter1.attack_rect and fighter1.attack_rect.colliderect(fighter2.rect):
        if not fighter2.invincible and fighter2.hit_stun == 0:
            stats['p1_hits'] += 1
    if fighter2.attacking and fighter2.attack_rect and fighter2.attack_rect.colliderect(fighter1.rect):
        if not fighter1.invincible and fighter1.hit_stun == 0:
            stats['p2_hits'] += 1
    
    # Render
    screen.fill(c.DARK_GRAY)
    
    # Floor
    pygame.draw.rect(screen, (20, 20, 30), (0, c.FLOOR_Y, c.SCREEN_WIDTH, c.SCREEN_HEIGHT - c.FLOOR_Y))
    pygame.draw.line(screen, c.WHITE, (0, c.FLOOR_Y), (c.SCREEN_WIDTH, c.FLOOR_Y), 2)
    
    # Fighters
    fighter1.draw(screen)
    fighter2.draw(screen)
    
    # Projectiles
    for proj in projectiles:
        proj.draw(screen)
    
    # Simple HUD
    font = pygame.font.Font(None, 36)
    
    # Health bars
    bar_width = 300
    bar_height = 30
    
    # P1 health
    ratio_p1 = max(0, fighter1.health / fighter1.max_health)
    pygame.draw.rect(screen, c.BLACK, (18, 18, bar_width + 4, bar_height + 4))
    pygame.draw.rect(screen, c.DARK_GRAY, (20, 20, bar_width, bar_height))
    pygame.draw.rect(screen, c.RED, (20, 20, bar_width * ratio_p1, bar_height))
    pygame.draw.rect(screen, c.WHITE, (20, 20, bar_width, bar_height), 3)
    
    # P2 health
    ratio_p2 = max(0, fighter2.health / fighter2.max_health)
    p2_x = c.SCREEN_WIDTH - 20 - bar_width
    pygame.draw.rect(screen, c.BLACK, (p2_x - 2, 18, bar_width + 4, bar_height + 4))
    pygame.draw.rect(screen, c.DARK_GRAY, (p2_x, 20, bar_width, bar_height))
    pygame.draw.rect(screen, c.BLUE, (p2_x, 20, bar_width * ratio_p2, bar_height))
    pygame.draw.rect(screen, c.WHITE, (p2_x, 20, bar_width, bar_height), 3)
    
    # Timer
    try:
        timer_text = font.render(str(round_timer), True, c.WHITE)
        timer_x = c.SCREEN_WIDTH // 2 - timer_text.get_width() // 2
        screen.blit(timer_text, (timer_x, 10))
    except:
        pass
    
    pygame.display.flip()

# Final results
print("\n" + "=" * 60)
print("MATCH COMPLETE!")
print("=" * 60)

# Determine winner
if fighter1.health > fighter2.health:
    winner = p1_char['name']
    winner_hp = fighter1.health
elif fighter2.health > fighter1.health:
    winner = p2_char['name']
    winner_hp = fighter2.health
else:
    winner = "DRAW"
    winner_hp = 0

print(f"\nWinner: {winner}")
print(f"Final HP: P1={fighter1.health:.0f} | P2={fighter2.health:.0f}")
print(f"\nMatch Statistics:")
print(f"  P1 Attacks: {stats['p1_attacks']}")
print(f"  P1 Hits: {stats['p1_hits']}")
print(f"  P1 Max Combo: {stats['max_combo_p1']}")
print(f"  P2 Attacks: {stats['p2_attacks']}")
print(f"  P2 Hits: {stats['p2_hits']}")
print(f"  P2 Max Combo: {stats['max_combo_p2']}")
print(f"  Projectiles Fired: {stats['projectiles_fired']}")
print(f"  Total Frames: {frame_count}")
print("=" * 60)

# Keep window open for a moment
pygame.time.delay(3000)
pygame.quit()
