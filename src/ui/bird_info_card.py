import pygame
import pygame_gui
from pygame_gui.elements import UIWindow, UIButton, UILabel, UIImage
from src.data.storage import update_bird_status

class BirdInfoCard(UIWindow):
    def __init__(self, rect, manager, bird_data, on_close_callback=None, on_tweeter_callback=None):
        super().__init__(rect, manager, "Bird Check")
        self.bird_data = bird_data
        self.on_close_callback = on_close_callback
        self.on_tweeter_callback = on_tweeter_callback

        # Layout
        # Image
        img_rect = pygame.Rect((10, 10), (200, 200))
        # Try load image
        image_path = bird_data.get('cropped_path') or bird_data.get('image_path')
        self.bird_image_view = None # Renamed to avoid overwriting UIWindow.image
        
        if image_path:
             try:
                loaded_image = pygame.image.load(image_path)
                self.bird_image_view = UIImage(relative_rect=img_rect, image_surface=loaded_image, manager=manager, container=self)
             except:
                UILabel(relative_rect=img_rect, text="No Image", manager=manager, container=self)
        
        # Info
        species = bird_data.get('species', 'Unknown')
        UILabel(relative_rect=pygame.Rect((220, 10), (100, 30)), text=species, manager=manager, container=self)
        
        # Archive Button
        self.archive_btn = UIButton(
            relative_rect=pygame.Rect((220, 150), (100, 30)),
            text='Archive',
            manager=manager,
            container=self
        )

        # Tweeter Button
        self.tweeter_btn = UIButton(
            relative_rect=pygame.Rect((220, 190), (100, 30)),
            text='Tweeter',
            manager=manager,
            container=self
        )

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.archive_btn:
                # Move to archive
                update_bird_status(self.bird_data['id'], 'archived')
                print(f"Archived bird {self.bird_data['id']}")
                self.kill()
                if self.on_close_callback:
                    self.on_close_callback()
            elif event.ui_element == self.tweeter_btn:
                if self.on_tweeter_callback:
                    self.on_tweeter_callback()
                    
    def on_close_window_button_pressed(self):
        # Just close
        super().on_close_window_button_pressed()
        if self.on_close_callback:
            self.on_close_callback()
