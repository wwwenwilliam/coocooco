from src.scenes.screen import Screen
import pygame
import pygame_gui
import random
from src.entities.bird import Bird
from src.data.storage import load_birds, get_birds_by_status
from src.ui.bird_info_card import BirdInfoCard
from src.ui.tweeter_card import TweeterCard

class FieldScreen(Screen):
    def __init__(self, screen_manager, manager, window_size):
        super().__init__(screen_manager, manager, window_size)
        self.background = None
        self.scroll_x = 0
        self.max_scroll = 0
        self.birds = pygame.sprite.Group()
        self.camera_button = None
        self.birdchive_button = None
        self.is_dragging = False
        self.last_mouse_x = 0
        self.scroll_velocity = 0
        self.friction = 0.92
        self.active_card = None
        self.card_world_pos = None
        self.tweeter_card = None

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
            self.refresh_birds()
                
            # UI
            btn_size = (100, 50)
            self.camera_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((self.window_size[0] - btn_size[0] - 20, self.window_size[1] - btn_size[1] - 20), btn_size),
                text='Camera',
                manager=self.manager
            )

            self.birdchive_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((20, self.window_size[1] - btn_size[1] - 20), btn_size),
                text='Birdchive',
                manager=self.manager
            )
                
        except pygame.error as e:
            print(f"Could not load background image: {e}")

    def process_event(self, event):
        # 1. UI Buttons (Navigation) - Always allow? 
        # Actually user might want to navigate away.
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.camera_button:
                self.screen_manager.switch_to('camera')
            elif event.ui_element == self.birdchive_button:
                self.screen_manager.switch_to('birdchive')
        
        # 2. Block field interactions if a card is active
        # Only block if Tweeter is open (fullscreen overlay)
        # BirdInfoCard (active_card) should allow scrolling so it 'floats'
        if self.tweeter_card:
             return

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
                self.is_dragging = True
                self.last_mouse_x = event.pos[0]
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False
                
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                mouse_x = event.pos[0]
                dx = mouse_x - self.last_mouse_x
                self.scroll_x -= dx
                self.scroll_x = max(0, min(self.scroll_x, self.max_scroll))
                self.last_mouse_x = mouse_x
                self.scroll_velocity = dx 

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.camera_button:
                self.screen_manager.switch_to('camera')
            elif event.ui_element == self.birdchive_button:
                self.screen_manager.switch_to('birdchive')
        

        
        
        # Pass events to birds - Only if no card is active
        if not self.active_card:
            for bird in self.birds:
                if bird.handle_event(event, self.scroll_x):
                    # Pause THIS bird
                    bird.is_paused = True
                    
                    # Calculate World Position for Card
                    # Right of bird, top aligned
                    world_x = bird.rect.right
                    world_y = bird.rect.top - 20
                    
                    # Check absolute bounds? 
                    # Ideally we want it to stay relative to bird. 
                    # We'll just store this World Pos.
                    self.card_world_pos = pygame.Vector2(world_x, world_y)
                    
                    # Calculate initial screen pos
                    screen_x = int(world_x - self.scroll_x)
                    screen_y = int(world_y)
                    
                    # Clamp Y to screen (since Y doesn't scroll)
                    if screen_y < 0: screen_y = 10
                    if screen_y + 250 > self.window_size[1]: screen_y = self.window_size[1] - 260
                    
                    # Update world_pos Y to reflect the clamped Y (so it stays there)
                    self.card_world_pos.y = screen_y 

                    card_rect = pygame.Rect((screen_x, screen_y), (330, 250))
                    
                    def on_close():
                        bird.is_paused = False
                        self.active_card = None
                        self.refresh_birds()
                    
                    def on_open_tweeter():
                        # Create Tweeter Card
                        # Fullscreen overlay with margin
                        margin = 50
                        width = self.window_size[0] - (margin * 2)
                        height = self.window_size[1] - (margin * 2)
                        rect = pygame.Rect(0, 0, width, height)
                        rect.center = (self.window_size[0]//2, self.window_size[1]//2)
                        
                        def on_tweeter_close():
                            self.tweeter_card = None
                            # Re-enable Bird Info Card
                            if self.active_card:
                                 self.active_card.enable()
                            
                        self.tweeter_card = TweeterCard(rect, self.manager, bird.bird_data, on_close_callback=on_tweeter_close)
                        
                        # Disable active card interactions while Tweeter is up
                        if self.active_card:
                            self.active_card.disable()

                    self.active_card = BirdInfoCard(card_rect, self.manager, bird.bird_data, on_close_callback=on_close, on_tweeter_callback=on_open_tweeter)
                    break 

    def update(self, time_delta):
        self.birds.update(time_delta)
        
        # Update Card Position if active
        if self.active_card and self.card_world_pos:
            screen_x = int(self.card_world_pos.x - self.scroll_x)
            screen_y = int(self.card_world_pos.y)
            self.active_card.set_position((screen_x, screen_y))
        
        # Apply Momentum
        if not self.is_dragging and abs(self.scroll_velocity) > 0.1:
            self.scroll_x -= self.scroll_velocity
            self.scroll_velocity *= self.friction
            
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
            surface.fill((200, 255, 200)) 
            
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
            
        if self.birdchive_button:
            self.birdchive_button.kill()
            self.birdchive_button = None

    def refresh_birds(self):
        # Dictionary of current sprites by ID
        current_sprites = {b.bird_data['id']: b for b in self.birds}
        
        # Get target data
        field_birds_data = get_birds_by_status('field')
        field_ids = {b['id'] for b in field_birds_data}
        
        # Bounds logic
        if self.background:
             world_width = self.background.get_width()
             height = self.background.get_height()
        else:
             world_width = self.window_size[0] * 2 
             height = self.window_size[1]

        # 1. Remove sprites not in field list (Archived/Deleted)
        for bird_id, sprite in list(current_sprites.items()):
            if bird_id not in field_ids:
                sprite.kill()
        
        # 2. Add new sprites
        for bird_data in field_birds_data:
            b_id = bird_data['id']
            if b_id not in current_sprites:
                 # Spawn new
                x = random.randint(0, world_width - 100)
                y = random.randint(50, height - 200) 
                bird = Bird((x, y), (0, 0, world_width, height), bird_data)
                self.birds.add(bird)
