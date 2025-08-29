import pytest
from src.deduplication import deduplicate_content, calculate_similarity

def test_exact_duplicates():
    """Test removal of exact duplicate texts."""
    texts = [
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over the lazy dog",  # Exact duplicate
        "Different text entirely"
    ]
    result = deduplicate_content(texts, threshold=0.9)
    assert len(result) == 2
    assert "Different text entirely" in result

def test_near_duplicates():
    """Test removal of near-duplicate texts with small changes."""
    texts = [
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over a lazy dog",  # Minor change
        "Completely different content here"
    ]
    result = deduplicate_content(texts, threshold=0.9)
    assert len(result) == 2
    assert "Completely different content here" in result

def test_distinct_texts():
    """Test preservation of distinct texts."""
    texts = [
        "First unique text about something",
        "Second text about something else entirely",
        "Third completely different content"
    ]
    result = deduplicate_content(texts, threshold=0.9)
    assert len(result) == len(texts)
    assert set(result) == set(texts)

def test_similarity_calculation():
    """Test Jaccard similarity calculation."""
    text1 = "The quick brown fox"
    text2 = "The quick brown fox jumps"  # Similar
    text3 = "Completely different"  # Different
    
    sim1 = calculate_similarity(text1, text2)
    sim2 = calculate_similarity(text1, text3)
    
    assert sim1 > 0.7  # Similar texts
    assert sim2 < 0.3  # Different texts
