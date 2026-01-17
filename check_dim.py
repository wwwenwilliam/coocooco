import pygame
try:
    pygame.init()
    img = pygame.image.load("happy.png")
    print(f"DIMENSIONS: {img.get_size()}")
except Exception as e:
    print(f"ERROR: {e}")
