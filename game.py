import pygame
import sys
import random
import config as c
from entities import Fighter, Particle

class SoundManager:
    def __init__(self):
        self.sounds = {}
        # Try to start music if file exists, otherwise ignore
        try:
            pygame.mixer.music.load('music.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1) # Loop forever
        except:
            print("No 'music.mp3' found. Running without music.")

    def play(self, name):
        pass

class Game:
    def __init__(self):
        pygame.init()
        # Fullscreen Scaled Mode for Arcade Feel
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT), pygame.SCALED | pygame.FULLSCREEN)
        pygame.display.set_caption("PyFighter Arcade")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Courier New", 24, bold=True)
        self.big_font = pygame.font.SysFont("Courier New", 64, bold=True)
        
        self.sound_manager = SoundManager()
        self.particles = []
        
        # States: MENU -> SELECT -> FIGHT -> GAMEOVER
        self.state = "MENU"
        
        # Player Objects
        self.p1 = None
        self.p2 = None
        
        # Selection Vars
        self.p1_cursor = 0
        self.p2_cursor = 1
        self.p1_selected = False
        self.p2_selected = False
        
        self.round_timer = 99
        self.last_timer_update = 0

        # Retro Scanlines
        self.scanlines = pygame.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        self.scanlines.set_colorkey(c.BLACK)
        self.scanlines.set_alpha(30)
        for y in range(0, c.SCREEN_HEIGHT, 4):
            pygame.draw.line(self.scanlines, (0, 0, 0), (0, y), (c.SCREEN_WIDTH, y), 2)

    def init_fight(self):
        # Controls
        controls_p1 = {
            'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
            'light': pygame.K_j, 'heavy': pygame.K_k, 'kick': pygame.K_l, 'special': pygame.K_i
        }
        controls_p2 = {
            'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP,
            'light': pygame.K_KP1, 'heavy': pygame.K_KP2, 'kick': pygame.K_KP3, 'special': pygame.K_KP0
        }

        # Create Fighters based on selection
        stats_p1 = c.CHARACTERS[self.p1_cursor]
        stats_p2 = c.CHARACTERS[self.p2_cursor]
        
        self.p1 = Fighter(200, 200, stats_p1, controls_p1, is_p2=False)
        self.p2 = Fighter(550, 200, stats_p2, controls_p2, is_p2=True)
        
        self.round_timer = 99
        self.particles = []
        self.state = "FIGHT"
        self.last_timer_update = pygame.time.get_ticks()

    def run(self):
        running = True
        while running:
            self.clock.tick(c.FPS)
            self.screen.fill(c.DARK_GRAY) 
            
            # --- EVENTS ---
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == "FIGHT": self.state = "MENU"
                        else: running = False

                    # MENU INPUTS
                    if self.state == "MENU":
                        if event.key == pygame.K_RETURN:
                            self.state = "SELECT"
                            self.p1_selected = False
                            self.p2_selected = False

                    # SELECT INPUTS
                    elif self.state == "SELECT":
                        # P1 Controls (WASD + J)
                        if not self.p1_selected:
                            if event.key == pygame.K_d: self.p1_cursor = (self.p1_cursor + 1) % len(c.CHARACTERS)
                            if event.key == pygame.K_a: self.p1_cursor = (self.p1_cursor - 1) % len(c.CHARACTERS)
                            if event.key == pygame.K_j: self.p1_selected = True
                        
                        # P2 Controls (Arrows + Num1)
                        if not self.p2_selected:
                            if event.key == pygame.K_RIGHT: self.p2_cursor = (self.p2_cursor + 1) % len(c.CHARACTERS)
                            if event.key == pygame.K_LEFT: self.p2_cursor = (self.p2_cursor - 1) % len(c.CHARACTERS)
                            if event.key == pygame.K_KP1: self.p2_selected = True

                    # GAMEOVER INPUTS
                    elif self.state == "GAMEOVER":
                        if event.key == pygame.K_RETURN:
                            self.state = "MENU"
            
            # --- LOOP LOGIC ---
            if self.state == "SELECT":
                self.update_select()
                self.draw_select()
                
            elif self.state == "MENU":
                self.draw_menu()
                
            elif self.state == "FIGHT":
                self.update_fight()
                self.draw_fight()
                
            elif self.state == "GAMEOVER":
                self.draw_game_over()

            # CRT Overlay
            self.screen.blit(self.scanlines, (0,0))
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    # --- STATE FUNCTIONS ---

    def update_select(self):
        # Check if both ready
        if self.p1_selected and self.p2_selected:
            pygame.time.delay(500)
            self.init_fight()

    def draw_select(self):
        title = self.big_font.render("SELECT FIGHTER", True, c.WHITE)
        self.screen.blit(title, (c.SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        # Grid settings
        start_x = 100
        start_y = 200
        gap = 160
        
        for i, char in enumerate(c.CHARACTERS):
            x = start_x + i * gap
            y = start_y
            rect = pygame.Rect(x, y, 100, 150)
            
            # Draw Character Box
            pygame.draw.rect(self.screen, char['color'], rect)
            pygame.draw.rect(self.screen, c.WHITE, rect, 2)
            
            # Name
            name_surf = self.font.render(char['name'], True, c.WHITE)
            self.screen.blit(name_surf, (x, y + 160))
            
            # Stats
            stat_surf = pygame.font.SysFont("Arial", 16).render(f"HP:{char['health']} SPD:{char['speed']}", True, c.GRAY)
            self.screen.blit(stat_surf, (x, y + 180))

            # P1 Cursor (Red Border)
            if i == self.p1_cursor:
                color = c.YELLOW if self.p1_selected else c.RED
                pygame.draw.rect(self.screen, color, (x-5, y-5, 110, 160), 5)
                p1_ind = self.font.render("P1", True, c.RED)
                self.screen.blit(p1_ind, (x+35, y-30))

            # P2 Cursor (Blue Border)
            if i == self.p2_cursor:
                color = c.YELLOW if self.p2_selected else c.BLUE
                # Offset slightly if on same char
                offset = 5 if i == self.p1_cursor else 0
                pygame.draw.rect(self.screen, color, (x-5-offset, y-5-offset, 110+offset*2, 160+offset*2), 5)
                p2_ind = self.font.render("P2", True, c.BLUE)
                self.screen.blit(p2_ind, (x+35, y+200))

    def update_fight(self):
        # Timer
        if pygame.time.get_ticks() - self.last_timer_update > 1000:
            self.round_timer -= 1
            self.last_timer_update = pygame.time.get_ticks()
            
        if self.p1.health <= 0 or self.p2.health <= 0 or self.round_timer <= 0:
            self.state = "GAMEOVER"

        self.p1.move(self.p2, c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        self.p2.move(self.p1, c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        self.p1.update()
        self.p2.update()
        
        # Particles
        if self.p1.attacking and self.p1.attack_rect and self.p1.attack_rect.colliderect(self.p2.rect):
             self.spawn_particles(self.p2.rect.centerx, self.p2.rect.centery, c.RED)
        
        if self.p2.attacking and self.p2.attack_rect and self.p2.attack_rect.colliderect(self.p1.rect):
             self.spawn_particles(self.p1.rect.centerx, self.p1.rect.centery, c.BLUE)

    def draw_fight(self):
        # Retro Grid Floor
        pygame.draw.rect(self.screen, (20, 20, 30), (0, c.FLOOR_Y, c.SCREEN_WIDTH, c.SCREEN_HEIGHT - c.FLOOR_Y))
        for x in range(0, c.SCREEN_WIDTH, 50):
            # Perspective lines
            pygame.draw.line(self.screen, (50, 50, 100), (x, c.FLOOR_Y), (x - (x-c.SCREEN_WIDTH//2), c.SCREEN_HEIGHT), 1)
        pygame.draw.line(self.screen, c.WHITE, (0, c.FLOOR_Y), (c.SCREEN_WIDTH, c.FLOOR_Y), 2)
        
        # Players
        self.p1.draw(self.screen)
        self.p2.draw(self.screen)
        
        # Particles
        for p in self.particles[:]:
            p.update()
            p.draw(self.screen)
            if p.timer <= 0: self.particles.remove(p)
            
        # UI
        self.draw_hud()

    def draw_hud(self):
        bar_width = 300
        bar_height = 30
        
        # P1 Bar
        ratio_p1 = max(0, self.p1.health / self.p1.max_health)
        pygame.draw.rect(self.screen, c.DARK_GRAY, (20, 20, bar_width, bar_height))
        pygame.draw.rect(self.screen, c.YELLOW, (20, 20, bar_width * ratio_p1, bar_height))
        pygame.draw.rect(self.screen, c.WHITE, (20, 20, bar_width, bar_height), 2)
        
        # P2 Bar
        ratio_p2 = max(0, self.p2.health / self.p2.max_health)
        pygame.draw.rect(self.screen, c.DARK_GRAY, (c.SCREEN_WIDTH - 20 - bar_width, 20, bar_width, bar_height))
        pygame.draw.rect(self.screen, c.YELLOW, (c.SCREEN_WIDTH - 20 - bar_width, 20, bar_width * ratio_p2, bar_height))
        pygame.draw.rect(self.screen, c.WHITE, (c.SCREEN_WIDTH - 20 - bar_width, 20, bar_width, bar_height), 2)
        
        # Names
        self.screen.blit(self.font.render(self.p1.stats['name'], True, c.WHITE), (20, 55))
        self.screen.blit(self.font.render(self.p2.stats['name'], True, c.WHITE), (c.SCREEN_WIDTH - 20 - bar_width, 55))
        
        # Timer
        t_color = c.WHITE if self.round_timer > 10 else c.RED
        timer_text = self.big_font.render(str(self.round_timer), True, t_color)
        self.screen.blit(timer_text, (c.SCREEN_WIDTH//2 - timer_text.get_width()//2, 10))

    def draw_menu(self):
        title = self.big_font.render("PYFIGHTER ARCADE", True, c.ORANGE)
        sub = self.font.render("INSERT COIN (PRESS ENTER)", True, c.YELLOW)
        
        self.screen.blit(title, (c.SCREEN_WIDTH//2 - title.get_width()//2, 150))
        
        # Blink effect
        if pygame.time.get_ticks() % 1000 < 500:
            self.screen.blit(sub, (c.SCREEN_WIDTH//2 - sub.get_width()//2, 300))
            
        controls = self.font.render("P1: WASD+J | P2: Arrows+Num1", True, c.GRAY)
        self.screen.blit(controls, (c.SCREEN_WIDTH//2 - controls.get_width()//2, 500))

    def draw_game_over(self):
        self.draw_fight() # Draw game behind
        
        s = pygame.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        s.set_alpha(180)
        s.fill(c.BLACK)
        self.screen.blit(s, (0,0))
        
        if self.p1.health > self.p2.health:
            txt = f"{self.p1.stats['name']} WINS!"
            col = c.RED
        elif self.p2.health > self.p1.health:
            txt = f"{self.p2.stats['name']} WINS!"
            col = c.BLUE
        else:
            txt = "DOUBLE KO!"
            col = c.YELLOW
            
        msg = self.big_font.render(txt, True, col)
        retry = self.font.render("PRESS ENTER TO RESTART", True, c.WHITE)
        
        self.screen.blit(msg, (c.SCREEN_WIDTH//2 - msg.get_width()//2, 200))
        self.screen.blit(retry, (c.SCREEN_WIDTH//2 - retry.get_width()//2, 400))

    def spawn_particles(self, x, y, color):
        for _ in range(5):
            vx = random.uniform(-5, 5)
            vy = random.uniform(-5, -2)
            self.particles.append(Particle(x, y, color, (vx, vy)))