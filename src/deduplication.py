from typing import List, Set
from datasketch import MinHash, LeanMinHash
import re
import logging

logger = logging.getLogger(__name__)

def get_shingles(text: str, k: int = 5) -> Set[str]:
    """Convert text to k-shingles (character n-grams)."""
    text = re.sub(r'\s+', ' ', text.lower().strip())
    return {text[i:i+k] for i in range(len(text) - k + 1)}

def calculate_similarity(text1: str, text2: str, num_perm: int = 128) -> float:
    """Calculate Jaccard similarity between two texts using MinHash."""
    m1, m2 = MinHash(num_perm=num_perm), MinHash(num_perm=num_perm)
    
    # Add shingles to MinHash
    for shingle in get_shingles(text1):
        m1.update(shingle.encode('utf-8'))
    for shingle in get_shingles(text2):
        m2.update(shingle.encode('utf-8'))
    
    return m1.jaccard(m2)

def deduplicate_content(texts: List[str], threshold: float = 0.9) -> List[str]:
    """Remove near-duplicate texts using MinHash/LSH."""
    if not texts:
        return []
    
    try:
        # Keep track of unique texts and their MinHashes
        unique_texts = []
        minhashes = []
        
        for text in texts:
            is_duplicate = False
            current_minhash = MinHash(num_perm=128)
            
            # Create MinHash for current text
            for shingle in get_shingles(text):
                current_minhash.update(shingle.encode('utf-8'))
            
            # Compare with existing unique texts
            for idx, existing_minhash in enumerate(minhashes):
                if current_minhash.jaccard(existing_minhash) >= threshold:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_texts.append(text)
                minhashes.append(current_minhash)
        
        logger.info(f"Deduplicated {len(texts)} texts to {len(unique_texts)} unique texts")
        return unique_texts
        
    except Exception as e:
        logger.error(f"Deduplication failed: {str(e)}")
        return texts
