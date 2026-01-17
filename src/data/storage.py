import json
import os
import uuid

DATA_FILE = os.path.join('assets', 'saved_birds.json')

def load_birds():
    """Returns a list of saved bird dictionaries."""
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, 'r') as f:
            birds = json.load(f)
            # Migration/Sanity Check: ensure all have id and status
            modified = False
            for bird in birds:
                if 'id' not in bird:
                    bird['id'] = str(uuid.uuid4())
                    modified = True
                if 'status' not in bird:
                    bird['status'] = 'field'
                    modified = True
            
            if modified:
                save_all_birds(birds)
            
            return birds
    except (json.JSONDecodeError, IOError):
        print("Error loading birds data.")
        return []

def save_all_birds(birds):
    """Helper to save the entire list."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(birds, f, indent=4)
        return True
    except IOError as e:
        print(f"Error saving bird data: {e}")
        return False

def save_bird(bird_data):
    """Appends a new bird dictionary to storage."""
    # Add metadata
    bird_data['id'] = str(uuid.uuid4())
    bird_data['status'] = 'field'
    
    birds = load_birds()
    birds.append(bird_data)
    
    if save_all_birds(birds):
        print(f"Bird saved: {bird_data}")
        return True
    return False
    
def update_bird_status(bird_id, new_status):
    """Updates the status of a specific bird."""
    birds = load_birds()
    found = False
    for bird in birds:
        if bird.get('id') == bird_id:
            bird['status'] = new_status
            found = True
            break
    
    if found:
        return save_all_birds(birds)
    return False

def delete_bird(bird_id):
    """Permanently removes a bird."""
    birds = load_birds()
    # Filter out the bird
    new_birds = [b for b in birds if b.get('id') != bird_id]
    
    if len(new_birds) < len(birds):
        return save_all_birds(new_birds)
    return False

def get_birds_by_status(status):
    """Returns filtered list of birds."""
    return [b for b in load_birds() if b.get('status') == status]

def update_bird_data(bird_id, updates):
    """Updates arbitrary fields on a specific bird."""
    birds = load_birds()
    found = False
    for bird in birds:
        if bird.get('id') == bird_id:
            bird.update(updates)
            found = True
            break
    
    if found:
        return save_all_birds(birds)
    return False
