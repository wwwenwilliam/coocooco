import pygame
import pygame_gui
from pygame_gui.elements import UIWindow, UIButton, UILabel, UITextBox, UISelectionList

class TweeterCard(UIWindow):
    def __init__(self, rect, manager, bird_data=None, on_close_callback=None):
        super().__init__(rect, manager, "Tweeter", draggable=False)
        self.bird_data = bird_data
        self.on_close_callback = on_close_callback

        # Layout
        # Feed (Placeholder)
        self.feed_list = UISelectionList(
            relative_rect=pygame.Rect((10, 10), (rect.width - 20, rect.height - 100)),
            item_list=[
                "@BirdLover99: Saw a nice pigeon today!",
                "@EagleEye: The migration has started.",
                "@CoocoocoUser: Just archived a Looney Bird.",
                "System: Welcome to Coocooco Tweeter!"
            ],
            manager=manager,
            container=self
        )
        
        # Input Area (Placeholder)
        self.input_box = UITextBox(
            html_text="Write a tweet...",
            relative_rect=pygame.Rect((10, rect.height - 80), (rect.width - 140, 40)),
            manager=manager,
            container=self
        )
        
        # Post Button
        self.post_btn = UIButton(
            relative_rect=pygame.Rect((rect.width - 120, rect.height - 80), (110, 40)),
            text='Post',
            manager=manager,
            container=self
        )

    def process_event(self, event):
        super().process_event(event)
        # Handle Posting (Fake)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.post_btn:
                print("Posted tweet!")
                # Could append to list if we made it dynamic
                
    def on_close_window_button_pressed(self):
        super().on_close_window_button_pressed()
        if self.on_close_callback:
            self.on_close_callback()
