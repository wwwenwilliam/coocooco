import pygame
import sys
import os
from spritestripanim import SpriteStripAnim

# --- Constants ---
FPS = 60
WIDTH, HEIGHT = 390, 844
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
    sheet_filename = "owl_walk.png"
    # if not os.path.exists(sheet_filename):
    #     create_dummy_spritesheet(sheet_filename)

    # SPRITE SHEET DIMENSIONS --------------------------
    # SPARROW: (0, 0, 220, 158)
    # PIGEON: (0, 0, 240, 206)
    # OWL: (0, 0, 261, 340)
    # --------------------------------------------------

    # 2. Setup Animation
    # Sparrow
    anim = SpriteStripAnim(sheet_filename, (0, 0, 261, 340), 2, None, True, 8)
    anim_iter = iter(anim)

    # Happy Overlay
    # Dimensions: 302x143. Assuming standard strip.
    # Note: Please update the '6' below to the correct number of frames if different!
    happy_filename = "happy.png"
    anim_happy = SpriteStripAnim(happy_filename, (0, 0, 281, 210), 2, None, True, 12)
    happy_iter = iter(anim_happy)

    # Position variables
    x = 0
    y = HEIGHT // 2
    speed = 2

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        try:
            image = next(anim_iter)
            image_happy = next(happy_iter)
        except StopIteration:
            image = pygame.Surface((64, 64)) 
            image_happy = pygame.Surface((302, 143))

        # Move sprite
        x += speed
        if x > WIDTH:
            x = -image.get_width() # Reset to off-screen left

        # Draw
        screen.fill(BG_COLOR)
        
        # Draw the animated sparrow
        dest_rect = image.get_rect(midleft=(x, y))
        screen.blit(image, dest_rect)

        # Draw the happy overlay ON TOP of the sparrow
        # Centered on the sparrow
        happy_rect = image_happy.get_rect(center=dest_rect.center)
        screen.blit(image_happy, happy_rect)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
