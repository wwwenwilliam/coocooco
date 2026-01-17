
from src.scenes.camera_screen import CameraScreen
from src.scenes.birdchive_screen import BirdchiveScreen
from src.scenes.tweeter_screen import TweeterScreen
from src.scenes.field_screen import FieldScreen
from src.scenes.randomevent_screen import RandomEventScreen

class ScreenManager:
    def __init__(self, manager, window_size):
        self.manager = manager
        self.window_size = window_size
        self.current_screen = None
        self.screens = {}
        
        # Initialize all screens
        self.screens['camera'] = CameraScreen(self, manager, window_size)
        self.screens['birdchive'] = BirdchiveScreen(self, manager, window_size)
        self.screens['tweeter'] = TweeterScreen(self, manager, window_size)
        self.screens['field'] = FieldScreen(self, manager, window_size)
        self.screens['random_event'] = RandomEventScreen(self, manager, window_size)

    def switch_to(self, screen_name, **kwargs):
        """Switches to the screen with the given name."""
        if screen_name in self.screens:
            self.set_screen(self.screens[screen_name], **kwargs)
        else:
            print(f"Screen '{screen_name}' not found.")

    def set_screen(self, new_screen, **kwargs):
        """Switches to the new screen."""
        if self.current_screen:
            self.current_screen.cleanup()
        
        self.current_screen = new_screen
        if self.current_screen:
            # Sync window size before setup in case it changed while on another screen
            self.current_screen.window_size = self.window_size
            self.current_screen.setup(**kwargs)

    def setup(self):
        """Setup the manager itself."""
        # Default to field screen
        self.switch_to('field')

    def process_event(self, event):
        """Delegate event processing to current screen."""
        if self.current_screen:
            self.current_screen.process_event(event)

    def update(self, time_delta):
        """Delegate update to current screen."""
        if self.current_screen:
            self.current_screen.update(time_delta)


    def draw(self, surface):
        """Delegate draw to current screen."""
        if self.current_screen:
            self.current_screen.draw(surface)

    def cleanup(self):
        """Cleanup current screen."""
        if self.current_screen:
            self.current_screen.cleanup()
            self.current_screen = None
            
    def resize(self, new_size):
        """Handle window resize."""
        self.window_size = new_size
        # Notify all screens or just current? Best to update all if they store size.
        # But simpler to just update current for now, or ensure set_screen updates it.
        # Actually better to update current.
        if self.current_screen and hasattr(self.current_screen, 'resize'):
            self.current_screen.resize(new_size)
