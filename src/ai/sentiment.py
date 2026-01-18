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
            # Zero-Shot Classification for custom traits
            # Using distilbart-mnli-12-1 for speed/efficiency
            _sentiment_pipeline = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-1", device=device)
        except Exception as e:
            print(f"Failed to load pipeline on device {device}, trying CPU. Error: {e}")
            _sentiment_pipeline = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-1", device=-1)
            
    return _sentiment_pipeline

def analyze_text(text, candidate_labels=None):
    """
    Analyzes text against candidate trait labels.
    Returns: Dict[str, float] (e.g., {'Intelligent': 0.8, 'Lazy': 0.1})
    """
    if not text or not text.strip():
        return {}
        
    if candidate_labels is None:
        candidate_labels = ['Intelligent', 'Curious', 'Brave', 'Lazy', 'Friendly']

    try:
        pipe = get_pipeline()
        # multi_label=True allows multiple traits to apply independently? 
        # Or False to force them to sum to 1? User probably wants relative dominance.
        # False (default) makes them mutually exclusive (sum=1). 
        # Given "score them", mutex is good for finding the DOMINANT one.
        result = pipe(text[:512], candidate_labels, multi_label=False)
        
        # Result format: {'labels': [...], 'scores': [...]}
        scores = {label: score for label, score in zip(result['labels'], result['scores'])}
        return scores
    except Exception as e:
        print(f"Trait analysis failed: {e}")
        return {}
