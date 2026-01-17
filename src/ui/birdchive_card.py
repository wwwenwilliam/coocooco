import pygame
import pygame_gui
from pygame_gui.elements import UIWindow, UIButton, UILabel, UIImage
from src.data.storage import update_bird_status, delete_bird

class BirdchiveCard(UIWindow):
    def __init__(self, rect, manager, bird_data, on_close_callback=None):
        super().__init__(rect, manager, "Bird Archive Details")
        self.bird_data = bird_data
        self.on_close_callback = on_close_callback 

        # Layout
        # Larger Image
        img_rect = pygame.Rect((10, 10), (280, 280))
        image_path = bird_data.get('cropped_path') or bird_data.get('image_path')
        if image_path:
             try:
                loaded_image = pygame.image.load(image_path)
                self.bird_image_view = UIImage(relative_rect=img_rect, image_surface=loaded_image, manager=manager, container=self)
             except:
                 pass
        
        # Info
        species = bird_data.get('species', 'Unknown')
        UILabel(relative_rect=pygame.Rect((10, 300), (280, 30)), text=species, manager=manager, container=self)
        
        # Buttons
        self.release_btn = UIButton(
            relative_rect=pygame.Rect((10, 340), (130, 40)),
            text='Release',
            manager=manager,
            container=self
        )
        
        self.delete_btn = UIButton(
            relative_rect=pygame.Rect((160, 340), (130, 40)),
            text='Delete',
            manager=manager,
            container=self
        )

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.release_btn:
                update_bird_status(self.bird_data['id'], 'field')
                print(f"Released bird {self.bird_data['id']}")
                self.kill()
                if self.on_close_callback:
                    self.on_close_callback()
            elif event.ui_element == self.delete_btn:
                delete_bird(self.bird_data['id'])
                print(f"Deleted bird {self.bird_data['id']}")
                self.kill()
                if self.on_close_callback:
                    self.on_close_callback()
                    
    def on_close_window_button_pressed(self):
        super().on_close_window_button_pressed()
        if self.on_close_callback:
            self.on_close_callback()
