import pygame
import pygame_gui
import pygame.camera

from src.scenes.screen import Screen

class CameraScreen(Screen):
    def __init__(self, manager, window_size):
        super().__init__(manager, window_size)
        self.ui_elements = []
        self.cam = None
        self.camera_surface = None
        
        # Init camera
        cameras = pygame.camera.list_cameras()
        if cameras:
            # Use the first available camera
            try:
                self.cam = pygame.camera.Camera(cameras[0], self.window_size)
                self.cam.start()
            except Exception as e:
                print(f"Failed to start camera: {e}")
                self.cam = None
        else:
            print("No cameras found.")

    def setup(self):
        # Create UI elements
        # Back Button (Top Left)
        back_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (100, 40)),
            text='Back',
            manager=self.manager
        )
        self.ui_elements.append(back_btn)

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
