import pygame

class SimpleTextRenderer:
    """Custom text renderer using PIL/Pillow as fallback"""
    def __init__(self):
        self.use_pil = False
        try:
            from PIL import Image, ImageDraw, ImageFont
            self.use_pil = True
            self.Image = Image
            self.ImageDraw = ImageDraw
            self.ImageFont = ImageFont
            # Try to load a default font
            try:
                self.pil_font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
                self.pil_font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
                self.pil_font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
            except:
                self.pil_font_small = ImageFont.load_default()
                self.pil_font_medium = ImageFont.load_default()
                self.pil_font_large = ImageFont.load_default()
        except ImportError:
            self.use_pil = False
    
    def render(self, text, size='medium', color=(255, 255, 255)):
        """Render text and return a pygame surface"""
        if self.use_pil:
            return self._render_with_pil(text, size, color)
        else:
            return self._render_simple(text, size, color)
    
    def _render_with_pil(self, text, size, color):
        """Render text using PIL/Pillow"""
        # Select font based on size
        if size == 'small':
            font = self.pil_font_small
            height = 30
        elif size == 'large':
            font = self.pil_font_large
            height = 80
        else:  # medium
            font = self.pil_font_medium
            height = 40
        
        # Create PIL image
        img = self.Image.new('RGBA', (800, height), (0, 0, 0, 0))
        draw = self.ImageDraw.Draw(img)
        draw.text((0, 0), text, font=font, fill=color)
        
        # Convert PIL image to pygame surface
        mode = img.mode
        size = img.size
        data = img.tobytes()
        surface = pygame.image.fromstring(data, size, mode)
        
        return surface
    
    def _render_simple(self, text, size, color):
        """Simple fallback: render text as colored blocks"""
        # Character dimensions based on size
        if size == 'small':
            char_w, char_h, spacing = 8, 12, 2
        elif size == 'large':
            char_w, char_h, spacing = 20, 30, 5
        else:  # medium
            char_w, char_h, spacing = 12, 18, 3
        
        # Create surface
        width = len(text) * (char_w + spacing)
        surface = pygame.Surface((width, char_h), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        
        # Draw simple blocks for each character
        for i, char in enumerate(text):
            x = i * (char_w + spacing)
            if char != ' ':
                # Draw a simple rectangle for each character
                pygame.draw.rect(surface, color, (x, 0, char_w, char_h))
                # Add a small detail to make it look less blocky
                pygame.draw.rect(surface, (0, 0, 0, 100), (x + 2, 2, char_w - 4, char_h - 4))
        
        return surface
