import pygame
import pygame_gui

pygame.init()

pygame.display.set_caption('bIrD')
screen = pygame.display.set_mode((390, 844))
manager = pygame_gui.UIManager((390, 844))
clock = pygame.time.Clock()


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

    ## draw
    screen.fill((255, 255, 255))
    manager.draw_ui(screen)
    pygame.display.update()

pygame.quit()