import pygame
import pygame_gui
from pygame_gui.elements import UIWindow, UIButton, UILabel, UIImage, UITextEntryLine
from src.data.storage import update_bird_status, save_all_birds, load_birds, delete_bird

class BirdInfoCard(UIWindow):
    def __init__(self, rect, manager, bird_data, on_close_callback=None, on_tweeter_callback=None):
        super().__init__(rect, manager, "Bird Info", object_id='#bird_info_card')
        self.bird_data = bird_data
        self.on_close_callback = on_close_callback
        self.on_tweeter_callback = on_tweeter_callback

        self.on_tweeter_callback = on_tweeter_callback

        # Layout
        
        # 0. BACKGROUND IMAGE
        bg_path = "assets/images/infocard2.png"
        try:
            bg_surf = pygame.image.load(bg_path).convert_alpha()
            bg_surf = pygame.transform.scale(bg_surf, self.rect.size)
            UIImage(relative_rect=pygame.Rect((0, 0), self.rect.size), 
                    image_surface=bg_surf, 
                    manager=manager, 
                    container=self, 
                    object_id='#custom_background')
        except Exception as e:
            print(f"Failed to load background {bg_path}: {e}")
        
        # Dimensions for Centering (Card W=390, H=315)
        card_w, card_h = 390, 315
        
        # 1. NAME HEADER (Centered)
        # Width 290. Margin = (390 - 290) / 2 = 50.
        self.name_entry = UITextEntryLine(
            relative_rect=pygame.Rect((50, 40), (290, 35)),
            manager=manager,
            container=self,
            object_id='#name_header_entry'
        )
        self.name_entry.set_text(self.bird_data.get('name', ''))
        
        # 2. MIDDLE SECTION (Image + Info)
        start_x_middle = 50
        img_size = 140
        y_middle = 85
        
        # IMAGE (Left Part of Middle)
        img_rect = pygame.Rect((start_x_middle, y_middle), (img_size, img_size))
        image_path = bird_data.get('cropped_path') or bird_data.get('image_path')
        self.bird_image_view = None 
        
        if image_path:
             try:
                loaded_image = pygame.image.load(image_path).convert_alpha()
                loaded_image = pygame.transform.scale(loaded_image, (img_size, img_size))
                
                # Round the image (Rounded Rectangle)
                mask = pygame.Surface((img_size, img_size), pygame.SRCALPHA)
                pygame.draw.rect(mask, (255, 255, 255), (0, 0, img_size, img_size), border_radius=8)
                
                # Apply mask using RGBA_MULT
                final_image = loaded_image.copy()
                final_image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                
                self.bird_image_view = UIImage(relative_rect=img_rect, image_surface=final_image, manager=manager, container=self)
             except Exception as e:
                print(f"Image load error: {e}")
                UILabel(relative_rect=img_rect, text="No Image", manager=manager, container=self)
        
        # INFO COLUMN (Right Part of Middle)
        col_x = start_x_middle + img_size + 10 
        width = 140
        
        # Species
        species = bird_data.get('species', 'Unknown')
        UILabel(relative_rect=pygame.Rect((col_x, y_middle), (width, 20)), text="Species:", manager=manager, container=self, object_id='#info_header')
        UILabel(relative_rect=pygame.Rect((col_x, y_middle + 20), (width, 25)), text=species, manager=manager, container=self)
        
        # Personality / Trait Label
        personality = self.bird_data.get('personality', 'Unknown')
        UILabel(relative_rect=pygame.Rect((col_x, y_middle + 55), (width, 20)), text="Personality:", manager=manager, container=self, object_id='#info_header')
        self.personality_label = UILabel(relative_rect=pygame.Rect((col_x, y_middle + 75), (width, 25)), text=f"{personality}", manager=manager, container=self)

        # Archive Status (Checked early for Layout)
        is_archived = self.bird_data.get('status') == 'archived'

        # Squawk Meter (Hidden if archived)
        self.rage_bar = None
        if not is_archived:
            from pygame_gui.elements import UIProgressBar
            from src.data.game_state import GlobalState
            
            UILabel(relative_rect=pygame.Rect((col_x, y_middle + 105), (width, 20)), text="Squawk Meter:", manager=manager, container=self, object_id='#info_header')
            
            self.rage_bar = UIProgressBar(
                relative_rect=pygame.Rect((col_x, y_middle + 125), (width, 20)),
                manager=manager,
                container=self,
                object_id='#rage_bar' 
            )
            self.rage_bar.set_current_progress(GlobalState.get_instance().rage_level)
 
        # 3. BUTTONS (Bottom Centered)
        # Btn(135) + Gap(20) + Btn(135) = 290
        # Margin = (390 - 290) / 2 = 50
        btn_y = 240
        btn_w = 135
        btn_gap = 20
        start_x_btn = 50

        # Archive/Release Button
        btn_text = 'Release' if is_archived else 'Archive'

        self.archive_btn = UIButton(
            relative_rect=pygame.Rect((start_x_btn, btn_y), (btn_w, 35)),
            text=btn_text,
            manager=manager,
            container=self,
            object_id='#archive_button'
        )

        # Tweeter / Delete
        self.tweeter_btn = None
        self.delete_btn = None
        
        btn2_x = start_x_btn + btn_w + btn_gap

        if is_archived:
             self.delete_btn = UIButton(
                relative_rect=pygame.Rect((btn2_x, btn_y), (btn_w, 35)),

                text='Delete',
                manager=manager,
                container=self,
                object_id='#delete_button'
            )
        else:
            self.tweeter_btn = UIButton(
                relative_rect=pygame.Rect((btn2_x, btn_y), (btn_w, 35)),
                text='Tweeter',
                manager=manager,
                container=self,
                object_id='#tweeter_button'
            )


    def update(self, time_delta):
        super().update(time_delta)
        from src.data.game_state import GlobalState
        current_rage = GlobalState.get_instance().rage_level
        if self.rage_bar:
            self.rage_bar.set_current_progress(current_rage)

    def save_name(self):
        if self.name_entry:
            new_name = self.name_entry.get_text()
            if new_name: # Only save if not empty
                 if new_name != self.bird_data.get('name'):
                    # Save name locally
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
            
            # No mode switch needed

    def process_event(self, event):
        super().process_event(event)

        # Save name on enter
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == self.name_entry:
                self.save_name()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.archive_btn:
                self.save_name() # Save name before action
                
                if self.bird_data.get('status') == 'archived':
                     # Release
                     update_bird_status(self.bird_data['id'], 'field')
                     print(f"Released bird {self.bird_data['id']}")
                else:
                     # Archive
                     update_bird_status(self.bird_data['id'], 'archived')
                     print(f"Archived bird {self.bird_data['id']}")
                     
                self.kill()
                if self.on_close_callback:
                    self.on_close_callback()
            elif event.ui_element == self.tweeter_btn:
                self.save_name() # Save name before switching logic
                if self.on_tweeter_callback:
                    self.on_tweeter_callback()
            elif event.ui_element == self.delete_btn:
                 delete_bird(self.bird_data['id'])
                 print(f"Deleted bird {self.bird_data['id']}")
                 self.kill()
                 if self.on_close_callback:
                     self.on_close_callback()
                    
    def on_close_window_button_pressed(self):
        self.save_name() # Save name on close
        super().on_close_window_button_pressed()
        if self.on_close_callback:
            self.on_close_callback()
