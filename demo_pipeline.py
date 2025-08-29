from src.pipeline import PreprocessingPipeline
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def demo_pipeline():
    # Sample HTML documents
    sample_docs = [
        # Doc 1: Valid article
        """
        <article>
            <h1>Climate Change Study</h1>
            <p>According to recent research by Smith et al. (2023), global temperatures 
            have risen significantly. The study demonstrates clear evidence of climate
            change impacts across multiple regions. Further data from satellite
            observations confirms these findings.</p>
        </article>
        """,
        
        # Doc 2: Too short
        "<p>Just a short note.</p>",
        
        # Doc 3: Similar to Doc 1 (near-duplicate)
        """
        <article>
            <h1>Climate Research</h1>
            <p>According to recent studies by Smith et al. (2023), global temperatures 
            have increased significantly. The research shows clear evidence of climate
            change effects across many regions. Satellite data confirms these results.</p>
        </article>
        """
    ]

    print("\n=== TruthLens Preprocessing Pipeline Demo ===")
    
    # Initialize pipeline
    pipeline = PreprocessingPipeline(min_words=20)
    
    # Process documents
    results = pipeline.process_batch(sample_docs)
    
    # Show results
    print(f"\nProcessed {len(sample_docs)} documents")
    print(f"Unique documents after filtering: {len(results)}")
    
    for i, doc in enumerate(results, 1):
        print(f"\nDocument {i}:")
        print("-" * 50)
        print(f"Readability score: {doc['readability']:.1f}")
        print(f"Sentiment: {doc['sentiment']}")
        print(f"Contains citations: {doc['citations']}")
        print(f"Text preview: {doc['text'][:100]}...")

if __name__ == "__main__":
    demo_pipeline()
