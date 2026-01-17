import pygame
import pygame_gui

pygame.init()
import pygame.camera
pygame.camera.init()

pygame.display.set_caption('bIrD')
screen = pygame.display.set_mode((390, 844))
manager = pygame_gui.UIManager((390, 844))
clock = pygame.time.Clock()

## import scenes
from src.scenes.screen_manager import ScreenManager

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