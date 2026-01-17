from src.scenes.screen import Screen
import pygame
import pygame_gui

class FieldScreen(Screen):
    def __init__(self, screen_manager, manager, window_size):
        super().__init__(screen_manager, manager, window_size)
        self.background = None
        self.scroll_x = 0
        self.max_scroll = 0

    def setup(self):
        try:
            self.background = pygame.image.load("assets/images/botwfield_placeholder.jpg")
            # Scale to match window height while maintaining aspect ratio
            original_width, original_height = self.background.get_size()
            aspect_ratio = original_width / original_height
            new_height = self.window_size[1]
            new_width = int(new_height * aspect_ratio)
            self.background = pygame.transform.scale(self.background, (new_width, new_height))
            # Calculate max scrolling distance
            self.max_scroll = max(0, new_width - self.window_size[0])
        except pygame.error as e:
            print(f"Could not load background image: {e}")

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            scroll_speed = 10
            if event.key == pygame.K_LEFT:
                self.scroll_x = max(0, self.scroll_x - scroll_speed)
            elif event.key == pygame.K_RIGHT:
                self.scroll_x = min(self.max_scroll, self.scroll_x + scroll_speed)

    def update(self, time_delta):
        pass

    def draw(self, surface):
        if self.background:
            surface.blit(self.background, (-self.scroll_x, 0))
        else:
            surface.fill((200, 255, 200)) # Light green placeholder
        font = pygame.font.Font(None, 36)
        text = font.render("Field Screen", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.window_size[0]//2, self.window_size[1]//2))
        surface.blit(text, text_rect)

    def cleanup(self):
        pass
