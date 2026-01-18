from src.scenes.screen import Screen
import pygame
import pygame_gui
from src.data.storage import get_birds_by_status
from src.ui.birdchive_card import BirdchiveCard

class BirdchiveScreen(Screen):
    def __init__(self, screen_manager, manager, window_size):
        super().__init__(screen_manager, manager, window_size)
        self.back_button = None
        self.bird_list = None
        self.cached_birds = [] # To map list items back to data

    def setup(self, **kwargs):
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (100, 40)),
            text='Back',
            manager=self.manager,
            object_id='#back_button'
        )
        
        self.refresh_list()

    def refresh_list(self):
        if self.bird_list:
            self.bird_list.kill()
            
        birds = get_birds_by_status('archived')
        self.cached_birds = birds
        
        item_list = []
        for bird in birds:
            date_str = bird.get('timestamp', 'Unknown Date').split('T')[0]
            species = bird.get('species', 'Unknown')
            name = bird.get('name')
            
            if name:
                label = f"{name} ({species}) - {date_str}"
            else:
                label = f"{species} ({date_str})"
                
            item_list.append(label)
            
        self.bird_list = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect((20, 60), (self.window_size[0] - 40, self.window_size[1] - 80)),
            item_list=item_list,
            manager=self.manager,
            object_id='#birdchive_list'
        )

    def process_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.back_button:
                self.screen_manager.switch_to('field')
                
        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            if event.ui_element == self.bird_list:
                selection = event.text
                
                # Find bird by matching reconstructed label (first match wins for duplicates)
                selected_bird = None
                for bird in self.cached_birds:
                    date_str = bird.get('timestamp', 'Unknown Date').split('T')[0]
                    species = bird.get('species', 'Unknown')
                    name = bird.get('name')
                    
                    if name:
                        label = f"{name} ({species}) - {date_str}"
                    else:
                         label = f"{species} ({date_str})"
                         
                    if label == selection:
                        selected_bird = bird
                        break
                
                if selected_bird:
                    # Open Card
                    # Center rect
                    card_rect = pygame.Rect((0, 0), (300, 400))
                    card_rect.center = (self.window_size[0]//2, self.window_size[1]//2)
                    BirdchiveCard(card_rect, self.manager, selected_bird, on_close_callback=self.refresh_list)

    def update(self, time_delta):
        pass

    def draw(self, surface):
        surface.fill((240, 240, 255))
        font = pygame.font.Font(None, 48)
        text = font.render("Bird Archive", True, (0, 0, 0))
        text_rect = text.get_rect(midtop=(self.window_size[0]//2, 15))
        surface.blit(text, text_rect)

    def cleanup(self):
        if self.back_button:
            self.back_button.kill()
            self.back_button = None
        if self.bird_list:
            self.bird_list.kill()
            self.bird_list = None

    def resize(self, new_size):
        self.window_size = new_size
        
        if self.back_button:
            self.back_button.set_relative_position((10, 10))
            
        if self.bird_list:
            # Resize the list
            self.bird_list.set_relative_position((20, 60))
            self.bird_list.set_dimensions((self.window_size[0] - 40, self.window_size[1] - 80))
