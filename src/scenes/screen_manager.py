from src.scenes.screen import Screen
from src.scenes.camera_screen import CameraScreen
from src.scenes.birdchive_screen import BirdchiveScreen
from src.scenes.tweeter_screen import TweeterScreen
from src.scenes.field_screen import FieldScreen
from src.scenes.randomevent_screen import RandomEventScreen

class ScreenManager(Screen):
    def __init__(self, manager, window_size):
        super().__init__(manager, window_size)
        self.current_screen = None
        self.screens = {}
        
        # Initialize all screens
        self.screens['camera'] = CameraScreen(manager, window_size)
        self.screens['birdchive'] = BirdchiveScreen(manager, window_size)
        self.screens['tweeter'] = TweeterScreen(manager, window_size)
        self.screens['field'] = FieldScreen(manager, window_size)
        self.screens['random_event'] = RandomEventScreen(manager, window_size)

    def switch_to(self, screen_name):
        """Switches to the screen with the given name."""
        if screen_name in self.screens:
            self.set_screen(self.screens[screen_name])
        else:
            print(f"Screen '{screen_name}' not found.")

    def set_screen(self, new_screen):
        """Switches to the new screen."""
        if self.current_screen:
            self.current_screen.cleanup()
        
        self.current_screen = new_screen
        if self.current_screen:
            self.current_screen.setup()

    def setup(self):
        """Setup the manager itself."""
        # Default to camera screen for now, or field
        self.switch_to('camera')

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
