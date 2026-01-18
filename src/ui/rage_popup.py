import pygame
import pygame_gui
from pygame_gui.elements import UIPanel, UIImage, UIButton, UILabel

class RagePopup(UIPanel):
    def __init__(self, manager, window_size, on_ack_callback=None):
        # Load Background Image to determine size
        try:
            image_path = "assets/images/rage_popup.png" 
            self.bg_image = pygame.image.load(image_path).convert_alpha()
            width, height = self.bg_image.get_size()
        except Exception as e:
            print(f"RagePopup Load Error: {e}")
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
            object_id='#bird_info_card' # Re-use transparent style
        )
        
        self.on_ack_callback = on_ack_callback

        # Background Image
        if self.bg_image:
             UIImage(relative_rect=pygame.Rect((0,0), (width, height)),
                     image_surface=self.bg_image,
                     manager=manager,
                     container=self)

        # Acknowledge / Exit Button
        self.exit_btn = UIButton(
            relative_rect=pygame.Rect(0, -200, 400, 100), # Centered, near bottom
            text='', # Image based
            manager=manager,
            container=self,
            object_id='#popup_exit_button',
            anchors={'centerx': 'centerx', 'bottom': 'bottom'}
        )
        
    def process_event(self, event):
        super().process_event(event) # Handle basic UI stuff
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.exit_btn:
                if self.on_ack_callback:
                    self.on_ack_callback()
                self.kill()
