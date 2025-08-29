from src.preprocessing import enrich_text
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_enrichment_tests():
    # Test cases with different characteristics
    test_cases = [
        {
            "name": "Academic text",
            "text": """According to Smith et al. (2023), global warming has increased 
            by 1.5°C [1]. Further studies (doi:10.1234/climate) support these findings."""
        },
        {
            "name": "Positive sentiment",
            "text": """The breakthrough research demonstrates excellent results, showing 
            promising advances in renewable energy technology."""
        },
        {
            "name": "Technical text",
            "text": """The algorithm processes data using a multi-layered neural network
            architecture with backpropagation."""
        }
    ]

    print("\n=== Testing Text Enrichment ===")
    
    for case in test_cases:
        print(f"\nTest Case: {case['name']}")
        print("-" * 50)
        
        # Get enrichment data
        enriched = enrich_text(case['text'])
        
        # Display results
        print(f"Input preview: {case['text'][:50]}...")
        print(f"\nMetrics:")
        print(f"• Readability score: {enriched['readability']:.1f}")
        print(f"• Sentiment: {enriched['sentiment']}")
        print(f"• Citations detected: {enriched['citations']}")

if __name__ == "__main__":
    try:
        run_enrichment_tests()
    finally:
        # Cleanup test file
        print("\nCleaning up test file...")
        os.remove(__file__)
    try:
        test_text_enrichment()
    finally:
        # Clean up test file
        print("\nCleaning up test file...")
        os.remove(__file__)
