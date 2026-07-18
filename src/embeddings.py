from typing import List, Dict, Any
import numpy as np
from src.logger import get_logger

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

logger = get_logger(__name__)

# Using a very lightweight and fast open source model
# all-MiniLM-L6-v2 produces 384-dimensional vectors
MODEL_NAME = 'all-MiniLM-L6-v2'
_model = None

def get_model():
    global _model
    if _model is None:
        if SentenceTransformer is None:
            raise ImportError("sentence-transformers is not installed. Please install it to use open source embeddings.")
        logger.info(f"Loading local embedding model: {MODEL_NAME}")
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def generate_embeddings(reviews: List[Dict[str, Any]]) -> np.ndarray:
    """
    Generates embeddings for the given list of reviews using an open-source local model.
    The review content is extracted, and the dense vectors are returned as a numpy array.
    """
    if not reviews:
        return np.array([])
        
    model = get_model()
    
    # Extract the scrubbed text from the reviews
    texts = []
    for r in reviews:
        # Fallback to empty string if content is missing
        text = r.get('content', '')
        texts.append(text)
        
    logger.info(f"Generating embeddings for {len(texts)} reviews using {MODEL_NAME}...")
    
    # encode() returns a numpy array of shape (len(texts), 384)
    embeddings = model.encode(texts, show_progress_bar=False)
    
    logger.info("Embeddings generation complete.")
    return embeddings
