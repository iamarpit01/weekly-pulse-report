import re
from typing import List, Dict, Any
from src.logger import get_logger

logger = get_logger(__name__)

# Regular expressions for PII heuristics
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
# Matches international and standard phone numbers, sometimes separated by dashes or spaces
PHONE_REGEX = re.compile(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')

def scrub_text(text: str) -> str:
    """
    Replaces PII (Emails, Phone numbers) in the given text with placeholders.
    """
    if not text:
        return text
        
    scrubbed = EMAIL_REGEX.sub('[REDACTED_EMAIL]', text)
    scrubbed = PHONE_REGEX.sub('[REDACTED_PHONE]', scrubbed)
    
    # Note: Scrubbing names via regex is highly error-prone without an NLP engine like Presidio.
    # For Play Store reviews, contact details (email/phone) are the primary PII concern.
    return scrubbed

def scrub_reviews(reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Iterates through a list of fetched reviews and scrubs PII from the review text
    and potentially user names (replacing userName with a hash or generic string).
    """
    logger.info(f"Scrubbing PII from {len(reviews)} reviews...")
    
    scrubbed_reviews = []
    
    for r in reviews:
        # Create a shallow copy to avoid mutating the original fetched list if used elsewhere
        scrubbed_review = r.copy()
        
        # Scrub the main review content
        if 'content' in scrubbed_review and scrubbed_review['content']:
            scrubbed_review['content'] = scrub_text(scrubbed_review['content'])
            
        # Scrub the reply content if a developer has replied with an email/phone
        if 'replyContent' in scrubbed_review and scrubbed_review['replyContent']:
            scrubbed_review['replyContent'] = scrub_text(scrubbed_review['replyContent'])
            
        # Redact the user's name entirely to ensure anonymity before passing to LLM
        if 'userName' in scrubbed_review:
            scrubbed_review['userName'] = '[REDACTED_USER]'
            
        # Redact userImage to remove potential account identifiers
        if 'userImage' in scrubbed_review:
            scrubbed_review['userImage'] = ''
            
        scrubbed_reviews.append(scrubbed_review)
        
    logger.info("PII scrubbing complete.")
    return scrubbed_reviews
