from src.scenes.screen import Screen
import pygame
import pygame_gui

class FieldScreen(Screen):
    def __init__(self, screen_manager, manager, window_size):
        super().__init__(screen_manager, manager, window_size)

    def setup(self):
        pass

    def process_event(self, event):
        pass

    def update(self, time_delta):
        pass

    def draw(self, surface):
        surface.fill((200, 255, 200)) # Light green placeholder
        font = pygame.font.Font(None, 36)
        text = font.render("Field Screen", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.window_size[0]//2, self.window_size[1]//2))
        surface.blit(text, text_rect)

    def cleanup(self):
        pass
