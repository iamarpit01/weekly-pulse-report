from datetime import datetime, timedelta
import random
from typing import List, Dict, Any
from google_play_scraper import reviews, Sort
from src.logger import get_logger

logger = get_logger(__name__)

def fetch_play_store_reviews(app_id: str, weeks_ago: int = 8, max_reviews: int = 1000) -> List[Dict[str, Any]]:
    """
    Fetches reviews from the Google Play Store for the given app_id.
    Filters reviews to only include those from the last `weeks_ago` weeks.
    Limits the final output to `max_reviews` to prevent LLM token limits from being exceeded.
    """
    logger.info(f"Fetching Play Store reviews for {app_id} for the last {weeks_ago} weeks...")
    
    # Calculate the cutoff date
    cutoff_date = datetime.now() - timedelta(weeks=weeks_ago)
    
    fetched_reviews = []
    continuation_token = None
    
    # Batch size for each API call
    batch_size = 200
    
    # Safety limit to prevent infinite loops if the app has millions of new reviews
    max_api_calls = 50 
    api_calls = 0

    while api_calls < max_api_calls:
        api_calls += 1
        logger.debug(f"Fetching batch {api_calls}...")
        
        try:
            result, continuation_token = reviews(
                app_id,
                lang='en',
                country='in',
                sort=Sort.NEWEST,
                count=batch_size,
                continuation_token=continuation_token
            )
            
            # Filter by date
            valid_batch = []
            reached_cutoff = False
            for r in result:
                if r['at'] >= cutoff_date:
                    # Normalize: Only keep reviews with 10 or more words
                    content = r.get('content', '')
                    if content and len(content.split()) >= 10:
                        # Remove unwanted keys to minimize payload size
                        for key in ['reviewCreatedVersion', 'at', 'replyContent', 'repliedAt']:
                            r.pop(key, None)
                        valid_batch.append(r)
                else:
                    reached_cutoff = True
                    
            fetched_reviews.extend(valid_batch)
            
            # If we've reached reviews older than the cutoff, we can stop fetching
            if reached_cutoff or not continuation_token:
                break
                
        except Exception as e:
            logger.error(f"Error fetching reviews: {str(e)}")
            break

    logger.info(f"Found {len(fetched_reviews)} reviews in the last {weeks_ago} weeks.")
    
    # Sample/Limit reviews if they exceed max_reviews
    if len(fetched_reviews) > max_reviews:
        logger.info(f"Limiting to {max_reviews} reviews to prevent token limit issues.")
        # We can sample based on length, score, or randomly. 
        # Here we randomly sample to get a balanced pulse, or we could sort by helpfulness.
        # Sorting by 'score' (e.g. 1-2 stars) could be useful for finding issues, 
        # but random gives a general pulse. Let's do random sampling.
        fetched_reviews = random.sample(fetched_reviews, max_reviews)

    return fetched_reviews
