import os
import json
import time
from typing import List, Dict, Any, Optional
from src.logger import get_logger

try:
    from openai import OpenAI
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    OpenAI = None
    load_dotenv = None

logger = get_logger(__name__)

def get_openai_client() -> Optional[Any]:
    if OpenAI is None:
        logger.error("OpenAI library is not installed.")
        return None
        
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.warning("GROQ_API_KEY not found in environment variables.")
        return None
        
    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

def summarize_cluster(cluster_id: int, reviews: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Uses an LLM to generate a theme name, actionable ideas, and extract representative 
    quotes for a given cluster of reviews.
    """
    client = get_openai_client()
    if not client:
        return None
        
    logger.info(f"Summarizing Cluster {cluster_id} containing {len(reviews)} reviews...")
    
    # Prepare the context
    # Only send the review content to keep token usage low
    # TRUNCATE to avoid hitting Groq's 12K Tokens Per Minute limit
    max_reviews_per_prompt = 40
    review_texts = [r.get('content', '') for r in reviews if r.get('content')]
    if len(review_texts) > max_reviews_per_prompt:
        logger.info(f"Truncating from {len(review_texts)} to {max_reviews_per_prompt} reviews to respect TPM limits.")
        review_texts = review_texts[:max_reviews_per_prompt]
        
    context = "\n".join([f"- {text}" for text in review_texts])
    
    prompt = f"""
You are an expert product manager analyzing app reviews for a fintech application (Groww).
Below is a cluster of user reviews that are semantically similar.

Reviews:
{context}

Analyze these reviews and provide a JSON response with the following keys:
1. "theme_name": A short, concise name for this cluster's theme (e.g., "App performance & bugs").
2. "actionable_ideas": A list of 2-3 short, actionable ideas or recommendations for the product or support team based on these reviews.
3. "verbatim_quotes": A list of 1-3 exact, representative quotes from the reviews above. The quotes MUST be copied exactly word-for-word from the text above.

Output ONLY valid JSON.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Using Groq's high-performance model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that outputs only raw, valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" },
            temperature=0.3
        )
        
        result_json = response.choices[0].message.content
        result = json.loads(result_json)
        
        # Add the original reviews to the result
        result['cluster_id'] = cluster_id
        result['review_count'] = len(reviews)
        
        # VALIDATE QUOTES (Anti-Hallucination Post-Processor)
        validated_quotes = []
        for quote in result.get('verbatim_quotes', []):
            # Check if this exact string (ignoring case/whitespace slightly) exists in the original texts
            found = False
            clean_quote = quote.lower().strip()
            for text in review_texts:
                if clean_quote in text.lower():
                    found = True
                    break
            
            if found:
                validated_quotes.append(quote)
            else:
                logger.warning(f"Discarded hallucinated quote in Cluster {cluster_id}: {quote}")
                
        result['verbatim_quotes'] = validated_quotes
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to summarize Cluster {cluster_id}: {str(e)}")
        return None

def process_all_clusters(clusters: Dict[int, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """
    Iterates over all valid clusters (excluding noise) and summarizes them.
    Sorts the themes by the number of reviews they represent.
    """
    summaries = []
    
    for cluster_id, reviews in clusters.items():
        # Skip the noise cluster (-1) unless it's the only thing we have
        if cluster_id == -1 and len(clusters) > 1:
            continue
            
        summary = summarize_cluster(cluster_id, reviews)
        if summary:
            summaries.append(summary)
            
        # Add a sleep to respect Groq's Rate Limits (30 Requests Per Minute)
        logger.debug("Sleeping for 2.5s to respect Groq RPM limits...")
        time.sleep(2.5)
            
    # Sort summaries by review_count descending (largest themes first)
    summaries.sort(key=lambda x: x.get('review_count', 0), reverse=True)
    
    return summaries
