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

    def setup(self):
        # Header
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (100, 40)),
            text='Back',
            manager=self.manager
        )
        
        # Title
        
        # List
        self.refresh_list()

    def refresh_list(self):
        # Clear existing list if any
        if self.bird_list:
            self.bird_list.kill()
            
        birds = get_birds_by_status('archived')
        self.cached_birds = birds
        
        item_list = []
        for bird in birds:
            # Format: "Species - Date"
            # Date is in timestamp string usually, might want to prettify later
            date_str = bird.get('timestamp', 'Unknown Date').split('T')[0]
            species = bird.get('species', 'Unknown')
            item_list.append(f"{species} ({date_str})")
            
        self.bird_list = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect((20, 60), (self.window_size[0] - 40, self.window_size[1] - 80)),
            item_list=item_list,
            manager=self.manager
        )

    def process_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.back_button:
                self.screen_manager.switch_to('field')
                
        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            if event.ui_element == self.bird_list:
                selection = event.text
                # Find bird data matching index logic or search
                # pygame_gui UISelectionList doesn't give index easily in event, just text.
                # Assuming unique text for now, or just mapping by index if possible?
                # Actually, duplicate strings behave weirdly in UISelectionList.
                # Let's assume order is preserved?
                # Warning: Duplicate species+date strings will be ambiguous.
                # Ideally, UISelectionList supports object mapping, but standard one is string based.
                # For this prototype, I'll search list for FIRST match.
                # Better: Use loop index. But event doesn't give index.
                # Hack: Store 'id' in the string? (ugly)
                # Or just assume list index corresponds to selection index?
                # UISelectionList has .get_single_selection() which might help?
                # Let's iterate `item_list` and match text. 
                # If multiple same entries, this might pick first one always.
                # Good enough for prototype.
                
                # Find index of selection in items
                # The event.text is the string.
                # We can iterate our cached_birds and reconstruct string to find match.
                selected_bird = None
                for bird in self.cached_birds:
                    date_str = bird.get('timestamp', 'Unknown Date').split('T')[0]
                    species = bird.get('species', 'Unknown')
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
