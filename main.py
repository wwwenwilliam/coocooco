import pygame
import pygame_gui

# CONFIGURATION
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 844
FULLSCREEN = False


# 1. Initialize Pygame immediately
pygame.init()
import pygame.camera
pygame.camera.init()

pygame.display.set_caption('bIrD')

flags = pygame.RESIZABLE
if FULLSCREEN:
    flags = pygame.FULLSCREEN | pygame.RESIZABLE

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags)

# 2. Show Splash Screen
screen.fill((255, 255, 255))
font = pygame.font.Font(None, 48)
text = font.render("Loading...", True, (0, 0, 0))
text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
screen.blit(text, text_rect)
pygame.display.update()

# 3. Heavy Imports (Now that window is visible)
# This import chain triggers torch/transformers loading
from src.scenes.screen_manager import ScreenManager

manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), 'assets/ui/theme.json')
clock = pygame.time.Clock()

# Create Screen Manager
screen_manager = ScreenManager(manager, (WINDOW_WIDTH, WINDOW_HEIGHT))
screen_manager.setup()

running = True
while running:
    ## clock
    time_delta = clock.tick(60)/1000.0

    ## event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.VIDEORESIZE:
            # Update Window Size
            new_w, new_h = event.w, event.h
            
            # Enforce Minimum Size
            MIN_W, MIN_H = 390, 844
            clamped_w = max(new_w, MIN_W)
            clamped_h = max(new_h, MIN_H)
            
            # Only call set_mode if we needed to clamp to minimum size
            # Otherwise pygame handles the resize automatically without needing set_mode
            if new_w < MIN_W or new_h < MIN_H:
                screen = pygame.display.set_mode((clamped_w, clamped_h), pygame.RESIZABLE)
            
            manager.set_window_resolution((clamped_w, clamped_h))
            screen_manager.resize((clamped_w, clamped_h))
            
        manager.process_events(event)
        screen_manager.process_event(event)

    ## update
    manager.update(time_delta)
    screen_manager.update(time_delta)

    ## draw
    screen.fill((255, 255, 255))
    screen_manager.draw(screen) # Draw current screen
    manager.draw_ui(screen)     # UI Manager handles overlay UI if any are global, but screens might handle their own too
    pygame.display.update()

screen_manager.cleanup()
pygame.quit()