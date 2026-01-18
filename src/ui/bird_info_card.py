import pygame
import pygame_gui
from pygame_gui.elements import UIWindow, UIButton, UILabel, UIImage, UITextEntryLine
from src.data.storage import update_bird_status, save_all_birds, load_birds

class BirdInfoCard(UIWindow):
    def __init__(self, rect, manager, bird_data, on_close_callback=None, on_tweeter_callback=None):
        super().__init__(rect, manager, "Bird Info", object_id='#bird_info_card')
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
        UILabel(relative_rect=pygame.Rect((220, 10), (100, 30)), text="Species:", manager=manager, container=self)
        UILabel(relative_rect=pygame.Rect((220, 35), (100, 30)), text=species, manager=manager, container=self)
        
        # Name Section
        UILabel(relative_rect=pygame.Rect((220, 70), (100, 30)), text="Name:", manager=manager, container=self)
        
        self.name_label = None
        self.edit_btn = None
        self.name_entry = None
        
        # Initial State
        if 'name' in self.bird_data and self.bird_data['name']:
            self.switch_to_view_mode()
        else:
            self.switch_to_edit_mode()

        # Personality Label
        personality = self.bird_data.get('personality', 'Unknown')
        self.personality_label = UILabel(
            relative_rect=pygame.Rect((220, 60), (150, 30)), # Wider for text
            text=f"Trait: {personality}",
            manager=manager,
            container=self
        )

        # Archive Button
        self.archive_btn = UIButton(
            relative_rect=pygame.Rect((220, 170), (100, 30)),
            text='Archive',
            manager=manager,
            container=self,
            object_id='#archive_button'
        )

        # Tweeter Button
        self.tweeter_btn = UIButton(
            relative_rect=pygame.Rect((220, 210), (100, 30)),
            text='Tweeter',
            manager=manager,
            container=self,
            object_id='#tweeter_button'
        )

    def switch_to_view_mode(self):
        self.clear_name_ui()
        name = self.bird_data.get('name', 'Unnamed')
        self.name_label = UILabel(relative_rect=pygame.Rect((220, 95), (100, 30)), text=name, manager=self.ui_manager, container=self, object_id='#name_label')
        self.edit_btn = UIButton(relative_rect=pygame.Rect((220, 130), (100, 30)), text='Edit', manager=self.ui_manager, container=self, object_id='#edit_button')

    def switch_to_edit_mode(self):
        self.clear_name_ui()
        self.name_entry = UITextEntryLine(
            relative_rect=pygame.Rect((220, 95), (100, 30)),
            manager=self.ui_manager,
            container=self,
            object_id='#name_entry'
        )
        if 'name' in self.bird_data:
            self.name_entry.set_text(self.bird_data['name'])
        self.name_entry.focus()

    def clear_name_ui(self):
        if self.name_label:
            self.name_label.kill()
            self.name_label = None
        if self.edit_btn:
            self.edit_btn.kill()
            self.edit_btn = None
        if self.name_entry:
            self.name_entry.kill()
            self.name_entry = None

    def save_name(self):
        if self.name_entry:
            new_name = self.name_entry.get_text()
            if new_name: # Only save if not empty? Or allow clearing? Let's assume non-empty for now or keep old
                 if new_name != self.bird_data.get('name'):
                    # Save name
                    self.bird_data['name'] = new_name
                    
                    # Update storage
                    birds = load_birds()
                    found = False
                    for b in birds:
                        if b['id'] == self.bird_data['id']:
                            b['name'] = new_name
                            found = True
                            break
                    
                    if found:
                        save_all_birds(birds)
                        print(f"Saved name '{new_name}' for bird {self.bird_data['id']}")
            
            # Switch back to view mode
            self.switch_to_view_mode()

    def process_event(self, event):
        super().process_event(event)

        # Save name on enter or lose focus? 
        # UITextEntryLine triggers UI_TEXT_ENTRY_FINISHED on Enter
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == self.name_entry:
                self.save_name()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.edit_btn:
                self.switch_to_edit_mode()
            elif event.ui_element == self.archive_btn:
                self.save_name() # Save name before archiving too
                # Move to archive
                update_bird_status(self.bird_data['id'], 'archived')
                print(f"Archived bird {self.bird_data['id']}")
                self.kill()
                if self.on_close_callback:
                    self.on_close_callback()
            elif event.ui_element == self.tweeter_btn:
                self.save_name() # Save name before switching logic
                if self.on_tweeter_callback:
                    self.on_tweeter_callback()
                    
    def on_close_window_button_pressed(self):
        self.save_name() # Save name on close
        super().on_close_window_button_pressed()
        if self.on_close_callback:
            self.on_close_callback()
