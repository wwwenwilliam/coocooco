import pygame
import os
import datetime
from transformers import pipeline
from PIL import Image
from ultralytics import YOLO
from src.data.storage import save_bird

CAPTURES_DIR = os.path.join('assets', 'captures')
CLASSIFIER = None
DETECTOR = None

def get_classifier():
    global CLASSIFIER
    if CLASSIFIER is None:
        print("Loading local bird classification model... this may take a moment.")
        # Device -1 means CPU. Users with CUDA could use device=0, but let's stick to CPU for safety/compat.
        CLASSIFIER = pipeline("image-classification", model="chriamue/bird-species-classifier")
    return CLASSIFIER

def get_detector():
    global DETECTOR
    if DETECTOR is None:
        print("Loading YOLO object detector...")
        DETECTOR = YOLO("yolo11n.pt")
    return DETECTOR

def identify_bird(image_path):
    """
    Identifies bird species using local transformers model.
    Returns the top label description or 'Unknown Bird'.
    """
    try:
        classifier = get_classifier()
        # Transformers pipeline accepts file path directly
        results = classifier(image_path)
        
        # Returns list like [{'label': 'species', 'score': 0.9}, ...]
        if results and len(results) > 0:
            top_result = results[0]
            return top_result['label']
            
    except Exception as e:
        print(f"Identification failed: {e}")
        
    return 'Unknown Bird'

def detect_and_crop(image_path):
    """
    Detects a bird in the image and returns the path to the cropped image.
    Returns None if no bird is detected or detection fails.
    """
    try:
        detector = get_detector()
        # Run inference, suppress verbose output
        results = detector(image_path, verbose=False)
        
        # COCO class 14 is 'bird'
        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])
                if cls == 14: # bird
                    xyxy = box.xyxy[0].tolist()
                    
                    with Image.open(image_path) as img:
                        crop = img.crop((xyxy[0], xyxy[1], xyxy[2], xyxy[3]))
                        
                        crops_dir = os.path.join(CAPTURES_DIR, 'crops')
                        if not os.path.exists(crops_dir):
                            os.makedirs(crops_dir)
                            
                        filename = os.path.basename(image_path)
                        crop_path = os.path.join(crops_dir, filename)
                        crop.save(crop_path)
                        print(f"Bird detected and cropped to: {crop_path}")
                        return crop_path
                        
        print("No bird detected in image.")
        return None
    except Exception as e:
        print(f"Detection failed: {e}")
        return None

def process_image(surface):
    """
    Saves the provided surface to disk and records it in storage.
    Returns True on success, False otherwise.
    """
    if not os.path.exists(CAPTURES_DIR):
        os.makedirs(CAPTURES_DIR)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bird_{timestamp}.png"
    filepath = os.path.join(CAPTURES_DIR, filename)

    try:
        pygame.image.save(surface, filepath)
        
        # Detect and crop
        crop_path = detect_and_crop(filepath)
        inference_path = crop_path if crop_path else filepath
        
        # Identify bird species
        species = identify_bird(inference_path)

        # Save metadata
        bird_data = {
            'image_path': filepath,
            'timestamp': datetime.datetime.now().isoformat(),
            'species': species,
            'cropped_path': crop_path # Optional: store this too?
        }
        if save_bird(bird_data):
            print(f"Processed and saved: {filepath} (Species: {species})")
            return True
        else:
            return False

    except Exception as e:
        print(f"Failed to process image: {e}")
        return False
