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
import os
import config as c
from entities import Fighter, Particle, SpinningKickEffect, HitEffect, Projectile
from ui_components import Button, VintageTextRenderer, ArcadeFrame, ScanlineEffect
from combat import CombatSystem
from ai_controller import AIController
import drawing


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
        
        # Visual effects
        self.scanlines = ScanlineEffect(c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        self.screen_shake = 0
        self.screen_shake_offset = (0, 0)
        self.hit_effects = []  # Comic book hit effects
        self.ko_slowdown = False
        self.slowdown_timer = 0
        
        # Set random seed for consistent ground texture
        random.seed(42)
        
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
        self.p2_coin_inserted = False  # Requires coin insertion for P2
        self.p2_is_ai = True  # P2 starts as AI by default
        
    def _init_fight_screen(self):
        """Initialize fight screen variables"""
        self.p1 = None
        self.p2 = None
        self.p2_ai = None  # AI controller for P2 if needed
        self.round_timer = 99
        self.last_timer_update = 0
        self.particles = []
        self.projectiles = []
        self.special_effects = []
        self.combat_system = CombatSystem()  # Combat system for tracking combos
        self.winner_sequence_active = False
        self.winner_sequence_frame = 0
    
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
            # Coin insertion for P2 (press '5' key like arcade machines)
            if key == pygame.K_5:
                if not self.p2_coin_inserted:
                    self.p2_coin_inserted = True
                    self.p2_is_ai = False
                    
            # P1 controls
            if not self.p1_selected:
                if key == pygame.K_a:
                    self.p1_cursor = (self.p1_cursor - 1) % len(c.CHARACTERS)
                elif key == pygame.K_d:
                    self.p1_cursor = (self.p1_cursor + 1) % len(c.CHARACTERS)
                elif key == pygame.K_j:
                    self.p1_selected = True
            
            # P2 controls (only if coin inserted)
            if not self.p2_selected and self.p2_coin_inserted and not self.p2_is_ai:
                if key == pygame.K_LEFT:
                    self.p2_cursor = (self.p2_cursor - 1) % len(c.CHARACTERS)
                elif key == pygame.K_RIGHT:
                    self.p2_cursor = (self.p2_cursor + 1) % len(c.CHARACTERS)
                elif key == pygame.K_KP1:
                    self.p2_selected = True
            
            # Auto-select for AI
            if self.p2_is_ai and self.p1_selected and not self.p2_selected:
                self.p2_selected = True
                    
        # Game over screen
        elif self.state == "GAME_OVER":
            if key == pygame.K_RETURN:
                # Reset character selection for next game
                self.p1_selected = False
                self.p2_selected = False
                self.p1_cursor = 0
                self.p2_cursor = 0
                self.p2_coin_inserted = False
                self.p2_is_ai = True
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
        
        # Controls panel - made taller to fit all text
        panel_rect = pygame.Rect(100, 120, c.SCREEN_WIDTH - 200, 410)
        pygame.draw.rect(self.screen, c.BLACK, panel_rect)
        pygame.draw.rect(self.screen, c.ORANGE, panel_rect, 3)
        
        # Player 1 controls
        y_offset = 140
        p1_title = self.text_renderer.render("PLAYER 1", 'medium', c.RED)
        self.screen.blit(p1_title, (120, y_offset))
        
        y_offset += 35
        controls_p1 = [
            ("MOVE:", "W/A/S/D"),
            ("LIGHT PUNCH:", "J"),
            ("HEAVY PUNCH:", "K"),
            ("LIGHT KICK:", "L"),
            ("HEAVY KICK:", "I"),
            ("SPECIAL:", "U"),
            ("DASH:", "LEFT SHIFT"),
            ("PARRY:", "O"),
            ("BLOCK:", "HOLD DOWN (S)"),
        ]
        
        for label, key in controls_p1:
            label_surf = self.text_renderer.render(label, 'small', c.WHITE)
            key_surf = self.text_renderer.render(key, 'small', c.YELLOW)
            self.screen.blit(label_surf, (120, y_offset))
            self.screen.blit(key_surf, (350, y_offset))
            y_offset += 22
        
        # Player 2 controls
        y_offset = 140
        p2_title = self.text_renderer.render("PLAYER 2", 'medium', c.BLUE)
        self.screen.blit(p2_title, (450, y_offset))
        
        y_offset += 35
        controls_p2 = [
            ("MOVE:", "ARROW KEYS"),
            ("LIGHT PUNCH:", "NUMPAD 1"),
            ("HEAVY PUNCH:", "NUMPAD 2"),
            ("LIGHT KICK:", "NUMPAD 3"),
            ("HEAVY KICK:", "NUMPAD 4"),
            ("SPECIAL:", "NUMPAD 0"),
            ("DASH:", "RIGHT SHIFT"),
            ("PARRY:", "NUMPAD 5"),
            ("BLOCK:", "HOLD DOWN ARROW"),
        ]
        
        for label, key in controls_p2:
            label_surf = self.text_renderer.render(label, 'small', c.WHITE)
            key_surf = self.text_renderer.render(key, 'small', c.YELLOW)
            self.screen.blit(label_surf, (450, y_offset))
            self.screen.blit(key_surf, (450, y_offset + 16))
            y_offset += 22
        
        # Coin insertion note
        coin_note = self.text_renderer.render("PRESS '5' TO INSERT COIN FOR PLAYER 2", 'small', c.GREEN)
        coin_x = c.SCREEN_WIDTH // 2 - coin_note.get_width() // 2
        self.screen.blit(coin_note, (coin_x, 100))
        
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
            "Made by Game Dev Club with Love",
            "Yousef Hussein - Class of 2029",
            "Version 1.0 - Tarnival 2026"
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
            pygame.draw.rect(self.screen, c.GRAY, char_rect)
            pygame.draw.rect(self.screen, c.WHITE, char_rect, 3)
            
            # Draw character portrait (head only, centered in box)
            portrait_x = x + box_width // 2
            portrait_y = y + box_height // 2
            char_name = char['name']
            if 'KHALID' in char_name:
                drawing.draw_khalid(self.screen, portrait_x, portrait_y + 30, True, 'idle', 0)
            elif 'EDUARDO' in char_name:
                drawing.draw_eduardo(self.screen, portrait_x, portrait_y + 30, True, 'idle', 0)
            elif 'HASAN' in char_name:
                drawing.draw_hasan(self.screen, portrait_x, portrait_y + 30, True, 'idle', 0)
            elif 'HAMMOUD' in char_name:
                drawing.draw_hammoud(self.screen, portrait_x, portrait_y + 30, True, 'idle', 0)
            
            # Character name - centered, smaller font
            name = self.text_renderer.render(char['name'], 'small', c.WHITE)
            name_x = x + box_width // 2 - name.get_width() // 2
            self.screen.blit(name, (name_x, y + box_height + 8))
            
            # Description - centered, extra small (use smaller font)
            desc = self.text_renderer.render(char['desc'], 'small', c.GRAY)
            desc_x = x + box_width // 2 - desc.get_width() // 2
            self.screen.blit(desc, (desc_x, y + box_height + 28))
            
            # Stats - centered, extra small
            stats = f"HP:{char['health']} SPD:{char['speed']}"
            stats_surf = self.text_renderer.render(stats, 'small', c.GRAY)
            stats_x = x + box_width // 2 - stats_surf.get_width() // 2
            self.screen.blit(stats_surf, (stats_x, y + box_height + 42))
            
            # P1 selection indicator
            if i == self.p1_cursor:
                color = c.YELLOW if self.p1_selected else c.RED
                pygame.draw.rect(self.screen, color, char_rect.inflate(10, 10), 5)
                
                p1_label = self.text_renderer.render("P1", 'small', c.RED)
                label_x = x + box_width // 2 - p1_label.get_width() // 2
                self.screen.blit(p1_label, (label_x, y - 30))
                
                if self.p1_selected:
                    ready = self.text_renderer.render("READY!", 'small', c.YELLOW)
                    ready_x = x + box_width // 2 - ready.get_width() // 2
                    self.screen.blit(ready, (ready_x, y + box_height + 60))
            
            # P2 selection indicator
            if i == self.p2_cursor:
                # Show different indicator based on coin status
                if not self.p2_coin_inserted or self.p2_is_ai:
                    # AI indicator
                    color = c.PURPLE
                    pygame.draw.rect(self.screen, color, char_rect.inflate(10 + offset * 2, 10 + offset * 2), 5)
                    
                    ai_label = self.text_renderer.render("AI", 'small', c.PURPLE)
                    label_x = x + box_width // 2 - ai_label.get_width() // 2
                    y_pos = y + box_height + 78 if i == self.p1_cursor else y + box_height + 60
                    self.screen.blit(ai_label, (label_x, y_pos))
                else:
                    # P2 human player indicator
                    color = c.YELLOW if self.p2_selected else c.BLUE
                    pygame.draw.rect(self.screen, color, char_rect.inflate(10 + offset * 2, 10 + offset * 2), 5)
                    
                    p2_label = self.text_renderer.render("P2", 'small', c.BLUE)
                    label_x = x + box_width // 2 - p2_label.get_width() // 2
                    y_pos = y + box_height + 78 if i == self.p1_cursor else y + box_height + 60
                    self.screen.blit(p2_label, (label_x, y_pos))
                    
                    if self.p2_selected:
                        ready = self.text_renderer.render("READY!", 'small', c.YELLOW)
                        ready_x = x + box_width // 2 - ready.get_width() // 2
                        self.screen.blit(ready, (ready_x, y_pos + 18))
        
        # Coin insertion prompt
        if not self.p2_coin_inserted or self.p2_is_ai:
            coin_prompt = self.text_renderer.render("PRESS '5' TO INSERT COIN FOR PLAYER 2", 'medium', c.YELLOW)
            coin_x = c.SCREEN_WIDTH // 2 - coin_prompt.get_width() // 2
            self.screen.blit(coin_prompt, (coin_x, 50))
        else:
            mode_text = self.text_renderer.render("2 PLAYER MODE", 'medium', c.GREEN)
            mode_x = c.SCREEN_WIDTH // 2 - mode_text.get_width() // 2
            self.screen.blit(mode_text, (mode_x, 50))
    
    # ==================== FIGHT STATE ====================
    
    def _start_fight(self):
        """Initialize a new fight with selected characters"""
        # Use control configuration from config
        controls_p1 = c.DEFAULT_P1_CONTROLS
        controls_p2 = c.DEFAULT_P2_CONTROLS
        
        # Create fighters at proper ground positions
        stats_p1 = c.CHARACTERS[self.p1_cursor]
        stats_p2 = c.CHARACTERS[self.p2_cursor]
        
        # Spawn fighters on the ground (FLOOR_Y - P_HEIGHT)
        spawn_y = c.FLOOR_Y - c.P_HEIGHT
        self.p1 = Fighter(200, spawn_y, stats_p1, controls_p1, is_p2=False, combat_system=self.combat_system, fighter_id="p1")
        self.p2 = Fighter(550, spawn_y, stats_p2, controls_p2, is_p2=True, combat_system=self.combat_system, fighter_id="p2")
        
        # Initialize AI controller for P2 if needed
        if self.p2_is_ai:
            self.p2_ai = AIController(self.p2, self.p1, difficulty='hard')
        else:
            self.p2_ai = None
        
        # Register fighters with combat system for combo tracking
        self.combat_system.register_fighter("p1")
        self.combat_system.register_fighter("p2")
        
        # Reset ALL fight variables and clear leftover effects
        self.round_timer = 99
        self.particles = []
        self.projectiles = []
        self.special_effects = []
        self.hit_effects = []  # Clear hit effects from previous game
        self.screen_shake = 0  # Reset screen shake
        self.ko_slowdown = False
        self.slowdown_timer = 0
        self.winner_sequence_active = False
        self.winner_sequence_frame = 0
        
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
            # Add KO effect and start winner sequence
            if self.p1.health <= 0:
                self.hit_effects.append(HitEffect(self.p1.rect.centerx, self.p1.rect.centery - 50, 'ko', c.RED))
                if not self.winner_sequence_active:
                    self.winner_sequence_active = True
                    self.winner_sequence_frame = 0
            elif self.p2.health <= 0:
                self.hit_effects.append(HitEffect(self.p2.rect.centerx, self.p2.rect.centery - 50, 'ko', c.BLUE))
                if not self.winner_sequence_active:
                    self.winner_sequence_active = True
                    self.winner_sequence_frame = 0
            elif self.round_timer <= 0:
                if not self.winner_sequence_active:
                    self.winner_sequence_active = True
                    self.winner_sequence_frame = 0
        
        # Winner sequence animation - exactly 3 seconds (180 frames at 60fps)
        if self.winner_sequence_active:
            self.winner_sequence_frame += 1
            
            # Slow motion effect: Skip update on even frames for first 30 frames
            # This creates a slow-mo effect by updating game state at half speed
            is_in_slowmo_window = self.winner_sequence_frame <= 30
            is_even_frame = self.winner_sequence_frame % 2 == 0
            if is_in_slowmo_window and is_even_frame:
                return  # Skip this update to create slow motion
            
            if self.winner_sequence_frame >= 180:  # Exactly 3 seconds
                self.state = "GAME_OVER"
                self.winner_sequence_active = False
                self.winner_sequence_frame = 0
            return  # Don't update fight during winner sequence
        
        # Update screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1
            shake_amount = min(self.screen_shake, 5)
            self.screen_shake_offset = (
                random.randint(-shake_amount, shake_amount),
                random.randint(-shake_amount, shake_amount)
            )
        else:
            self.screen_shake_offset = (0, 0)
        
        # Update AI controller if active
        if self.p2_ai:
            self.p2_ai.update(self.projectiles)
        
        # Update fighters and handle special moves
        result1 = self.p1.move(self.p2, c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        result2 = self.p2.move(self.p1, c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        
        # Handle special move results
        for result in [result1, result2]:
            if result is not None:
                if isinstance(result, list):
                    # Multiple projectiles (pizza throw)
                    self.projectiles.extend(result)
                elif isinstance(result, SpinningKickEffect):
                    # Special effect (spinning kick)
                    self.special_effects.append(result)
                elif hasattr(result, 'active'):
                    # Single projectile
                    self.projectiles.append(result)
        
        self.p1.update()
        self.p2.update()
        
        # Update and handle projectiles
        for proj in self.projectiles[:]:
            proj.update()
            if not proj.active:
                self.projectiles.remove(proj)
                continue
            
            # Check collision with fighters
            proj_rect = proj.get_rect()
            if proj.owner == self.p1 and proj_rect.colliderect(self.p2.rect):
                # Check if p2 is parrying
                if self.p2.parrying and self.p2.parry_window > 0:
                    # Successful parry - reflect projectile
                    proj.vel_x = -proj.vel_x  # Reverse horizontal velocity
                    proj.owner = self.p2  # Change ownership to p2
                    self.p2.parry_success = True
                    self.p2.color_flash = 10
                    self._spawn_particles(self.p2.rect.centerx, self.p2.rect.centery, c.YELLOW)
                    self.hit_effects.append(HitEffect(self.p2.rect.centerx, self.p2.rect.centery, 'parry', c.YELLOW))
                else:
                    # Apply combo damage scaling
                    damage = proj.damage
                    if self.p1.combat_system and self.p1.fighter_id:
                        self.p1.combat_system.increment_combo(self.p1.fighter_id)
                        combo_multiplier = self.p1.combat_system.get_combo_damage_multiplier(self.p1.fighter_id)
                        damage *= combo_multiplier
                    
                    self.p2.take_damage(damage, 10, 15, self.p1.facing_right)
                    self._spawn_particles(self.p2.rect.centerx, self.p2.rect.centery, c.ORANGE)
                    self.hit_effects.append(HitEffect(self.p2.rect.centerx, self.p2.rect.centery, 'special', c.ORANGE))
                    self.screen_shake = 8
                    proj.active = False
            elif proj.owner == self.p2 and proj_rect.colliderect(self.p1.rect):
                # Check if p1 is parrying
                if self.p1.parrying and self.p1.parry_window > 0:
                    # Successful parry - reflect projectile
                    proj.vel_x = -proj.vel_x  # Reverse horizontal velocity
                    proj.owner = self.p1  # Change ownership to p1
                    self.p1.parry_success = True
                    self.p1.color_flash = 10
                    self._spawn_particles(self.p1.rect.centerx, self.p1.rect.centery, c.YELLOW)
                    self.hit_effects.append(HitEffect(self.p1.rect.centerx, self.p1.rect.centery, 'parry', c.YELLOW))
                else:
                    # Apply combo damage scaling
                    damage = proj.damage
                    if self.p2.combat_system and self.p2.fighter_id:
                        self.p2.combat_system.increment_combo(self.p2.fighter_id)
                        combo_multiplier = self.p2.combat_system.get_combo_damage_multiplier(self.p2.fighter_id)
                        damage *= combo_multiplier
                    
                    self.p1.take_damage(damage, 10, 15, self.p2.facing_right)
                    self._spawn_particles(self.p1.rect.centerx, self.p1.rect.centery, c.ORANGE)
                    self.hit_effects.append(HitEffect(self.p1.rect.centerx, self.p1.rect.centery, 'special', c.ORANGE))
                    self.screen_shake = 8
                    proj.active = False
        
        # Update special effects
        for effect in self.special_effects[:]:
            effect.update()
            if not effect.active:
                self.special_effects.remove(effect)
                continue
            
            # Check for spinning kick hits
            if isinstance(effect, SpinningKickEffect) and effect.can_hit():
                target = self.p2 if effect.fighter == self.p1 else self.p1
                attacker = effect.fighter
                kick_rect = pygame.Rect(attacker.rect.x - 30, attacker.rect.y - 30, 
                                       attacker.rect.width + 60, attacker.rect.height + 60)
                if kick_rect.colliderect(target.rect):
                    # Apply combo damage scaling
                    damage = 8
                    if attacker.combat_system and attacker.fighter_id:
                        attacker.combat_system.increment_combo(attacker.fighter_id)
                        combo_multiplier = attacker.combat_system.get_combo_damage_multiplier(attacker.fighter_id)
                        damage *= combo_multiplier
                    
                    target.take_damage(damage, 15, 10, attacker.facing_right)
                    effect.register_hit()
                    self._spawn_particles(target.rect.centerx, target.rect.centery, c.ORANGE)
                    self.hit_effects.append(HitEffect(target.rect.centerx, target.rect.centery, 'heavy', c.ORANGE))
                    self.screen_shake = 10
        
        # Spawn particles on hit
        if self.p1.attacking and self.p1.attack_rect and self.p1.attack_rect.colliderect(self.p2.rect):
            self._spawn_particles(self.p2.rect.centerx, self.p2.rect.centery, c.RED)
            # Add hit effect based on attack type with randomness
            effect_type = 'heavy' if 'heavy' in self.p1.attack_type else 'light'
            # Higher chance for heavy attacks (80%), lower for light (30%)
            chance = 0.8 if effect_type == 'heavy' else 0.3
            if random.random() < chance:
                # Position text higher to avoid blood splash overlap (move up by 40 pixels)
                self.hit_effects.append(HitEffect(self.p2.rect.centerx, self.p2.rect.centery - 40, effect_type, c.RED))
            if effect_type == 'heavy':
                self.screen_shake = 10
        if self.p2.attacking and self.p2.attack_rect and self.p2.attack_rect.colliderect(self.p1.rect):
            self._spawn_particles(self.p1.rect.centerx, self.p1.rect.centery, c.BLUE)
            effect_type = 'heavy' if 'heavy' in self.p2.attack_type else 'light'
            # Higher chance for heavy attacks (80%), lower for light (30%)
            chance = 0.8 if effect_type == 'heavy' else 0.3
            if random.random() < chance:
                # Position text higher to avoid blood splash overlap (move up by 40 pixels)
                self.hit_effects.append(HitEffect(self.p1.rect.centerx, self.p1.rect.centery - 40, effect_type, c.BLUE))
            if effect_type == 'heavy':
                self.screen_shake = 10
        
        # Update particles
        for p in self.particles[:]:
            p.update()
            if p.timer <= 0:
                self.particles.remove(p)
        
        # Update hit effects
        for effect in self.hit_effects[:]:
            effect.update()
            if not effect.active:
                self.hit_effects.remove(effect)
    
    def _draw_fight(self):
        """Render fight screen with vintage arcade HUD"""
        # Apply screen shake offset
        shake_x, shake_y = self.screen_shake_offset
        
        # Draw brown dirt floor (no perspective grid)
        dirt_floor = pygame.Rect(0 + shake_x, c.FLOOR_Y + shake_y, c.SCREEN_WIDTH, c.SCREEN_HEIGHT - c.FLOOR_Y)
        pygame.draw.rect(self.screen, c.DIRT_BROWN, dirt_floor)
        
        # Add subtle texture with random darker spots (using consistent seed from __init__)
        for _ in range(50):
            spot_x = random.randint(0, c.SCREEN_WIDTH)
            spot_y = random.randint(c.FLOOR_Y, c.SCREEN_HEIGHT)
            spot_size = random.randint(3, 8)
            darker_brown = (int(c.DIRT_BROWN[0] * 0.8), int(c.DIRT_BROWN[1] * 0.8), int(c.DIRT_BROWN[2] * 0.8))
            pygame.draw.circle(self.screen, darker_brown, (spot_x + shake_x, spot_y + shake_y), spot_size)
        
        # Floor line
        pygame.draw.line(self.screen, (100, 60, 25), (0 + shake_x, c.FLOOR_Y + shake_y), 
                        (c.SCREEN_WIDTH + shake_x, c.FLOOR_Y + shake_y), 3)
        
        # Create shaken surface for game objects
        if self.screen_shake > 0:
            # Draw everything to a temporary surface then blit with offset
            game_surface = pygame.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT), pygame.SRCALPHA)
            game_surface.fill((0, 0, 0, 0))
        else:
            game_surface = self.screen
            shake_x, shake_y = 0, 0
        
        # Draw fighters (or winner sequence)
        if self.winner_sequence_active:
            # Determine winner and loser
            if self.p1.health <= 0:
                winner = self.p2
                loser = self.p1
            else:
                winner = self.p1
                loser = self.p2
            
            # Draw blood puddle at loser's position
            drawing.draw_blood_puddle(game_surface, loser.rect.centerx, c.FLOOR_Y, 80)
            
            # Draw defeated character on top of blood puddle
            drawing.draw_defeated_character(game_surface, loser.rect.centerx, c.FLOOR_Y,
                                           loser.stats['name'], loser.stats['skin'], loser.stats['color'])
            
            # Draw winner doing victory dance
            drawing.draw_victory_dance(game_surface, winner.rect.centerx, winner.rect.bottom,
                                      winner.stats['name'], winner.stats['skin'], winner.stats['color'],
                                      self.winner_sequence_frame)
        else:
            self.p1.draw(game_surface)
            self.p2.draw(game_surface)
        
        # Draw projectiles
        for proj in self.projectiles:
            proj.draw(game_surface)
        
        # Draw special effects (spinning kick rotation)
        for effect in self.special_effects:
            if isinstance(effect, SpinningKickEffect):
                # Draw rotation effect
                angle = effect.get_rotation_angle()
                # Visual feedback - could draw motion lines
                pass
        
        # Draw particles
        for p in self.particles:
            p.draw(game_surface)
        
        # Draw hit effects
        for effect in self.hit_effects:
            effect.draw(game_surface, self.text_renderer)
        
        # Blit shaken surface if needed
        if self.screen_shake > 0:
            self.screen.blit(game_surface, (shake_x, shake_y))
        
        # Draw HUD (not affected by shake)
        self._draw_fight_hud()
    
    def _draw_fight_hud(self):
        """Draw vintage arcade-style HUD with segmented health bars"""
        bar_width = 300
        bar_height = 30
        num_segments = 10
        segment_width = (bar_width - (num_segments - 1) * 2) / num_segments  # 2px gap between segments
        
        # P1 health bar (segmented)
        ratio_p1 = max(0, self.p1.health / self.p1.max_health)
        pygame.draw.rect(self.screen, c.BLACK, (18, 18, bar_width + 4, bar_height + 4))
        pygame.draw.rect(self.screen, c.DARK_GRAY, (20, 20, bar_width, bar_height))
        
        # Draw segments
        for i in range(num_segments):
            segment_x = 20 + i * (segment_width + 2)
            segment_health = (i + 1) / num_segments
            
            if ratio_p1 >= segment_health:
                # Full segment
                color = c.RED
            elif ratio_p1 > (i / num_segments):
                # Partial segment
                color = c.RED
            else:
                # Empty segment (already dark gray background)
                continue
            
            # Flash on low health
            if ratio_p1 < 0.3 and pygame.time.get_ticks() % 500 < 250:
                color = c.YELLOW
            
            pygame.draw.rect(self.screen, color, (segment_x, 20, segment_width, bar_height))
        
        pygame.draw.rect(self.screen, c.WHITE, (20, 20, bar_width, bar_height), 3)
        
        # P2 health bar (segmented)
        ratio_p2 = max(0, self.p2.health / self.p2.max_health)
        p2_x = c.SCREEN_WIDTH - 20 - bar_width
        pygame.draw.rect(self.screen, c.BLACK, (p2_x - 2, 18, bar_width + 4, bar_height + 4))
        pygame.draw.rect(self.screen, c.DARK_GRAY, (p2_x, 20, bar_width, bar_height))
        
        # Draw segments
        for i in range(num_segments):
            segment_x = p2_x + i * (segment_width + 2)
            segment_health = (i + 1) / num_segments
            
            if ratio_p2 >= segment_health:
                color = c.BLUE
            elif ratio_p2 > (i / num_segments):
                color = c.BLUE
            else:
                continue
            
            # Flash on low health
            if ratio_p2 < 0.3 and pygame.time.get_ticks() % 500 < 250:
                color = c.YELLOW
            
            pygame.draw.rect(self.screen, color, (segment_x, 20, segment_width, bar_height))
        
        pygame.draw.rect(self.screen, c.WHITE, (p2_x, 20, bar_width, bar_height), 3)
        
        # Player names
        p1_name = self.text_renderer.render(self.p1.stats['name'], 'medium', c.WHITE)
        self.screen.blit(p1_name, (25, 55))
        
        p2_name = self.text_renderer.render(self.p2.stats['name'], 'medium', c.WHITE)
        self.screen.blit(p2_name, (p2_x, 55))
        
        # P1 Special ability power bar
        power_bar_width = 150
        power_bar_height = 15
        current_time = pygame.time.get_ticks()
        time_since_special_p1 = current_time - self.p1.last_special_time
        special_cooldown = 2000  # 2 seconds
        power_ratio_p1 = min(1.0, time_since_special_p1 / special_cooldown)
        
        pygame.draw.rect(self.screen, c.BLACK, (18, 78, power_bar_width + 4, power_bar_height + 4))
        pygame.draw.rect(self.screen, c.DARK_GRAY, (20, 80, power_bar_width, power_bar_height))
        if power_ratio_p1 > 0:
            filled_width = int(power_bar_width * power_ratio_p1)
            color = c.YELLOW if power_ratio_p1 >= 1.0 else c.ORANGE
            pygame.draw.rect(self.screen, color, (20, 80, filled_width, power_bar_height))
        pygame.draw.rect(self.screen, c.WHITE, (20, 80, power_bar_width, power_bar_height), 2)
        
        # P2 Special ability power bar
        time_since_special_p2 = current_time - self.p2.last_special_time
        power_ratio_p2 = min(1.0, time_since_special_p2 / special_cooldown)
        
        p2_power_x = c.SCREEN_WIDTH - 20 - power_bar_width
        pygame.draw.rect(self.screen, c.BLACK, (p2_power_x - 2, 78, power_bar_width + 4, power_bar_height + 4))
        pygame.draw.rect(self.screen, c.DARK_GRAY, (p2_power_x, 80, power_bar_width, power_bar_height))
        if power_ratio_p2 > 0:
            filled_width = int(power_bar_width * power_ratio_p2)
            color = c.YELLOW if power_ratio_p2 >= 1.0 else c.ORANGE
            pygame.draw.rect(self.screen, color, (p2_power_x, 80, filled_width, power_bar_height))
        pygame.draw.rect(self.screen, c.WHITE, (p2_power_x, 80, power_bar_width, power_bar_height), 2)
        
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
