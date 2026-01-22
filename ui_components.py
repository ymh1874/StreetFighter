"""
UI Components for CMUQ Arena - Vintage Arcade Fighter
Contains reusable UI elements like buttons, text renderers, and visual effects
"""

import pygame
import config as c

class Button:
    """
    A vintage arcade-style button that supports both mouse and keyboard interaction
    Features: hover effects, click detection, visual feedback
    """
    def __init__(self, x, y, width, height, text, color=c.ORANGE, text_color=c.WHITE):
        """
        Initialize a button with position, size, and styling
        
        Args:
            x, y: Top-left position of button
            width, height: Button dimensions
            text: Button label text
            color: Button background color
            text_color: Text color
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hover = False
        self.selected = False
        
        # Vintage arcade colors
        self.border_color = c.YELLOW
        self.shadow_color = c.BLACK
        self.hover_color = c.YELLOW
        
    def update(self, mouse_pos):
        """Update hover state based on mouse position"""
        self.hover = self.rect.collidepoint(mouse_pos)
        
    def draw(self, surface, text_renderer):
        """
        Draw the button with vintage arcade styling
        
        Args:
            surface: Pygame surface to draw on
            text_renderer: Text renderer instance for drawing text
        """
        # Shadow effect for depth
        shadow_rect = self.rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(surface, self.shadow_color, shadow_rect)
        
        # Determine button color based on state
        if self.hover or self.selected:
            btn_color = self.hover_color
            current_text_color = c.BLACK
            border_width = 5
        else:
            btn_color = self.color
            current_text_color = self.text_color
            border_width = 3
            
        # Draw button background
        pygame.draw.rect(surface, btn_color, self.rect)
        
        # Draw double border for vintage arcade look
        pygame.draw.rect(surface, self.border_color, self.rect, border_width)
        inner_rect = self.rect.inflate(-10, -10)
        pygame.draw.rect(surface, c.WHITE, inner_rect, 2)
        
        # Draw centered text
        text_surf = text_renderer.render(self.text, 'medium', current_text_color)
        text_x = self.rect.centerx - text_surf.get_width() // 2
        text_y = self.rect.centery - text_surf.get_height() // 2
        surface.blit(text_surf, (text_x, text_y))
        
    def is_clicked(self, mouse_pos, mouse_clicked):
        """Check if button was clicked"""
        return self.rect.collidepoint(mouse_pos) and mouse_clicked


class VintageTextRenderer:
    """
    Custom text renderer with vintage arcade styling
    Attempts to use PIL/Pillow, falls back to simple rendering
    """
    def __init__(self):
        self.use_pil = False
        try:
            from PIL import Image, ImageDraw, ImageFont
            self.use_pil = True
            self.Image = Image
            self.ImageDraw = ImageDraw
            self.ImageFont = ImageFont
            
            # Try to load retro fonts
            try:
                self.pil_font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
                self.pil_font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
                self.pil_font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
            except:
                # Fallback to default font
                self.pil_font_small = ImageFont.load_default()
                self.pil_font_medium = ImageFont.load_default()
                self.pil_font_large = ImageFont.load_default()
        except ImportError:
            self.use_pil = False
    
    def render(self, text, size='medium', color=(255, 255, 255)):
        """
        Render text and return a pygame surface
        
        Args:
            text: String to render
            size: 'small', 'medium', or 'large'
            color: RGB tuple for text color
            
        Returns:
            Pygame surface with rendered text
        """
        if self.use_pil:
            return self._render_with_pil(text, size, color)
        else:
            return self._render_simple(text, size, color)
    
    def _render_with_pil(self, text, size, color):
        """Render text using PIL/Pillow for better quality"""
        # Select font based on size
        if size == 'small':
            font = self.pil_font_small
            height = 30
        elif size == 'large':
            font = self.pil_font_large
            height = 70
        else:  # medium
            font = self.pil_font_medium
            height = 40
        
        # Create PIL image
        img = self.Image.new('RGBA', (1000, height), (0, 0, 0, 0))
        draw = self.ImageDraw.Draw(img)
        draw.text((0, 0), text, font=font, fill=color)
        
        # Convert to pygame surface
        mode = img.mode
        size = img.size
        data = img.tobytes()
        surface = pygame.image.fromstring(data, size, mode)
        
        # Crop to actual text size
        bbox = surface.get_bounding_rect()
        if bbox.width > 0:
            surface = surface.subsurface(bbox)
        
        return surface
    
    def _render_simple(self, text, size, color):
        """Fallback: simple block rendering for retro look"""
        # Character dimensions based on size
        if size == 'small':
            char_w, char_h, spacing = 6, 10, 2
        elif size == 'large':
            char_w, char_h, spacing = 16, 24, 4
        else:  # medium
            char_w, char_h, spacing = 10, 16, 3
        
        # Create surface
        width = len(text) * (char_w + spacing)
        surface = pygame.Surface((width, char_h), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        
        # Draw simple blocks for each character
        for i, char in enumerate(text):
            x = i * (char_w + spacing)
            if char != ' ':
                # Main character block
                pygame.draw.rect(surface, color, (x, 0, char_w, char_h))
                # Inner detail for vintage look
                pygame.draw.rect(surface, (0, 0, 0, 100), (x + 2, 2, char_w - 4, char_h - 4))
        
        return surface


class ArcadeFrame:
    """Draws a vintage arcade cabinet frame around the game area"""
    
    @staticmethod
    def draw(surface):
        """
        Draw arcade cabinet decorations
        
        Args:
            surface: Pygame surface to draw on
        """
        width = surface.get_width()
        height = surface.get_height()
        
        # Top arcade marquee
        pygame.draw.rect(surface, c.BLACK, (0, 0, width, 8))
        pygame.draw.rect(surface, c.ORANGE, (0, 0, width, 4))
        pygame.draw.rect(surface, c.YELLOW, (0, 4, width, 2))
        
        # Bottom cabinet base
        pygame.draw.rect(surface, c.BLACK, (0, height - 8, width, 8))
        pygame.draw.rect(surface, c.YELLOW, (0, height - 6, width, 2))
        pygame.draw.rect(surface, c.ORANGE, (0, height - 4, width, 4))
        
        # Side panels
        pygame.draw.rect(surface, c.BLACK, (0, 0, 4, height))
        pygame.draw.rect(surface, c.BLACK, (width - 4, 0, 4, height))
        
        # Corner decorations
        corner_size = 20
        # Top-left
        pygame.draw.circle(surface, c.ORANGE, (corner_size, corner_size), 8)
        # Top-right
        pygame.draw.circle(surface, c.ORANGE, (width - corner_size, corner_size), 8)
        # Bottom-left
        pygame.draw.circle(surface, c.ORANGE, (corner_size, height - corner_size), 8)
        # Bottom-right
        pygame.draw.circle(surface, c.ORANGE, (width - corner_size, height - corner_size), 8)


class ScanlineEffect:
    """Creates vintage CRT scanline effect"""
    
    def __init__(self, width, height):
        """Initialize scanline surface"""
        self.surface = pygame.Surface((width, height))
        self.surface.set_colorkey(c.BLACK)
        self.surface.set_alpha(40)
        
        # Draw horizontal scanlines
        for y in range(0, height, 3):
            pygame.draw.line(self.surface, (0, 0, 0), (0, y), (width, y), 1)
    
    def draw(self, surface):
        """Apply scanline effect to surface"""
        surface.blit(self.surface, (0, 0))
