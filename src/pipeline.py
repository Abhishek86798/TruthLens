from typing import List, Dict, Set, Tuple
from src.preprocessing import (
    clean_html, normalize_text, validate_text,
    enrich_text
)
import logging
from datasketch import MinHash

logger = logging.getLogger(__name__)

class PreprocessingPipeline:
    def __init__(self, min_words: int = 50, similarity_threshold: float = 0.8):
        self.min_words = min_words
        self.similarity_threshold = similarity_threshold
        
    def deduplicate_content(self, texts: List[str]) -> List[str]:
        """Remove near-duplicate texts using MinHash."""
        if not texts:
            return []
            
        unique_texts = []
        minhashes = []
        
        for text in texts:
            current_hash = MinHash(num_perm=128)
            for shingle in self._get_shingles(text):
                current_hash.update(shingle.encode('utf-8'))
                
            # Check similarity with existing texts
            is_duplicate = False
            for idx, existing_hash in enumerate(minhashes):
                if current_hash.jaccard(existing_hash) >= self.similarity_threshold:
                    is_duplicate = True
                    break
                    
            if not is_duplicate:
                unique_texts.append(text)
                minhashes.append(current_hash)
        
        return unique_texts
    
    def _get_shingles(self, text: str, k: int = 5) -> Set[str]:
        """Generate k-shingles from text."""
        text = text.lower()
        return {text[i:i+k] for i in range(len(text) - k + 1)}
    
    def process_batch(self, urls: List[str]) -> List[Dict]:
        """Process a batch of URLs through the complete pipeline."""
        results = []
        
        for url in urls:
            try:
                # Step 1: Clean HTML
                cleaned = clean_html(url)
                
                # Step 2: Normalize text
                normalized = normalize_text(cleaned)
                
                # Step 3: Validate content
                is_valid, reason = validate_text(normalized, self.min_words)
                if not is_valid:
                    logger.info(f"Skipping invalid content: {reason}")
                    continue
                
                # Step 4: Enrich with metadata
                enriched = enrich_text(normalized)
                enriched['url'] = url
                
                results.append(enriched)
                
            except Exception as e:
                logger.error(f"Error processing {url}: {e}")
                continue
        
        # Step 5: Deduplicate
        if results:
            texts = [r['text'] for r in results]
            unique_texts = self.deduplicate_content(texts)
            
            # Keep only non-duplicate results
            results = [r for r in results if r['text'] in unique_texts]
            
        return results
