from src.deduplication import deduplicate_content
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_deduplication():
    print("\n=== Testing Content Deduplication ===")
    
    # Test cases
    texts = [
        # Exact duplicates
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over the lazy dog",
        
        # Near duplicate
        "The quick brown fox jumps over a lazy dog",
        
        # Distinct text
        "This is a completely different text about something else"
    ]
    
    print(f"\nOriginal texts: {len(texts)}")
    for i, text in enumerate(texts, 1):
        print(f"\n{i}. {text[:50]}...")
        
    # Run deduplication
    unique_texts = deduplicate_content(texts, threshold=0.9)
    
    print(f"\nAfter deduplication: {len(unique_texts)}")
    for i, text in enumerate(unique_texts, 1):
        print(f"\n{i}. {text[:50]}...")

if __name__ == "__main__":
    test_deduplication()
