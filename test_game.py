import pygame
import sys
import tkinter as tk
from tkinter import filedialog
import os

# --- Configuration ---
WIDTH, HEIGHT = 400, 800  # Dimensions mimicking a mobile screen (9:18 aspect ratio)
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
BLUE = (50, 100, 255)

def open_file_dialog():
    """
    Opens a system file dialog to select an image.
    Returns the path to the file or None if cancelled.
    """
    # Initialize tkinter root for the dialog
    root = tk.Tk()
    root.withdraw()  # Hide the small main tkinter window

    # Open file explorer
    file_path = filedialog.askopenfilename(
        title="Select a Photo",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )
    
    root.destroy() # Clean up tkinter
    return file_path

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mobile Upload Prototype")
    clock = pygame.time.Clock()

    # Font setup
    font = pygame.font.SysFont("Arial", 24)
    
    # Button properties
    button_rect = pygame.Rect(0, 0, 200, 60)
    button_rect.center = (WIDTH // 2, HEIGHT // 2)
    
    button_color = GRAY
    button_text = "Upload Photo"
    status_message = "Waiting for upload..."
    detected_color = None

    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if button_rect.collidepoint(event.pos):
                        # Visual feedback for click
                        button_color = DARK_GRAY
                        pygame.display.flip() 
                        
                        # Open the dialog
                        print("Opening file dialog...")
                        file_path = open_file_dialog()
                        
                        if file_path:
                            # Truncate path for display if it's too long
                            filename = os.path.basename(file_path)
                            status_message = f"Loaded: {filename}"
                            print(f"File Selected: {file_path}")
                            
                            try:
                                # Load image and get average color
                                img = pygame.image.load(file_path)
                                detected_color = pygame.transform.average_color(img)
                                print(f"Detected Average Color: {detected_color}")
                            except Exception as e:
                                print(f"Error processing image: {e}")
                                status_message = "Error loading image"
                                detected_color = None
                        else:
                            status_message = "Upload cancelled."
                            print("No file selected.")

            if event.type == pygame.MOUSEBUTTONUP:
                button_color = GRAY

        # 2. Drawing
        screen.fill(WHITE)

        # Draw the phone bezel/border for effect (optional)
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, HEIGHT), 10)

        # Draw Button
        pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, button_rect, 2, border_radius=10)

        # Draw Button Text
        text_surf = font.render(button_text, True, BLACK)
        text_rect = text_surf.get_rect(center=button_rect.center)
        screen.blit(text_surf, text_rect)

        # Draw Status Message
        status_surf = font.render(status_message, True, BLACK)
        status_rect = status_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        screen.blit(status_surf, status_rect)

        # Draw Detected Color
        if detected_color:
            # Draw color swatch
            color_rect = pygame.Rect(0, 0, 100, 100)
            color_rect.center = (WIDTH // 2, HEIGHT // 2 + 150)
            pygame.draw.rect(screen, detected_color, color_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, color_rect, 2, border_radius=10)

            # Draw RGB Text
            color_text = f"RGB: {detected_color[:3]}"
            color_surf = font.render(color_text, True, BLACK)
            color_rect = color_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 220))
            screen.blit(color_surf, color_rect)

        # 3. Update Display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()