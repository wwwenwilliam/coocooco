import torch
from transformers import pipeline

_sentiment_pipeline = None

def get_pipeline():
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        print("Loading sentiment analysis model...")
        # Use simple default model (distilbert-base-uncased-finetuned-sst-2-english)
        # Device logic: check for cuda
        device = 0 if torch.cuda.is_available() else -1
        try:
            _sentiment_pipeline = pipeline("sentiment-analysis", device=device)
        except Exception as e:
            print(f"Failed to load sentiment pipeline on device {device}, trying CPU. Error: {e}")
            _sentiment_pipeline = pipeline("sentiment-analysis", device=-1)
            
    return _sentiment_pipeline

def analyze_text(text):
    """
    Analyzes text and returns a score/label.
    Returns: {'label': 'POSITIVE'|'NEGATIVE', 'score': float}
    """
    if not text or not text.strip():
        return {'label': 'NEUTRAL', 'score': 0.0}
        
    try:
        pipe = get_pipeline()
        # Truncate to 512 chars to match model limit typically
        result = pipe(text[:512])[0]
        return result
    except Exception as e:
        print(f"Sentiment analysis failed: {e}")
        return {'label': 'NEUTRAL', 'score': 0.0}
