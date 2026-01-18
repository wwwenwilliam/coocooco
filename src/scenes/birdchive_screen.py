from src.scenes.screen import Screen
import pygame
import pygame_gui
from pygame_gui.elements import UIScrollingContainer, UIPanel, UIImage, UILabel, UIButton
from src.data.storage import get_birds_by_status
from src.ui.bird_info_card import BirdInfoCard

class BirdchiveScreen(Screen):
    def __init__(self, screen_manager, manager, window_size):
        super().__init__(screen_manager, manager, window_size)
        self.back_button = None
        self.scroll_container = None
        self.bird_buttons = {} # Map button -> bird_data
        self.grid_items = []
        self.active_card = None

    def setup(self, **kwargs):
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 20), (120, 80)),
            text='',
            manager=self.manager,
            object_id='#back_button'
        )
        
        # Container for the grid
        container_rect = pygame.Rect((20, 120), (self.window_size[0] - 40, self.window_size[1] - 140))
        self.scroll_container = UIScrollingContainer(
            relative_rect=container_rect,
            manager=self.manager
        )
        
        self.refresh_list()

    def refresh_list(self):
        # Clear existing
        for item in self.grid_items:
            item.kill()
        self.grid_items = []
            
        self.bird_buttons = {}
            
        birds = get_birds_by_status('archived')
        
        # Grid Configuration
        tile_size = (200, 240)
        gap = 20
        start_x, start_y = 10, 10
        
        container_width = self.scroll_container.get_relative_rect().width
        # Calculate columns based on width
        cols = max(1, (container_width - start_x) // (tile_size[0] + gap))
        
        current_row = 0
        current_col = 0
        
        for bird in birds:
            x = start_x + (current_col * (tile_size[0] + gap))
            y = start_y + (current_row * (tile_size[1] + gap))
            
            # 1. Tile Panel (Background)
            tile_rect = pygame.Rect((x, y), tile_size)
            panel = UIPanel(
                relative_rect=tile_rect,
                manager=self.manager,
                container=self.scroll_container,
                object_id='#bird_tile'
            )
            self.grid_items.append(panel)
            
            # 2. Image
            img_h = 160
            # Center horizontally with anchors
            # rect.x=0 acts as offset from center when anchored
            img_rect = pygame.Rect((0, 10), (tile_size[0]-30, img_h))
            image_path = bird.get('cropped_path') or bird.get('image_path')
            
            # Check if image exists/loadable
            try:
                loaded_image = pygame.image.load(image_path)
                loaded_image = pygame.transform.scale(loaded_image, (img_rect.width, img_rect.height))
                UIImage(relative_rect=img_rect, image_surface=loaded_image, manager=self.manager, container=panel,
                        anchors={'centerx': 'centerx', 'top': 'top'})
            except:
                UILabel(relative_rect=img_rect, text="No Image", manager=self.manager, container=panel,
                        anchors={'centerx': 'centerx', 'top': 'top'})

            # 3. Label (Name/Species)
            name = bird.get('name')
            species = bird.get('species', 'Unknown')
            date_str = bird.get('timestamp', 'Unknown').split('T')[0]
            
            label_text = name if name else species
            
            UILabel(relative_rect=pygame.Rect((0, img_h + 15), (tile_size[0]-20, 25)), 
                    text=label_text, 
                    manager=self.manager, 
                    container=panel,
                    object_id='#tile_label_main',
                    anchors={'centerx': 'centerx', 'top': 'top'})
            
            UILabel(relative_rect=pygame.Rect((0, img_h + 40), (tile_size[0]-20, 20)), 
                    text=date_str, 
                    manager=self.manager, 
                    container=panel,
                    object_id='#tile_label_sub',
                    anchors={'centerx': 'centerx', 'top': 'top'})

            # 4. Invisible Button for Click
            btn = UIButton(
                relative_rect=pygame.Rect((0,0), tile_size),
                text='',
                manager=self.manager,
                container=panel,
                parent_element=panel,
                object_id='#tile_button' # Make this transparent in theme
            )
            self.bird_buttons[btn] = bird
            
            # Increment Grid
            current_col += 1
            if current_col >= cols:
                current_col = 0
                current_row += 1
                
        # Update scrolling area
        total_rows = current_row + (1 if current_col > 0 else 0)
        total_height = start_y + (total_rows * (tile_size[1] + gap))
        self.scroll_container.set_scrollable_area_dimensions((container_width - 20, total_height))


    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.active_card:
                    card_rect = self.active_card.get_abs_rect()
                    if not card_rect.collidepoint(event.pos):
                        self.active_card.kill()
                        self.active_card = None
                        self.refresh_list()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.back_button:
                self.screen_manager.switch_to('field')
            elif event.ui_element in self.bird_buttons:
                # Open Card
                if self.active_card:
                    self.active_card.kill()
                    
                bird_data = self.bird_buttons[event.ui_element]
                card_rect = pygame.Rect((0, 0), (390, 315))
                card_rect.center = (self.window_size[0]//2, self.window_size[1]//2)
                self.active_card = BirdInfoCard(card_rect, self.manager, bird_data, on_close_callback=self.refresh_list)

    def update(self, time_delta):
        pass

    def draw(self, surface):
        surface.fill((240, 240, 255))
        font = pygame.font.Font(None, 48)
        text = font.render("Bird Archive", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.window_size[0]//2, 60))
        surface.blit(text, text_rect)

    def cleanup(self):
        if self.back_button:
            self.back_button.kill()
            self.back_button = None
        if self.scroll_container:
            self.scroll_container.kill()
            self.scroll_container = None
        self.bird_buttons = {}

    def resize(self, new_size):
        self.window_size = new_size
        
        if self.back_button:
            self.back_button.set_relative_position((20, 20))
            
        if self.scroll_container:
            self.scroll_container.set_relative_position((20, 120))
            self.scroll_container.set_dimensions((self.window_size[0] - 40, self.window_size[1] - 140))
            self.refresh_list() # Re-calc columns
