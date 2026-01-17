from src.scenes.screen import Screen
import pygame
import pygame_gui

class TweeterScreen(Screen):
    def __init__(self, screen_manager, manager, window_size):
        super().__init__(screen_manager, manager, window_size)

    def setup(self, **kwargs):
        pass

    def process_event(self, event):
        pass

    def update(self, time_delta):
        pass

    def draw(self, surface):
        surface.fill((255, 200, 200)) # Light red placeholder
        font = pygame.font.Font(None, 36)
        text = font.render("Tweeter Screen", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.window_size[0]//2, self.window_size[1]//2))
        surface.blit(text, text_rect)

    def cleanup(self):
        pass

    def resize(self, new_size):
        self.window_size = new_size
