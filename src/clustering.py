import numpy as np
from typing import List, Dict, Any, Tuple
from src.logger import get_logger

try:
    import umap
    import hdbscan
except ImportError:
    umap = None
    hdbscan = None

logger = get_logger(__name__)

def cluster_embeddings(embeddings: np.ndarray, reviews: List[Dict[str, Any]], min_cluster_size: int = 5) -> Tuple[Dict[int, List[Dict[str, Any]]], int]:
    """
    Reduces the dimensionality of embeddings using UMAP, then clusters them using HDBSCAN.
    Returns a dictionary mapping cluster_id to a list of reviews in that cluster,
    and the total number of clusters found (excluding noise).
    
    Noise points are assigned to cluster_id -1.
    """
    if len(embeddings) == 0 or len(reviews) == 0:
        return {}, 0
        
    if umap is None or hdbscan is None:
        raise ImportError("umap-learn and hdbscan are required for clustering. Please install them.")
        
    if len(embeddings) != len(reviews):
        raise ValueError("Number of embeddings must match the number of reviews.")
        
    logger.info(f"Reducing dimensionality with UMAP for {len(embeddings)} vectors...")
    
    # Adjust n_neighbors based on the dataset size to prevent errors on very small batches
    n_neighbors = min(15, len(embeddings) - 1) if len(embeddings) > 2 else 2
    
    reducer = umap.UMAP(
        n_neighbors=n_neighbors, 
        n_components=5, 
        metric='cosine', 
        random_state=42
    )
    reduced_embeddings = reducer.fit_transform(embeddings)
    
    logger.info(f"Clustering with HDBSCAN (min_cluster_size={min_cluster_size})...")
    
    # Adjust min_cluster_size if we have very few reviews
    actual_min_size = min(min_cluster_size, len(embeddings))
    if actual_min_size < 2:
        actual_min_size = 2
        
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=actual_min_size,
        min_samples=1,
        metric='euclidean'
    )
    
    labels = clusterer.fit_predict(reduced_embeddings)
    
    # Group reviews by cluster
    clusters: Dict[int, List[Dict[str, Any]]] = {}
    for label, review in zip(labels, reviews):
        cluster_id = int(label)
        if cluster_id not in clusters:
            clusters[cluster_id] = []
        clusters[cluster_id].append(review)
        
    num_clusters = len([k for k in clusters.keys() if k != -1])
    logger.info(f"Found {num_clusters} valid clusters and {len(clusters.get(-1, []))} noise points.")
    
    return clusters, num_clusters
