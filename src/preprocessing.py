from bs4 import BeautifulSoup
from langdetect import detect
import re
import logging
import trafilatura
import html
import unicodedata
from typing import Tuple, Dict
from textstat import flesch_reading_ease
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter
from typing import List, Set

logger = logging.getLogger(__name__)

def clean_text(html_text: str) -> str:
    """Clean and normalize HTML text."""
    if not isinstance(html_text, str):
        raise ValueError("Input must be a string")
    
    try:
        soup = BeautifulSoup(html_text, 'html.parser')
        text = soup.get_text(separator=' ')
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    except Exception as e:
        logger.error(f"Text cleaning failed: {e}")
        raise
    

def validate_text(text: str, min_words: int = 50) -> Tuple[bool, str]:
    """
    Validate text content for length and language requirements.
    Returns (True, "valid") if text passes all checks, otherwise (False, reason).
    """
    try:
        # Clean and normalize first
        text = normalize_text(text)
        
        # Check length
        words = [w for w in text.split() if w.strip()]
        if len(words) < min_words:
            return False, f"Text too short: {len(words)} words < {min_words} required"
            
        # Check language
        if not text.strip():
            return False, "Empty text"
            
        if detect(text) != 'en':
            return False, "Text must be in English"
            
        return True, "valid"
        
    except Exception as e:
        logger.error(f"Text validation failed: {e}")
        return False, f"Validation error: {str(e)}"

def check_data_quality(dataset: List[Dict]) -> Dict:
    """
    Check dataset quality and generate detailed statistics.
    Returns quality metrics and potential issues.
    """
    if not dataset:
        return {
            "total_examples": 0,
            "status": "error",
            "error": "Empty dataset"
        }
    
    try:
        # Track issues
        issues = []
        seen_ids: Set[str] = set()
        
        # Required fields
        required_fields = {'id', 'text', 'label', 'annotator'}
        
        # Collect statistics
        total = len(dataset)
        labels_count = Counter()
        text_lengths = []
        missing_fields = Counter()
        duplicate_ids = []

        for item in dataset:
            # Check required fields
            missing = required_fields - set(item.keys())
            if missing:
                missing_fields.update(missing)
            
            # Check for duplicate IDs
            if 'id' in item:
                if item['id'] in seen_ids:
                    duplicate_ids.append(item['id'])
                seen_ids.add(item['id'])
            
            # Collect text lengths
            if 'text' in item:
                text_lengths.append(len(item['text']))
            
            # Count labels
            if 'label' in item:
                labels_count[item['label']] += 1
        
        # Calculate metrics
        avg_length = sum(text_lengths) / len(text_lengths) if text_lengths else 0
        label_distribution = {k: v/total for k, v in labels_count.items()}
        
        # Check class balance
        if labels_count:
            majority_class = max(labels_count.values())
            minority_class = min(labels_count.values())
            balance_ratio = minority_class / majority_class
        else:
            balance_ratio = 0
            issues.append("No valid labels found")
        
        # Compile quality report
        quality_report = {
            "status": "issues" if issues else "ok",
            "total_examples": total,
            "avg_text_length": round(avg_length, 2),
            "label_distribution": label_distribution,
            "class_balance": round(balance_ratio, 3),
            "issues": {
                "missing_fields": dict(missing_fields),
                "duplicate_ids": duplicate_ids,
                "other_issues": issues
            }
        }
        
        return quality_report
        
    except Exception as e:
        logger.error(f"Quality check failed: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "total_examples": len(dataset)
        }

def check_label_balance(dataset: list) -> dict:
    """Calculate label distribution."""
    if not dataset:
        return {}
    
    counts = {}
    for item in dataset:
        label = item.get('label')
        counts[label] = counts.get(label, 0) + 1
    
    total = len(dataset)
    return {label: count/total for label, count in counts.items()}

def clean_html(html: str) -> str:
    """Remove boilerplate content and extract main article text."""
    if not isinstance(html, str):
        raise ValueError("Input must be a string")
    
    try:
        # Get original content length
        original_length = len(html)
        
        # Extract main content using trafilatura
        extracted_text = trafilatura.extract(html)
        
        if not extracted_text:
            # Fallback to basic cleaning if trafilatura fails
            soup = BeautifulSoup(html, 'html.parser')
            # Remove common boilerplate elements
            for element in soup.find_all(['nav', 'header', 'footer', 'script', 'style', 'iframe', 'ad', '.advertisement']):
                element.decompose()
            extracted_text = soup.get_text(separator=' ')
        
        cleaned_length = len(extracted_text)
        reduction = ((original_length - cleaned_length) / original_length) * 100
        
        logger.info(f"Content cleaned: {original_length:,} chars -> {cleaned_length:,} chars ({reduction:.1f}% reduction)")
        
        return extracted_text.strip()
        
    except Exception as e:
        logger.error(f"HTML cleaning failed: {e}")
        raise

def normalize_text(text: str) -> str:
    """Normalize text by cleaning and standardizing format."""
    try:
        # Convert to string and lowercase
        text = str(text).lower()
        
        # Decode HTML entities
        text = html.unescape(text)
        
        # Remove non-UTF characters and normalize Unicode
        text = unicodedata.normalize('NFKD', text)
        text = ''.join(c for c in text if not unicodedata.combining(c))
        
        # Keep only letters, numbers, punctuation, and spaces
        text = re.sub(r'[^\w\s.,!?-]', ' ', text)
        
        # Replace multiple spaces/newlines with single space
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
        
    except Exception as e:
        logger.error(f"Text normalization failed: {e}")
        raise

def detect_citations(text: str) -> bool:
    """Check if text contains citation patterns."""
    citation_patterns = [
        r'\[\d+\]',                    # [1], [2], etc.
        r'\(\d{4}\)',                  # (2023), (2024), etc.
        r'et al\.',                    # et al.
        r'doi:[\w\./-]+',              # DOI patterns
        r'https?://[\w\./&=\?-]+',     # URLs
    ]
    
    return any(re.search(pattern, text, re.IGNORECASE) 
              for pattern in citation_patterns)

def get_sentiment(text: str) -> str:
    """Analyze text sentiment using NLTK VADER."""
    try:
        sia = SentimentIntensityAnalyzer()
        scores = sia.polarity_scores(text)
        
        if scores['compound'] >= 0.05:
            return 'positive'
        elif scores['compound'] <= -0.05:
            return 'negative'
        return 'neutral'
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {e}")
        return 'neutral'

def enrich_text(text: str) -> Dict:
    """
    Enrich text with readability, sentiment, and citation information.
    Returns dict with text metrics and metadata.
    """
    try:
        normalized = normalize_text(text)
        
        return {
            "text": text,
            "readability": flesch_reading_ease(text),
            "sentiment": get_sentiment(normalized),
            "citations": detect_citations(text)
        }
    except Exception as e:
        logger.error(f"Text enrichment failed: {e}")
        return {
            "text": text,
            "readability": 0.0,
            "sentiment": "neutral",
            "citations": False
        }
