import pygame
import pygame_gui

# 1. Initialize Pygame immediately
pygame.init()
import pygame.camera
pygame.camera.init()

pygame.display.set_caption('bIrD')
screen = pygame.display.set_mode((390, 844))

# 2. Show Splash Screen
screen.fill((255, 255, 255))
font = pygame.font.Font(None, 48)
text = font.render("Loading...", True, (0, 0, 0))
text_rect = text.get_rect(center=(390//2, 844//2))
screen.blit(text, text_rect)
pygame.display.update()

# 3. Heavy Imports (Now that window is visible)
# This import chain triggers torch/transformers loading
from src.scenes.screen_manager import ScreenManager

manager = pygame_gui.UIManager((390, 844))
clock = pygame.time.Clock()

# Create Screen Manager
screen_manager = ScreenManager(manager, (390, 844))
screen_manager.setup()

running = True
while running:
    ## clock
    time_delta = clock.tick(60)/1000.0

    ## event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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