"""
CMUQ Arena - Vintage Arcade Fighting Game
A professionally structured, maintainable fighting game with vintage arcade aesthetics

Game States:
- MAIN_MENU: Main menu with START, CONTROLS, ABOUT buttons
- CONTROLS: Display game controls
- ABOUT: Display game information
- CHARACTER_SELECT: Character selection screen
- FIGHT: Main fighting gameplay
- GAME_OVER: End game screen

Author: Senior Game Developer
Date: 2026
"""

import pygame
import sys
import random
import config as c
from entities import Fighter, Particle
from ui_components import Button, VintageTextRenderer, ArcadeFrame, ScanlineEffect


class SoundManager:
    """Manages all game audio - music and sound effects"""
    
    def __init__(self):
        """Initialize sound system and load audio files"""
        self.sounds = {}
        try:
            pygame.mixer.music.load('music.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  # Loop forever
        except:
            print("No music file found - running without background music")

    def play(self, name):
        """Play a sound effect by name"""
        if name in self.sounds:
            self.sounds[name].play()


class Game:
    """
    Main game class - handles all game logic, rendering, and state management
    """
    
    # ==================== INITIALIZATION ====================
    
    def __init__(self):
        """Initialize game window, assets, and game state"""
        pygame.init()
        
        # Display setup - fullscreen scaled for authentic arcade feel
        self.screen = pygame.display.set_mode(
            (c.SCREEN_WIDTH, c.SCREEN_HEIGHT),
            pygame.SCALED | pygame.FULLSCREEN
        )
        pygame.display.set_caption("CMUQ Arena - Vintage Arcade Fighter")
        
        # Core game components
        self.clock = pygame.time.Clock()
        self.text_renderer = VintageTextRenderer()
        self.sound_manager = SoundManager()
        
        # Visual effects
        self.scanlines = ScanlineEffect(c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        
        # Game state management
        self.state = "MAIN_MENU"  # Current game state
        self.running = True
        
        # Initialize all game screens
        self._init_main_menu()
        self._init_controls_screen()
        self._init_about_screen()
        self._init_character_select()
        self._init_fight_screen()
        
    def _init_main_menu(self):
        """Initialize main menu UI elements"""
        # Menu title
        self.menu_title = "CMUQ ARENA"
        self.menu_subtitle = "VINTAGE ARCADE FIGHTER"
        
        # Create menu buttons (centered vertically)
        button_width = 300
        button_height = 60
        button_x = c.SCREEN_WIDTH // 2 - button_width // 2
        start_y = 280
        gap = 80
        
        self.menu_buttons = [
            Button(button_x, start_y, button_width, button_height, "START", c.ORANGE),
            Button(button_x, start_y + gap, button_width, button_height, "CONTROLS", c.BLUE),
            Button(button_x, start_y + gap * 2, button_width, button_height, "ABOUT", c.GREEN)
        ]
        self.menu_selected = 0  # Current selected button (for keyboard navigation)
        
    def _init_controls_screen(self):
        """Initialize controls screen UI"""
        # Back button
        self.controls_back_button = Button(
            c.SCREEN_WIDTH // 2 - 150, 500, 300, 60, "BACK", c.ORANGE
        )
        
    def _init_about_screen(self):
        """Initialize about screen UI"""
        # Back button
        self.about_back_button = Button(
            c.SCREEN_WIDTH // 2 - 150, 500, 300, 60, "BACK", c.ORANGE
        )
        
    def _init_character_select(self):
        """Initialize character selection screen"""
        self.p1_cursor = 0
        self.p2_cursor = 1
        self.p1_selected = False
        self.p2_selected = False
        
    def _init_fight_screen(self):
        """Initialize fight screen variables"""
        self.p1 = None
        self.p2 = None
        self.round_timer = 99
        self.last_timer_update = 0
        self.particles = []
    
    # ==================== GAME LOOP ====================
    
    def run(self):
        """Main game loop - handles events, updates, and rendering"""
        while self.running:
            # Limit to 60 FPS for consistent gameplay
            self.clock.tick(c.FPS)
            
            # Clear screen with arcade background
            self.screen.fill(c.DARK_GRAY)
            
            # Get mouse state
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = False
            
            # ===== EVENT HANDLING =====
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        mouse_clicked = True
                        
                if event.type == pygame.KEYDOWN:
                    self._handle_keypress(event.key)
            
            # ===== STATE-BASED UPDATE AND RENDERING =====
            if self.state == "MAIN_MENU":
                self._update_main_menu(mouse_pos, mouse_clicked)
                self._draw_main_menu()
                
            elif self.state == "CONTROLS":
                self._update_controls(mouse_pos, mouse_clicked)
                self._draw_controls()
                
            elif self.state == "ABOUT":
                self._update_about(mouse_pos, mouse_clicked)
                self._draw_about()
                
            elif self.state == "CHARACTER_SELECT":
                self._update_character_select(mouse_pos, mouse_clicked)
                self._draw_character_select()
                
            elif self.state == "FIGHT":
                self._update_fight()
                self._draw_fight()
                
            elif self.state == "GAME_OVER":
                self._update_game_over(mouse_pos, mouse_clicked)
                self._draw_game_over()
            
            # ===== VINTAGE ARCADE EFFECTS =====
            ArcadeFrame.draw(self.screen)
            self.scanlines.draw(self.screen)
            
            # Update display
            pygame.display.flip()
        
        # Cleanup
        pygame.quit()
        sys.exit()
    
    # ==================== INPUT HANDLING ====================
    
    def _handle_keypress(self, key):
        """
        Handle keyboard input based on current game state
        
        Args:
            key: Pygame key constant
        """
        # Global: ESC to go back/quit
        if key == pygame.K_ESCAPE:
            if self.state == "MAIN_MENU":
                self.running = False
            else:
                self.state = "MAIN_MENU"
                
        # Main menu keyboard navigation
        if self.state == "MAIN_MENU":
            if key == pygame.K_UP or key == pygame.K_w:
                self.menu_selected = (self.menu_selected - 1) % len(self.menu_buttons)
            elif key == pygame.K_DOWN or key == pygame.K_s:
                self.menu_selected = (self.menu_selected + 1) % len(self.menu_buttons)
            elif key == pygame.K_RETURN or key == pygame.K_SPACE:
                self._activate_menu_button(self.menu_selected)
                
        # Character select keyboard controls
        elif self.state == "CHARACTER_SELECT":
            # P1 controls
            if not self.p1_selected:
                if key == pygame.K_a:
                    self.p1_cursor = (self.p1_cursor - 1) % len(c.CHARACTERS)
                elif key == pygame.K_d:
                    self.p1_cursor = (self.p1_cursor + 1) % len(c.CHARACTERS)
                elif key == pygame.K_j:
                    self.p1_selected = True
            
            # P2 controls
            if not self.p2_selected:
                if key == pygame.K_LEFT:
                    self.p2_cursor = (self.p2_cursor - 1) % len(c.CHARACTERS)
                elif key == pygame.K_RIGHT:
                    self.p2_cursor = (self.p2_cursor + 1) % len(c.CHARACTERS)
                elif key == pygame.K_KP1:
                    self.p2_selected = True
                    
        # Game over screen
        elif self.state == "GAME_OVER":
            if key == pygame.K_RETURN:
                self.state = "MAIN_MENU"
    
    # ==================== MAIN MENU STATE ====================
    
    def _update_main_menu(self, mouse_pos, mouse_clicked):
        """
        Update main menu logic
        
        Args:
            mouse_pos: Current mouse position tuple (x, y)
            mouse_clicked: Boolean indicating if mouse was clicked
        """
        # Update all buttons with mouse position
        for i, button in enumerate(self.menu_buttons):
            button.update(mouse_pos)
            button.selected = (i == self.menu_selected)
            
            # Check for button clicks
            if button.is_clicked(mouse_pos, mouse_clicked):
                self._activate_menu_button(i)
    
    def _activate_menu_button(self, index):
        """
        Activate menu button by index
        
        Args:
            index: Button index (0=START, 1=CONTROLS, 2=ABOUT)
        """
        if index == 0:  # START
            self.state = "CHARACTER_SELECT"
            self.p1_selected = False
            self.p2_selected = False
        elif index == 1:  # CONTROLS
            self.state = "CONTROLS"
        elif index == 2:  # ABOUT
            self.state = "ABOUT"
    
    def _draw_main_menu(self):
        """Render main menu screen with vintage arcade styling"""
        # Title section with background panel
        title = self.text_renderer.render(self.menu_title, 'large', c.ORANGE)
        title_x = c.SCREEN_WIDTH // 2 - title.get_width() // 2
        title_y = 80
        
        # Title background panel
        title_panel = pygame.Rect(title_x - 40, title_y - 20, title.get_width() + 80, title.get_height() + 40)
        pygame.draw.rect(self.screen, c.BLACK, title_panel)
        pygame.draw.rect(self.screen, c.ORANGE, title_panel, 4)
        pygame.draw.rect(self.screen, c.YELLOW, title_panel.inflate(-10, -10), 2)
        
        self.screen.blit(title, (title_x, title_y))
        
        # Subtitle
        subtitle = self.text_renderer.render(self.menu_subtitle, 'medium', c.WHITE)
        subtitle_x = c.SCREEN_WIDTH // 2 - subtitle.get_width() // 2
        self.screen.blit(subtitle, (subtitle_x, 170))
        
        # Draw all menu buttons
        for button in self.menu_buttons:
            button.draw(self.screen, self.text_renderer)
        
        # Footer text
        footer = self.text_renderer.render("USE ARROW KEYS OR MOUSE", 'small', c.GRAY)
        footer_x = c.SCREEN_WIDTH // 2 - footer.get_width() // 2
        self.screen.blit(footer, (footer_x, 540))
    
    # ==================== CONTROLS SCREEN STATE ====================
    
    def _update_controls(self, mouse_pos, mouse_clicked):
        """Update controls screen logic"""
        self.controls_back_button.update(mouse_pos)
        
        if self.controls_back_button.is_clicked(mouse_pos, mouse_clicked):
            self.state = "MAIN_MENU"
    
    def _draw_controls(self):
        """Render controls screen"""
        # Title
        title = self.text_renderer.render("GAME CONTROLS", 'large', c.ORANGE)
        title_x = c.SCREEN_WIDTH // 2 - title.get_width() // 2
        self.screen.blit(title, (title_x, 50))
        
        # Controls panel
        panel_rect = pygame.Rect(100, 150, c.SCREEN_WIDTH - 200, 320)
        pygame.draw.rect(self.screen, c.BLACK, panel_rect)
        pygame.draw.rect(self.screen, c.ORANGE, panel_rect, 3)
        
        # Player 1 controls
        y_offset = 180
        p1_title = self.text_renderer.render("PLAYER 1", 'medium', c.RED)
        self.screen.blit(p1_title, (150, y_offset))
        
        controls_p1 = [
            "MOVE: W/A/S/D",
            "LIGHT ATTACK: J",
            "HEAVY ATTACK: K",
            "KICK: L",
            "SPECIAL: I"
        ]
        
        for i, control in enumerate(controls_p1):
            text = self.text_renderer.render(control, 'small', c.WHITE)
            self.screen.blit(text, (170, y_offset + 40 + i * 30))
        
        # Player 2 controls
        p2_title = self.text_renderer.render("PLAYER 2", 'medium', c.BLUE)
        self.screen.blit(p2_title, (450, y_offset))
        
        controls_p2 = [
            "MOVE: ARROW KEYS",
            "LIGHT ATTACK: NUMPAD 1",
            "HEAVY ATTACK: NUMPAD 2",
            "KICK: NUMPAD 3",
            "SPECIAL: NUMPAD 0"
        ]
        
        for i, control in enumerate(controls_p2):
            text = self.text_renderer.render(control, 'small', c.WHITE)
            self.screen.blit(text, (470, y_offset + 40 + i * 30))
        
        # Back button
        self.controls_back_button.draw(self.screen, self.text_renderer)
    
    # ==================== ABOUT SCREEN STATE ====================
    
    def _update_about(self, mouse_pos, mouse_clicked):
        """Update about screen logic"""
        self.about_back_button.update(mouse_pos)
        
        if self.about_back_button.is_clicked(mouse_pos, mouse_clicked):
            self.state = "MAIN_MENU"
    
    def _draw_about(self):
        """Render about screen"""
        # Title
        title = self.text_renderer.render("ABOUT CMUQ ARENA", 'large', c.ORANGE)
        title_x = c.SCREEN_WIDTH // 2 - title.get_width() // 2
        self.screen.blit(title, (title_x, 50))
        
        # Info panel
        panel_rect = pygame.Rect(100, 150, c.SCREEN_WIDTH - 200, 320)
        pygame.draw.rect(self.screen, c.BLACK, panel_rect)
        pygame.draw.rect(self.screen, c.ORANGE, panel_rect, 3)
        
        # Game information
        y_offset = 180
        info_lines = [
            "CMUQ ARENA",
            "ULTIMATE FIGHTING CHAMPIONSHIP",
            "",
            "A vintage arcade-style fighting game",
            "featuring intense 1v1 combat with",
            "unique characters and special moves.",
            "",
            "Developed with passion for",
            "classic arcade gaming.",
            "",
            "Version 1.0 - 2026"
        ]
        
        for i, line in enumerate(info_lines):
            color = c.ORANGE if i < 2 else c.WHITE
            size = 'medium' if i < 2 else 'small'
            text = self.text_renderer.render(line, size, color)
            text_x = c.SCREEN_WIDTH // 2 - text.get_width() // 2
            self.screen.blit(text, (text_x, y_offset + i * 25))
        
        # Back button
        self.about_back_button.draw(self.screen, self.text_renderer)
    
    # ==================== CHARACTER SELECT STATE ====================
    
    def _update_character_select(self, mouse_pos, mouse_clicked):
        """Update character selection logic"""
        # Check if both players are ready
        if self.p1_selected and self.p2_selected:
            pygame.time.delay(500)
            self._start_fight()
    
    def _draw_character_select(self):
        """Render character selection screen with perfect alignment"""
        # Title
        title = self.text_renderer.render("CHOOSE YOUR FIGHTER", 'large', c.WHITE)
        title_x = c.SCREEN_WIDTH // 2 - title.get_width() // 2
        title_bg = pygame.Rect(title_x - 30, 35, title.get_width() + 60, 70)
        pygame.draw.rect(self.screen, c.BLACK, title_bg)
        pygame.draw.rect(self.screen, c.ORANGE, title_bg, 4)
        self.screen.blit(title, (title_x, 50))
        
        # Character grid - perfectly centered
        num_chars = len(c.CHARACTERS)
        box_width = 120
        box_height = 140
        gap = 30
        total_width = num_chars * box_width + (num_chars - 1) * gap
        start_x = (c.SCREEN_WIDTH - total_width) // 2
        start_y = 180
        
        for i, char in enumerate(c.CHARACTERS):
            x = start_x + i * (box_width + gap)
            y = start_y
            
            # Character box with shadow
            shadow_rect = pygame.Rect(x + 4, y + 4, box_width, box_height)
            char_rect = pygame.Rect(x, y, box_width, box_height)
            
            pygame.draw.rect(self.screen, c.BLACK, shadow_rect)
            pygame.draw.rect(self.screen, char['color'], char_rect)
            pygame.draw.rect(self.screen, c.WHITE, char_rect, 3)
            
            # Character name - centered
            name = self.text_renderer.render(char['name'], 'medium', c.WHITE)
            name_x = x + box_width // 2 - name.get_width() // 2
            self.screen.blit(name, (name_x, y + box_height + 10))
            
            # Description - centered
            desc = self.text_renderer.render(char['desc'], 'small', c.GRAY)
            desc_x = x + box_width // 2 - desc.get_width() // 2
            self.screen.blit(desc, (desc_x, y + box_height + 35))
            
            # Stats - centered
            stats = f"HP:{char['health']} SPD:{char['speed']}"
            stats_surf = self.text_renderer.render(stats, 'small', c.GRAY)
            stats_x = x + box_width // 2 - stats_surf.get_width() // 2
            self.screen.blit(stats_surf, (stats_x, y + box_height + 55))
            
            # P1 selection indicator
            if i == self.p1_cursor:
                color = c.YELLOW if self.p1_selected else c.RED
                pygame.draw.rect(self.screen, color, char_rect.inflate(10, 10), 5)
                
                p1_label = self.text_renderer.render("P1", 'medium', c.RED)
                label_x = x + box_width // 2 - p1_label.get_width() // 2
                self.screen.blit(p1_label, (label_x, y - 35))
                
                if self.p1_selected:
                    ready = self.text_renderer.render("READY!", 'small', c.YELLOW)
                    ready_x = x + box_width // 2 - ready.get_width() // 2
                    self.screen.blit(ready, (ready_x, y + box_height + 75))
            
            # P2 selection indicator
            if i == self.p2_cursor:
                color = c.YELLOW if self.p2_selected else c.BLUE
                offset = 6 if i == self.p1_cursor else 0
                pygame.draw.rect(self.screen, color, char_rect.inflate(10 + offset * 2, 10 + offset * 2), 5)
                
                p2_label = self.text_renderer.render("P2", 'medium', c.BLUE)
                label_x = x + box_width // 2 - p2_label.get_width() // 2
                y_pos = y + box_height + 95 if i == self.p1_cursor else y + box_height + 75
                self.screen.blit(p2_label, (label_x, y_pos))
                
                if self.p2_selected:
                    ready = self.text_renderer.render("READY!", 'small', c.YELLOW)
                    ready_x = x + box_width // 2 - ready.get_width() // 2
                    self.screen.blit(ready, (ready_x, y_pos + 20))
    
    # ==================== FIGHT STATE ====================
    
    def _start_fight(self):
        """Initialize a new fight with selected characters"""
        # P1 controls
        controls_p1 = {
            'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
            'light': pygame.K_j, 'heavy': pygame.K_k, 'kick': pygame.K_l, 'special': pygame.K_i
        }
        # P2 controls
        controls_p2 = {
            'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP,
            'light': pygame.K_KP1, 'heavy': pygame.K_KP2, 'kick': pygame.K_KP3, 'special': pygame.K_KP0
        }
        
        # Create fighters
        stats_p1 = c.CHARACTERS[self.p1_cursor]
        stats_p2 = c.CHARACTERS[self.p2_cursor]
        
        self.p1 = Fighter(200, 200, stats_p1, controls_p1, is_p2=False)
        self.p2 = Fighter(550, 200, stats_p2, controls_p2, is_p2=True)
        
        # Reset fight variables
        self.round_timer = 99
        self.particles = []
        self.state = "FIGHT"
        self.last_timer_update = pygame.time.get_ticks()
    
    def _update_fight(self):
        """Update fight logic"""
        # Update timer
        if pygame.time.get_ticks() - self.last_timer_update > 1000:
            self.round_timer -= 1
            self.last_timer_update = pygame.time.get_ticks()
        
        # Check win conditions
        if self.p1.health <= 0 or self.p2.health <= 0 or self.round_timer <= 0:
            self.state = "GAME_OVER"
        
        # Update fighters
        self.p1.move(self.p2, c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        self.p2.move(self.p1, c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        self.p1.update()
        self.p2.update()
        
        # Spawn particles on hit
        if self.p1.attacking and self.p1.attack_rect and self.p1.attack_rect.colliderect(self.p2.rect):
            self._spawn_particles(self.p2.rect.centerx, self.p2.rect.centery, c.RED)
        if self.p2.attacking and self.p2.attack_rect and self.p2.attack_rect.colliderect(self.p1.rect):
            self._spawn_particles(self.p1.rect.centerx, self.p1.rect.centery, c.BLUE)
        
        # Update particles
        for p in self.particles[:]:
            p.update()
            if p.timer <= 0:
                self.particles.remove(p)
    
    def _draw_fight(self):
        """Render fight screen with vintage arcade HUD"""
        # Draw retro grid floor
        pygame.draw.rect(self.screen, (20, 20, 30), (0, c.FLOOR_Y, c.SCREEN_WIDTH, c.SCREEN_HEIGHT - c.FLOOR_Y))
        for x in range(0, c.SCREEN_WIDTH, 50):
            pygame.draw.line(self.screen, (50, 50, 100), (x, c.FLOOR_Y), 
                           (x - (x - c.SCREEN_WIDTH // 2), c.SCREEN_HEIGHT), 1)
        pygame.draw.line(self.screen, c.WHITE, (0, c.FLOOR_Y), (c.SCREEN_WIDTH, c.FLOOR_Y), 2)
        
        # Draw fighters
        self.p1.draw(self.screen)
        self.p2.draw(self.screen)
        
        # Draw particles
        for p in self.particles:
            p.draw(self.screen)
        
        # Draw HUD
        self._draw_fight_hud()
    
    def _draw_fight_hud(self):
        """Draw vintage arcade-style HUD"""
        bar_width = 300
        bar_height = 30
        power_bar_height = 15
        
        # P1 health bar
        ratio_p1 = max(0, self.p1.health / self.p1.max_health)
        pygame.draw.rect(self.screen, c.BLACK, (18, 18, bar_width + 4, bar_height + 4))
        pygame.draw.rect(self.screen, c.DARK_GRAY, (20, 20, bar_width, bar_height))
        pygame.draw.rect(self.screen, c.RED, (20, 20, bar_width * ratio_p1, bar_height))
        pygame.draw.rect(self.screen, c.WHITE, (20, 20, bar_width, bar_height), 3)
        
        # P1 power bar
        power_ratio_p1 = max(0, self.p1.power / self.p1.max_power)
        power_y = 55
        pygame.draw.rect(self.screen, c.BLACK, (18, power_y - 2, bar_width + 4, power_bar_height + 4))
        pygame.draw.rect(self.screen, c.DARK_GRAY, (20, power_y, bar_width, power_bar_height))
        pygame.draw.rect(self.screen, c.YELLOW, (20, power_y, bar_width * power_ratio_p1, power_bar_height))
        pygame.draw.rect(self.screen, c.ORANGE, (20, power_y, bar_width, power_bar_height), 2)
        
        # P2 health bar
        ratio_p2 = max(0, self.p2.health / self.p2.max_health)
        p2_x = c.SCREEN_WIDTH - 20 - bar_width
        pygame.draw.rect(self.screen, c.BLACK, (p2_x - 2, 18, bar_width + 4, bar_height + 4))
        pygame.draw.rect(self.screen, c.DARK_GRAY, (p2_x, 20, bar_width, bar_height))
        pygame.draw.rect(self.screen, c.BLUE, (p2_x, 20, bar_width * ratio_p2, bar_height))
        pygame.draw.rect(self.screen, c.WHITE, (p2_x, 20, bar_width, bar_height), 3)
        
        # P2 power bar
        power_ratio_p2 = max(0, self.p2.power / self.p2.max_power)
        pygame.draw.rect(self.screen, c.BLACK, (p2_x - 2, power_y - 2, bar_width + 4, power_bar_height + 4))
        pygame.draw.rect(self.screen, c.DARK_GRAY, (p2_x, power_y, bar_width, power_bar_height))
        pygame.draw.rect(self.screen, c.YELLOW, (p2_x, power_y, bar_width * power_ratio_p2, power_bar_height))
        pygame.draw.rect(self.screen, c.ORANGE, (p2_x, power_y, bar_width, power_bar_height), 2)
        
        # Player names
        p1_name = self.text_renderer.render(self.p1.stats['name'], 'small', c.WHITE)
        self.screen.blit(p1_name, (25, 75))
        
        p2_name = self.text_renderer.render(self.p2.stats['name'], 'small', c.WHITE)
        self.screen.blit(p2_name, (p2_x, 75))
        
        # Combo counters
        if self.p1.combo_count > 1:
            combo_text = self.text_renderer.render(f"{self.p1.combo_count} HIT COMBO!", 'medium', c.YELLOW)
            self.screen.blit(combo_text, (25, 95))
        
        if self.p2.combo_count > 1:
            combo_text = self.text_renderer.render(f"{self.p2.combo_count} HIT COMBO!", 'medium', c.YELLOW)
            combo_x = p2_x + bar_width - combo_text.get_width()
            self.screen.blit(combo_text, (combo_x, 95))
        
        # Timer
        t_color = c.WHITE if self.round_timer > 10 else c.RED
        timer = self.text_renderer.render(str(self.round_timer), 'large', t_color)
        timer_x = c.SCREEN_WIDTH // 2 - timer.get_width() // 2
        timer_bg = pygame.Rect(timer_x - 15, 8, timer.get_width() + 30, timer.get_height() + 10)
        pygame.draw.rect(self.screen, c.BLACK, timer_bg)
        pygame.draw.rect(self.screen, c.ORANGE, timer_bg, 3)
        self.screen.blit(timer, (timer_x, 10))
        
        # FIGHT! text at start
        if self.round_timer > 96:
            fight_text = self.text_renderer.render("FIGHT!", 'large', c.YELLOW)
            fight_x = c.SCREEN_WIDTH // 2 - fight_text.get_width() // 2
            fight_bg = pygame.Rect(fight_x - 20, c.SCREEN_HEIGHT // 2 - 50, 
                                  fight_text.get_width() + 40, 90)
            pygame.draw.rect(self.screen, c.BLACK, fight_bg)
            pygame.draw.rect(self.screen, c.ORANGE, fight_bg, 5)
            self.screen.blit(fight_text, (fight_x, c.SCREEN_HEIGHT // 2 - 30))
    
    # ==================== GAME OVER STATE ====================
    
    def _update_game_over(self, mouse_pos, mouse_clicked):
        """Update game over logic"""
        pass
    
    def _draw_game_over(self):
        """Render game over screen"""
        # Draw faded fight background
        self._draw_fight()
        
        # Dark overlay
        overlay = pygame.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(c.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Determine winner
        if self.p1.health > self.p2.health:
            winner_text = f"{self.p1.stats['name']} WINS!"
            color = c.RED
        elif self.p2.health > self.p1.health:
            winner_text = f"{self.p2.stats['name']} WINS!"
            color = c.BLUE
        else:
            winner_text = "DOUBLE K.O!"
            color = c.YELLOW
        
        # Winner announcement
        winner = self.text_renderer.render(winner_text, 'large', color)
        winner_x = c.SCREEN_WIDTH // 2 - winner.get_width() // 2
        winner_bg = pygame.Rect(winner_x - 30, 150, winner.get_width() + 60, 90)
        pygame.draw.rect(self.screen, c.BLACK, winner_bg)
        pygame.draw.rect(self.screen, color, winner_bg, 5)
        self.screen.blit(winner, (winner_x, 170))
        
        # Subtitle
        subtitle = self.text_renderer.render("GAME OVER", 'medium', c.WHITE)
        subtitle_x = c.SCREEN_WIDTH // 2 - subtitle.get_width() // 2
        self.screen.blit(subtitle, (subtitle_x, 280))
        
        # Restart prompt (blinking)
        if pygame.time.get_ticks() % 1000 < 500:
            prompt = self.text_renderer.render("PRESS ENTER TO CONTINUE", 'medium', c.YELLOW)
            prompt_x = c.SCREEN_WIDTH // 2 - prompt.get_width() // 2
            self.screen.blit(prompt, (prompt_x, 400))
    
    # ==================== HELPER METHODS ====================
    
    def _spawn_particles(self, x, y, color):
        """Spawn particle effects at position"""
        for _ in range(5):
            vx = random.uniform(-5, 5)
            vy = random.uniform(-5, -2)
            self.particles.append(Particle(x, y, color, (vx, vy)))
