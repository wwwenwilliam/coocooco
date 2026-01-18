import pygame
import pygame_gui
from pygame_gui.elements import UIPanel, UIImage

class CreditsPopup(UIPanel):
    def __init__(self, manager, window_size, on_close_callback=None):
        # Load Background Image
        try:
            image_path = "assets/images/caption_card.png" 
            self.bg_image = pygame.image.load(image_path).convert_alpha()
            width, height = self.bg_image.get_size()
        except Exception as e:
            print(f"CreditsPopup Load Error: {e}")
            width, height = 390, 315
            self.bg_image = None

        # Center on screen using window_size
        center_x = (window_size[0] - width) // 2
        center_y = (window_size[1] - height) // 2
        rect = pygame.Rect(center_x, center_y, width, height)

        super().__init__(
            relative_rect=rect,
            starting_height=2, # Top layer
            manager=manager,
            object_id='#bird_info_card' # Transparent background
        )
        
        self.on_close_callback = on_close_callback

        # Background Image
        if self.bg_image:
             UIImage(relative_rect=pygame.Rect((0,0), (width, height)),
                     image_surface=self.bg_image,
                     manager=manager,
                     container=self)

    def process_event(self, event):
        super().process_event(event) # Handle basic UI stuff
        
        # Close on click ON the popup (Left Click)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if click is ON the panel's absolute rect
            if self.rect.collidepoint(mouse_pos):
                self.kill()
                if self.on_close_callback:
                    self.on_close_callback()
