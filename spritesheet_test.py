import pygame
import sys
import os
from spritestripanim import SpriteStripAnim

# --- Constants ---
FPS = 60
WIDTH, HEIGHT = 400, 300
BG_COLOR = (30, 30, 30)

def create_dummy_spritesheet(filename):
    """Creates a simple sprite sheet for testing purposes."""
    # Create a surface for 4 frames, each 64x64
    frame_width = 64
    frame_height = 64
    sheet_width = frame_width * 4
    sheet_height = frame_height
    
    surface = pygame.Surface((sheet_width, sheet_height))
    surface.fill((255, 0, 255)) # Background (will be colorkey)

    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0)   # Yellow
    ]

    for i, color in enumerate(colors):
        # Draw a circle in each frame
        center = (i * frame_width + frame_width // 2, frame_height // 2)
        pygame.draw.circle(surface, color, center, 25)
        
        # Draw a number
        # (skipping font for simplicity, shapes are enough to see animation)

    pygame.image.save(surface, filename)
    print(f"Created temporary sprite sheet: {filename}")

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sprite Sheet Animation Test")
    clock = pygame.time.Clock()

    # 1. Ensure we have a sprite sheet
    sheet_filename = "Shrug Side-Sheet.png"
    # if not os.path.exists(sheet_filename):
    #     create_dummy_spritesheet(sheet_filename)

    # 2. Setup Animation
    # (0,0,64,64) is the rect of the FIRST frame
    # 4 is the number of frames
    # (255, 0, 255) is the colorkey (magenta)
    # True means loop forever
    # 10 is the number of ticks per frame (speed)
    anim = SpriteStripAnim(sheet_filename, (0, 0, 26, 49), 5, None, True, 10)
    
    # Create an iterator (required by the class implementation logic if we used 'next' manually, 
    # but the class __add__ etc imply we might just use the object if it obeyed iterator protocol well.
    # The modified class is an iterator itself (returns self in __iter__).
    anim_iter = iter(anim)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        try:
            # Get next frame
            image = next(anim_iter)
        except StopIteration:
            # Should not happen if loop=True
            image = pygame.Surface((64, 64)) 

        # Draw
        screen.fill(BG_COLOR)
        
        # Draw the animated sprite in the center
        dest_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(image, dest_rect)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
