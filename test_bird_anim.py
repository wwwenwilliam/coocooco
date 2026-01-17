import pygame
import os
import sys

# Add src to path if needed (assuming running from root)
sys.path.append(os.getcwd())

from src.entities.bird import Bird

def test_bird_anim():
    pygame.init()
    # Need display for image loading usually, though modern pygame might handle it.
    # Set a dummy mode just in case
    pygame.display.set_mode((100, 100))
    
    print("Testing Bird Animation...")
    
    # Create a bird
    # Bird(pos, bounds_rect, bird_data=None)
    bird = Bird((0,0), (0,0, 500, 500))
    
    if not bird.using_sprite:
        print("FAIL: Bird is not using sprite. Check assets path.")
        
    print(f"Bird using sprite: {bird.using_sprite}")
    if bird.image:
        print("Initial image set.")
    else:
        print("FAIL: No image set.")

    # Check Dimensions
    expected_size = (261, 340)
    if (bird.width, bird.height) != expected_size:
        print(f"FAIL: Bird dimensions {bird.width}x{bird.height} do not match expected {expected_size}")
    else:
        print(f"SUCCESS: Bird dimensions match expected {expected_size}")

    # Check Y constraint
    # bounds_rect is (0,0, 500, 500)
    # ground_y = 500 * 0.8 = 400
    expected_y = 400 - bird.height
    if int(bird.position.y) != int(expected_y):
        print(f"FAIL: Bird Y position {bird.position.y} does not match expected {expected_y}")
    else:
        print(f"SUCCESS: Bird Y position matches expected ground level constraint ({expected_y})")
        
    # Check Directional Sprites
    if bird.anim_left and bird.anim_right:
        print("SUCCESS: Both left and right animations loaded.")
    else:
        print("FAIL: Missing directional animations.")
        
    # Check Idle Sprites
    if bird.image_idle_right:
        print("SUCCESS: Right idle sprite loaded.")
    else:
        print("FAIL: Right idle sprite not loaded.")

    if bird.image_idle_left:
        print("SUCCESS: Left idle sprite loaded.")
    else:
        print("FAIL: Left idle sprite not loaded.")

    pygame.quit()

if __name__ == "__main__":
    test_bird_anim()
