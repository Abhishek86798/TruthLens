from src.pipeline import PreprocessingPipeline
import pytest

def test_preprocessing_pipeline():
    """Test complete preprocessing pipeline."""
    # Sample HTML documents
    test_docs = [
        # Document 1: Valid
        """<article><h1>Climate Change Study</h1>
        <p>Scientists report significant findings about global warming.
        The study conducted in 2023 shows clear evidence of temperature rise.
        Multiple data sources confirm these trends.</p></article>""",
        
        # Document 2: Duplicate of 1 with slight changes
        """<article><h1>Climate Change Research</h1>
        <p>Scientists report important findings about global warming.
        The study conducted in 2023 shows clear evidence of temperature rise.
        Multiple sources confirm these trends.</p></article>""",
        
        # Document 3: Too short
        """<p>Just a brief note.</p>""",
        
        # Document 4: Valid but different
        """<article><h1>AI Development</h1>
        <p>Recent advances in artificial intelligence have led to significant
        breakthroughs in natural language processing. Researchers demonstrate
        impressive results in various applications.</p></article>""",
        
        # Document 5: Non-English
        """<article><h1>Estudio Científico</h1>
        <p>Los científicos reportan hallazgos importantes sobre el cambio
        climático global. El estudio muestra evidencia clara.</p></article>"""
    ]
    
    pipeline = PreprocessingPipeline(min_words=20)
    results = pipeline.process_batch(test_docs)
    
    # Verify results
    assert len(results) == 2  # Should keep only 2 valid, unique documents
    
    # Check enrichment
    for result in results:
        assert 'readability' in result
        assert 'sentiment' in result
        assert 'citations' in result
        assert len(result['text']) > 0

    # Verify deduplication worked
    texts = [r['text'] for r in results]
    assert len(texts) == len(set(texts))  # All texts should be unique
