import sys
import os
import pygame

# Mock pygame
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.display.set_mode((1, 1))

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.entities.bird import Bird
from src.data.events import EVENT_HAPPY, EVENT_SAD, EVENT_ANGRY

def test_bird_state_persistence():
    print("Testing Bird State Persistence...")
    
    # Mock data
    bird_data = {"id": "test", "species": "owl"}
    bird = Bird(bird_data, (0, 0))
    
    # 1. Initial State
    assert bird.state == 0 # IDLE
    print(f"Initial State: {bird.state} (OK)")
    
    # 2. Trigger Event
    bird.trigger_random_event()
    assert bird.state in [EVENT_HAPPY, EVENT_SAD, EVENT_ANGRY]
    assert bird.current_event is not None
    event_state = bird.state
    print(f"Triggered Event State: {bird.state} (OK)")
    
    # 3. specific update (simulate frames)
    # We need to simulate dt
    for i in range(100):
        bird.update(0.016) # 60fps
        # State should NOT change back to IDLE
        if bird.state != event_state:
            print(f"FAILURE: State changed to {bird.state} at frame {i}")
            return False
            
    print("State persisted after 100 updates (OK)")
    
    # 4. Check if current_event is unexpectedly None
    if bird.current_event is None:
        print("FAILURE: current_event became None")
        return False
        
    print("SUCCESS: Bird state persists correctly.")
    return True

if __name__ == "__main__":
    if test_bird_state_persistence():
        sys.exit(0)
    else:
        sys.exit(1)
