from src.scenes.screen import Screen
import pygame
import pygame_gui
import random
from src.entities.bird import Bird
from src.data.storage import load_birds

class FieldScreen(Screen):
    def __init__(self, screen_manager, manager, window_size):
        super().__init__(screen_manager, manager, window_size)
        self.background = None
        self.scroll_x = 0
        self.max_scroll = 0
        self.birds = pygame.sprite.Group()
        self.camera_button = None
        self.is_dragging = False
        self.last_mouse_x = 0
        self.scroll_velocity = 0
        self.friction = 0.92

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
            saved_birds = load_birds()
            
            if not saved_birds:
                # Fallback if no birds saved? Or just empty?
                # Let's spawn a couple of random placeholders just so it's not empty for testing if they have no data
                # But user wanted "a bird for every picture". If 0 pictures, 0 birds.
                # However, for testing let's keep one debug bird if empty? No, respect user request.
                pass
            
            for bird_data in saved_birds:
                 # Random position for now
                x = random.randint(0, world_width - 100)
                y = random.randint(50, new_height - 200) 
                
                # Pass data to bird
                bird = Bird((x, y), (0, 0, world_width, new_height), bird_data)
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
        # Keyboard Scrolling
        if event.type == pygame.KEYDOWN:
            scroll_speed = 10
            if event.key == pygame.K_LEFT:
                self.scroll_x = max(0, self.scroll_x - scroll_speed)
            elif event.key == pygame.K_RIGHT:
                self.scroll_x = min(self.max_scroll, self.scroll_x + scroll_speed)
        
        # Drag Scrolling
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                # Check if we clicked the button first (hacky, ideally UI manager handles this and consumes event)
                # But UI manager processes events in main loop too. 
                # To avoid dragging when clicking button, we could check button rect, 
                # but pygame_gui usually consumes events if we let it.
                # Here we are processing *after* manager in main.py, so we should be fine?
                # Actually main.py calls manager.process_events first.
                # Simple check: collidepoint with birds (handled later) or ignore if clicking button area?
                # For now, just enable drag.
                self.is_dragging = True
                self.last_mouse_x = event.pos[0]
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False
                
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                mouse_x = event.pos[0]
                dx = mouse_x - self.last_mouse_x
                # Dragging left (x decreases) means moving view right (scroll increases)
                # Dragging right (x increases) means moving view left (scroll decreases)
                # So we SUBTRACT dx from scroll_x
                self.scroll_x -= dx
                self.scroll_x = max(0, min(self.scroll_x, self.max_scroll))
                self.last_mouse_x = mouse_x
                self.scroll_velocity = dx # Track velocity for momentum

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.camera_button:
                self.screen_manager.switch_to('camera')
        
        # Pass events to birds
        for bird in self.birds:
            bird.handle_event(event, self.scroll_x)

    def update(self, time_delta):
        self.birds.update(time_delta)
        
        # Apply Momentum
        if not self.is_dragging and abs(self.scroll_velocity) > 0.1:
            self.scroll_x -= self.scroll_velocity
            self.scroll_velocity *= self.friction
            
            # Clamp and stop if hitting bounds
            if self.scroll_x < 0:
                self.scroll_x = 0
                self.scroll_velocity = 0
            elif self.scroll_x > self.max_scroll:
                self.scroll_x = self.max_scroll
                self.scroll_velocity = 0
        elif not self.is_dragging:
             self.scroll_velocity = 0

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
