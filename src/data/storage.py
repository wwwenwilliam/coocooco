import json
import os

DATA_FILE = os.path.join('assets', 'saved_birds.json')

def load_birds():
    """Returns a list of saved bird dictionaries."""
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Error loading birds data.")
        return []

def save_bird(bird_data):
    """Appends a new bird dictionary to storage."""
    birds = load_birds()
    birds.append(bird_data)
    
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(birds, f, indent=4)
        print(f"Bird saved: {bird_data}")
        return True
    except IOError as e:
        print(f"Error saving bird data: {e}")
        return False
