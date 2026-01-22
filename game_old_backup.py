import pygame
import sys
import random
import config as c
from entities import Fighter, Particle
from text_renderer import SimpleTextRenderer

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
        self.text_renderer = SimpleTextRenderer()
        
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
        # Title with background
        title = self.text_renderer.render("CHOOSE YOUR FIGHTER", 'large', c.WHITE)
        title_bg = pygame.Rect(c.SCREEN_WIDTH//2 - title.get_width()//2 - 20, 35, title.get_width() + 40, 80)
        pygame.draw.rect(self.screen, c.DARK_GRAY, title_bg)
        pygame.draw.rect(self.screen, c.ORANGE, title_bg, 3)
        self.screen.blit(title, (c.SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        # Grid settings - better centered
        start_x = 50
        start_y = 180
        gap = 175
        
        for i, char in enumerate(c.CHARACTERS):
            x = start_x + i * gap
            y = start_y
            rect = pygame.Rect(x, y, 120, 140)
            
            # Draw Character Box with shadow
            shadow_rect = pygame.Rect(x + 3, y + 3, 120, 140)
            pygame.draw.rect(self.screen, c.BLACK, shadow_rect)
            pygame.draw.rect(self.screen, char['color'], rect)
            pygame.draw.rect(self.screen, c.WHITE, rect, 3)
            
            # Name - centered under box
            name_surf = self.text_renderer.render(char['name'], 'medium', c.WHITE)
            name_x = x + 60 - name_surf.get_width()//2
            self.screen.blit(name_surf, (name_x, y + 150))
            
            # Description - centered
            desc_surf = self.text_renderer.render(char['desc'], 'small', c.GRAY)
            desc_x = x + 60 - desc_surf.get_width()//2
            self.screen.blit(desc_surf, (desc_x, y + 175))
            
            # Stats - centered
            stat_text = f"HP:{char['health']} SPD:{char['speed']}"
            stat_surf = self.text_renderer.render(stat_text, 'small', c.GRAY)
            stat_x = x + 60 - stat_surf.get_width()//2
            self.screen.blit(stat_surf, (stat_x, y + 195))

            # P1 Cursor (Red Border)
            if i == self.p1_cursor:
                color = c.YELLOW if self.p1_selected else c.RED
                pygame.draw.rect(self.screen, color, (x-5, y-5, 130, 150), 5)
                # P1 indicator - centered above
                p1_ind = self.text_renderer.render("P1", 'medium', c.RED)
                p1_x = x + 60 - p1_ind.get_width()//2
                self.screen.blit(p1_ind, (p1_x, y-35))
                if self.p1_selected:
                    ready_text = self.text_renderer.render("READY!", 'small', c.YELLOW)
                    ready_x = x + 60 - ready_text.get_width()//2
                    self.screen.blit(ready_text, (ready_x, y + 215))

            # P2 Cursor (Blue Border)
            if i == self.p2_cursor:
                color = c.YELLOW if self.p2_selected else c.BLUE
                # Offset slightly if on same char
                offset = 6 if i == self.p1_cursor else 0
                pygame.draw.rect(self.screen, color, (x-5-offset, y-5-offset, 130+offset*2, 150+offset*2), 5)
                # P2 indicator - centered below
                p2_ind = self.text_renderer.render("P2", 'medium', c.BLUE)
                p2_x = x + 60 - p2_ind.get_width()//2
                self.screen.blit(p2_ind, (p2_x, y + 235))
                if self.p2_selected:
                    ready_text = self.text_renderer.render("READY!", 'small', c.YELLOW)
                    ready_x = x + 60 - ready_text.get_width()//2
                    self.screen.blit(ready_text, (ready_x, y + 255))

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
        
        # P1 Bar with border
        ratio_p1 = max(0, self.p1.health / self.p1.max_health)
        pygame.draw.rect(self.screen, c.BLACK, (18, 18, bar_width + 4, bar_height + 4))
        pygame.draw.rect(self.screen, c.DARK_GRAY, (20, 20, bar_width, bar_height))
        pygame.draw.rect(self.screen, c.RED, (20, 20, bar_width * ratio_p1, bar_height))
        pygame.draw.rect(self.screen, c.WHITE, (20, 20, bar_width, bar_height), 3)
        
        # P2 Bar with border
        ratio_p2 = max(0, self.p2.health / self.p2.max_health)
        p2_bar_x = c.SCREEN_WIDTH - 20 - bar_width
        pygame.draw.rect(self.screen, c.BLACK, (p2_bar_x - 2, 18, bar_width + 4, bar_height + 4))
        pygame.draw.rect(self.screen, c.DARK_GRAY, (p2_bar_x, 20, bar_width, bar_height))
        pygame.draw.rect(self.screen, c.BLUE, (p2_bar_x, 20, bar_width * ratio_p2, bar_height))
        pygame.draw.rect(self.screen, c.WHITE, (p2_bar_x, 20, bar_width, bar_height), 3)
        
        # P1 Name with background
        p1_name = self.text_renderer.render(self.p1.stats['name'], 'medium', c.WHITE)
        name_bg = pygame.Rect(18, 53, p1_name.get_width() + 10, p1_name.get_height() + 4)
        pygame.draw.rect(self.screen, c.BLACK, name_bg)
        self.screen.blit(p1_name, (23, 55))
        
        # P2 Name with background (right-aligned)
        p2_name = self.text_renderer.render(self.p2.stats['name'], 'medium', c.WHITE)
        p2_name_x = p2_bar_x + bar_width - p2_name.get_width() - 5
        name_bg2 = pygame.Rect(p2_name_x - 5, 53, p2_name.get_width() + 10, p2_name.get_height() + 4)
        pygame.draw.rect(self.screen, c.BLACK, name_bg2)
        self.screen.blit(p2_name, (p2_name_x, 55))
        
        # Timer with background circle/box
        t_color = c.WHITE if self.round_timer > 10 else c.RED
        timer_text = self.text_renderer.render(str(self.round_timer), 'large', t_color)
        timer_x = c.SCREEN_WIDTH//2 - timer_text.get_width()//2
        timer_bg = pygame.Rect(timer_x - 15, 8, timer_text.get_width() + 30, timer_text.get_height() + 10)
        pygame.draw.rect(self.screen, c.BLACK, timer_bg)
        pygame.draw.rect(self.screen, c.DARK_GRAY, timer_bg, 3)
        self.screen.blit(timer_text, (timer_x, 10))
        
        # FIGHT text at start with pulsing effect
        if self.round_timer > 96:
            fight_text = self.text_renderer.render("FIGHT!", 'large', c.YELLOW)
            fight_bg = pygame.Rect(c.SCREEN_WIDTH//2 - fight_text.get_width()//2 - 20, 
                                   c.SCREEN_HEIGHT//2 - 50, 
                                   fight_text.get_width() + 40, 90)
            pygame.draw.rect(self.screen, c.BLACK, fight_bg)
            pygame.draw.rect(self.screen, c.ORANGE, fight_bg, 5)
            self.screen.blit(fight_text, (c.SCREEN_WIDTH//2 - fight_text.get_width()//2, c.SCREEN_HEIGHT//2 - 30))

    def draw_menu(self):
        # Decorative top bar
        pygame.draw.rect(self.screen, c.ORANGE, (0, 0, c.SCREEN_WIDTH, 5))
        pygame.draw.rect(self.screen, c.YELLOW, (0, 5, c.SCREEN_WIDTH, 2))
        
        # Main Title with background
        title = self.text_renderer.render("CMUQ ARENA", 'large', c.ORANGE)
        title_bg = pygame.Rect(c.SCREEN_WIDTH//2 - title.get_width()//2 - 30, 130, title.get_width() + 60, 100)
        pygame.draw.rect(self.screen, c.BLACK, title_bg)
        pygame.draw.rect(self.screen, c.ORANGE, title_bg, 4)
        self.screen.blit(title, (c.SCREEN_WIDTH//2 - title.get_width()//2, 155))
        
        # Subtitle - centered
        subtitle = self.text_renderer.render("ULTIMATE FIGHTING CHAMPIONSHIP", 'medium', c.WHITE)
        sub_bg = pygame.Rect(c.SCREEN_WIDTH//2 - subtitle.get_width()//2 - 15, 245, subtitle.get_width() + 30, 40)
        pygame.draw.rect(self.screen, c.DARK_GRAY, sub_bg)
        self.screen.blit(subtitle, (c.SCREEN_WIDTH//2 - subtitle.get_width()//2, 250))
        
        # Blink effect - Press Start with box
        if pygame.time.get_ticks() % 1000 < 500:
            start_text = self.text_renderer.render(">>> PRESS ENTER TO START <<<", 'medium', c.YELLOW)
            start_bg = pygame.Rect(c.SCREEN_WIDTH//2 - start_text.get_width()//2 - 20, 325, start_text.get_width() + 40, 50)
            pygame.draw.rect(self.screen, c.DARK_GRAY, start_bg)
            pygame.draw.rect(self.screen, c.YELLOW, start_bg, 3)
            self.screen.blit(start_text, (c.SCREEN_WIDTH//2 - start_text.get_width()//2, 335))
        
        # Controls section with boxes
        controls_y = 450
        # P1 Controls
        p1_controls = self.text_renderer.render("P1: WASD + JKLI", 'small', c.RED)
        p1_bg = pygame.Rect(120, controls_y - 5, p1_controls.get_width() + 20, 35)
        pygame.draw.rect(self.screen, c.DARK_GRAY, p1_bg)
        pygame.draw.rect(self.screen, c.RED, p1_bg, 2)
        self.screen.blit(p1_controls, (130, controls_y))
        
        # P2 Controls
        p2_controls = self.text_renderer.render("P2: ARROWS + NUMPAD", 'small', c.BLUE)
        p2_bg = pygame.Rect(c.SCREEN_WIDTH - 290, controls_y - 5, p2_controls.get_width() + 20, 35)
        pygame.draw.rect(self.screen, c.DARK_GRAY, p2_bg)
        pygame.draw.rect(self.screen, c.BLUE, p2_bg, 2)
        self.screen.blit(p2_controls, (c.SCREEN_WIDTH - 280, controls_y))
        
        # Footer - centered
        footer = self.text_renderer.render("PREPARE FOR EPIC BATTLE!", 'small', c.GRAY)
        self.screen.blit(footer, (c.SCREEN_WIDTH//2 - footer.get_width()//2, 520))
        
        # Decorative bottom bar
        pygame.draw.rect(self.screen, c.ORANGE, (0, c.SCREEN_HEIGHT - 7, c.SCREEN_WIDTH, 2))
        pygame.draw.rect(self.screen, c.YELLOW, (0, c.SCREEN_HEIGHT - 5, c.SCREEN_WIDTH, 5))

    def draw_game_over(self):
        self.draw_fight() # Draw game behind
        
        # Dark overlay
        s = pygame.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        s.set_alpha(200)
        s.fill(c.BLACK)
        self.screen.blit(s, (0,0))
        
        if self.p1.health > self.p2.health:
            winner_text = f"{self.p1.stats['name']} WINS!"
            col = c.RED
            subtitle = "FLAWLESS VICTORY!"
        elif self.p2.health > self.p1.health:
            winner_text = f"{self.p2.stats['name']} WINS!"
            col = c.BLUE
            subtitle = "FLAWLESS VICTORY!"
        else:
            winner_text = "DOUBLE K.O!"
            col = c.YELLOW
            subtitle = "UNBELIEVABLE!"
        
        # Winner announcement with background box
        msg = self.text_renderer.render(winner_text, 'large', col)
        msg_bg = pygame.Rect(c.SCREEN_WIDTH//2 - msg.get_width()//2 - 30, 150, msg.get_width() + 60, 90)
        pygame.draw.rect(self.screen, c.BLACK, msg_bg)
        pygame.draw.rect(self.screen, col, msg_bg, 5)
        self.screen.blit(msg, (c.SCREEN_WIDTH//2 - msg.get_width()//2, 170))
        
        # Subtitle with background
        sub_msg = self.text_renderer.render(subtitle, 'medium', c.WHITE)
        sub_bg = pygame.Rect(c.SCREEN_WIDTH//2 - sub_msg.get_width()//2 - 20, 270, sub_msg.get_width() + 40, 50)
        pygame.draw.rect(self.screen, c.DARK_GRAY, sub_bg)
        pygame.draw.rect(self.screen, c.WHITE, sub_bg, 2)
        self.screen.blit(sub_msg, (c.SCREEN_WIDTH//2 - sub_msg.get_width()//2, 280))
        
        # Restart prompt with blinking box
        if pygame.time.get_ticks() % 1000 < 500:
            retry = self.text_renderer.render("PRESS ENTER FOR REMATCH", 'medium', c.YELLOW)
            retry_bg = pygame.Rect(c.SCREEN_WIDTH//2 - retry.get_width()//2 - 20, 385, retry.get_width() + 40, 50)
            pygame.draw.rect(self.screen, c.DARK_GRAY, retry_bg)
            pygame.draw.rect(self.screen, c.YELLOW, retry_bg, 3)
            self.screen.blit(retry, (c.SCREEN_WIDTH//2 - retry.get_width()//2, 395))

    def spawn_particles(self, x, y, color):
        for _ in range(5):
            vx = random.uniform(-5, 5)
            vy = random.uniform(-5, -2)
            self.particles.append(Particle(x, y, color, (vx, vy)))