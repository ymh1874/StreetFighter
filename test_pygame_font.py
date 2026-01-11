import pygame

# Initialize Pygame
pygame.init()

# Test Font Module
try:
    font = pygame.font.SysFont("Arial", 24)
    print("Font module is working correctly.")
except NotImplementedError as e:
    print("Font module is not available:", e)

pygame.quit()