import pygame
import pygame_gui
import pygame.camera

from src.scenes.screen import Screen
from src.image_tools.processor import process_image

class CameraScreen(Screen):
    def __init__(self, screen_manager, manager, window_size):
        super().__init__(screen_manager, manager, window_size)
        self.ui_elements = []
        self.cam = None
        self.camera_surface = None
        
    def setup(self):
        # Init camera
        if self.camera_surface is None:
             # Try to init camera here if needed or just start it
             pass

        # Init camera logic
        cameras = pygame.camera.list_cameras()
        if cameras:
            # Use the first available camera
            try:
                if self.cam is None:
                     self.cam = pygame.camera.Camera(cameras[0], self.window_size)
                self.cam.start()
            except Exception as e:
                print(f"Failed to start camera: {e}")
                self.cam = None
        else:
            print("No cameras found.")

        # Create UI elements
        # Back Button (Top Left)
        self.back_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (100, 40)),
            text='Back',
            manager=self.manager
        )
        self.ui_elements.append(self.back_btn)

        # Capture Button (Bottom Center-ish)
        # Centered horizontally, near bottom
        btn_width = 120
        btn_height = 50
        x_pos = (self.window_size[0] - btn_width) // 2
        y_pos = self.window_size[1] - 80 

        capture_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x_pos, y_pos), (btn_width, btn_height)),
            text='Capture',
            manager=self.manager
        )
        self.ui_elements.append(capture_btn)
        self.capture_btn = capture_btn # Store reference

    def process_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.back_btn:
                self.screen_manager.switch_to('field')
            elif event.ui_element == self.capture_btn:
                if self.cam:
                    try:
                        image = self.cam.get_image()
                        success = process_image(image)
                        
                        if success:
                            print("Image Captured and Saved!")
                        else:
                            print("Failed to save image.")
                    except Exception as e:
                        print(f"Capture failed: {e}")

    def draw(self, surface):
        # Draw camera feed
        if self.cam:
            try:
                image = self.cam.get_image()
                img_w, img_h = image.get_size()
                scale = max(self.window_size[0] / img_w, self.window_size[1] / img_h)
                scaled_image = pygame.transform.scale(image, (int(img_w * scale), int(img_h * scale)))
                surface.blit(scaled_image, scaled_image.get_rect(center=(self.window_size[0] // 2, self.window_size[1] // 2)))
            except Exception as e:
                 # Draw placeholder if error
                surface.fill((50, 50, 50))
        else:
            # Placeholder for no camera
            surface.fill((100, 100, 100))
            font = pygame.font.Font(None, 36)
            text = font.render("Camera Unavailable", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.window_size[0]//2, self.window_size[1]//2))
            surface.blit(text, text_rect)

    def update(self, time_delta):
       # Camera updates happen in draw via get_image usually, or here.
       pass
       
    def cleanup(self):
        if self.cam:
            self.cam.stop()
        
        for element in self.ui_elements:
            element.kill()
        self.ui_elements.clear()

    def resize(self, new_size):
        self.window_size = new_size
        if self.cam:
            # Camera might need restart if it depends on window size? Usually no.
            pass
            
        # Reposition UI
        if self.back_btn:
            self.back_btn.set_relative_position((10, 10))
            
        if self.capture_btn:
             btn_width = 120
             btn_height = 50
             x_pos = (self.window_size[0] - btn_width) // 2
             y_pos = self.window_size[1] - 80 
             self.capture_btn.set_relative_position((x_pos, y_pos))
