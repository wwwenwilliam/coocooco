from src.scenes.screen import Screen
import pygame
import pygame_gui
import random
from src.entities.bird import Bird

class FieldScreen(Screen):
    def __init__(self, screen_manager, manager, window_size):
        super().__init__(screen_manager, manager, window_size)
        self.background = None
        self.scroll_x = 0
        self.max_scroll = 0
        self.birds = pygame.sprite.Group()
        self.camera_button = None

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
            world_width = new_width
            self.max_scroll = max(0, new_width - self.window_size[0])
            
            # Spawn Birds
            self.birds.empty()
            for _ in range(5):
                x = random.randint(0, world_width - 100)
                y = random.randint(50, new_height - 200) # Keep them somewhat in the middle/ground
                bird = Bird((x, y), (0, 0, world_width, new_height))
                self.birds.add(bird)
                
            # UI
            btn_size = (100, 50)
            self.camera_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((self.window_size[0] - btn_size[0] - 20, self.window_size[1] - btn_size[1] - 20), btn_size),
                text='Camera',
                manager=self.manager
            )
                
        except pygame.error as e:
            print(f"Could not load background image: {e}")

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            scroll_speed = 10
            if event.key == pygame.K_LEFT:
                self.scroll_x = max(0, self.scroll_x - scroll_speed)
            elif event.key == pygame.K_RIGHT:
                self.scroll_x = min(self.max_scroll, self.scroll_x + scroll_speed)
                
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.camera_button:
                self.screen_manager.switch_to('camera')
        
        # Pass events to birds
        for bird in self.birds:
            bird.handle_event(event, self.scroll_x)

    def update(self, time_delta):
        self.birds.update(time_delta)

    def draw(self, surface):
        if self.background:
            surface.blit(self.background, (-self.scroll_x, 0))
        else:
            surface.fill((200, 255, 200)) # Light green placeholder
            
        # Draw birds with scroll offset
        for bird in self.birds:
            bird.draw(surface, self.scroll_x)
            
        font = pygame.font.Font(None, 36)
        text = font.render("Field Screen", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.window_size[0]//2, self.window_size[1]//2))
        surface.blit(text, text_rect)

    def cleanup(self):
        if self.camera_button:
            self.camera_button.kill()
            self.camera_button = None
