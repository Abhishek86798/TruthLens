import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from bs4 import BeautifulSoup
from langdetect import detect
from src.preprocessing import clean_text, validate_content, clean_html, normalize_text, validate_text, enrich_text

class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        self.html_samples = {
            "valid": """
                <div class="content">
                    <h1>Test Title</h1>
                    <p>This is a sample paragraph with enough English words to pass the minimum length requirement. 
                    We need to make sure this text is long enough to meet the validation criteria. Adding more 
                    meaningful content here to ensure we have more than fifty words in total. The quick brown fox 
                    jumps over the lazy dog multiple times to reach our word count goal.</p>
                </div>
            """,
            "short": "<p>Too short</p>",
            "invalid": "<unclosed>test"
        }

    def test_clean_text(self):
        result = clean_text(self.html_samples["valid"])
        self.assertIsInstance(result, str)
        self.assertFalse('<' in result)
        self.assertFalse('>' in result)

    def test_validate_content(self):
        cleaned = clean_text(self.html_samples["valid"])
        is_valid, reasons = validate_content(cleaned)
        self.assertTrue(is_valid)
        self.assertEqual(len(reasons), 0)

    def test_clean_html(self):
        # Sample HTML with boilerplate
        sample_html = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <nav>
                    <a href="#">Home</a>
                    <a href="#">About</a>
                </nav>
                <div class="advertisement">
                    Buy now! Special offer!
                </div>
                <article>
                    <h1>Main Article</h1>
                    <p>This is the main content that should be preserved.</p>
                    <p>Important information here.</p>
                </article>
                <footer>
                    Copyright 2025
                </footer>
            </body>
        </html>
        """
        
        cleaned = clean_html(sample_html)
        
        # Check content preservation
        self.assertIn("Main Article", cleaned)
        self.assertIn("Important information", cleaned)
        
        # Check boilerplate removal
        self.assertNotIn("Buy now! Special offer!", cleaned)
        self.assertNotIn("Copyright 2025", cleaned)
        self.assertNotIn("Home", cleaned)

    def test_clean_html_empty(self):
        """Test handling of empty/invalid HTML."""
        with self.assertRaises(ValueError):
            clean_html(None)
        
        self.assertEqual(clean_html(""), "")

    def test_clean_html_no_boilerplate(self):
        """Test HTML that's already clean."""
        clean_text = "Simple text without HTML"
        result = clean_html(f"<p>{clean_text}</p>")
        self.assertIn(clean_text, result)

    def test_normalize_html_entities(self):
        """Test normalization of HTML entities and messy text."""
        messy_text = """
        <p>This &amp; that&nbsp;are   entities</p>
        with Multiple   Spaces &lt;tag&gt;
        and\nmultiple\r\nlines
        """
        
        normalized = normalize_text(messy_text)
        
        self.assertIn("this & that", normalized)
        self.assertNotIn("<tag>", normalized)  # HTML tags removed
        self.assertNotIn("  ", normalized)    # No double spaces
        self.assertNotIn("\n", normalized)    # No newlines

    def test_normalize_special_chars(self):
        """Test handling of special characters and whitespace."""
        special_text = "Hello©™®   World\t\n   with–special—chars"
        normalized = normalize_text(special_text)
        
        self.assertEqual(normalized, "hello world with-special-chars")
        self.assertEqual(len(normalized.split()), 4)  # Words properly separated

    def test_validate_text_length(self):
        """Test text length validation."""
        # Short text
        short_text = "This is too short."
        is_valid, reason = validate_text(short_text, min_words=50)
        self.assertFalse(is_valid)
        self.assertIn("too short", reason.lower())
        
        # Valid length
        long_text = " ".join(["word"] * 51)
        is_valid, reason = validate_text(long_text)
        self.assertTrue(is_valid)
        self.assertEqual(reason, "valid")

    def test_validate_text_language(self):
        """Test language detection."""
        # Non-English text (Spanish)
        spanish = "Este es un texto en español que no debería ser válido."
        is_valid, reason = validate_text(spanish)
        self.assertFalse(is_valid)
        self.assertIn("english", reason.lower())
        
        # English text
        english = "This is a valid English text " + " ".join(["word"] * 47)
        is_valid, reason = validate_text(english)
        self.assertTrue(is_valid)
        self.assertEqual(reason, "valid")

    def test_validate_text_empty(self):
        """Test empty text handling."""
        is_valid, reason = validate_text("")
        self.assertFalse(is_valid)
        self.assertIn("empty", reason.lower())

    def test_text_enrichment(self):
        """Test text enrichment functionality."""
        
        # Test various text types
        test_cases = [
            # Academic text with citations
            """According to Smith et al. (2023), climate change impacts are significant [1].
            The study (doi:10.1234/example) shows clear trends.""",
            
            # Positive sentiment
            "This breakthrough discovery is amazing and revolutionary!",
            
            # Negative sentiment
            "The results were disappointing and showed serious problems.",
            
            # Simple text
            "This is a basic test sentence."
        ]
        
        for text in test_cases:
            result = enrich_text(text)
            
            # Check all required fields
            self.assertIn("text", result)
            self.assertIn("readability", result)
            self.assertIn("sentiment", result)
            self.assertIn("citations", result)
            
            # Check types
            self.assertIsInstance(result["readability"], float)
            self.assertIsInstance(result["sentiment"], str)
            self.assertIsInstance(result["citations"], bool)
            
            # Check sentiment values
            self.assertIn(result["sentiment"], ["positive", "neutral", "negative"])
            
            print(f"\nText enrichment results for sentiment analysis:")
            for key, value in result.items():
                if key != "text":
                    print(f"{key}: {value}")

if __name__ == '__main__':
    unittest.main()
import pytest
from src.preprocessing import (
    clean_text, validate_text, normalize_text,
    clean_html, enrich_text, detect_citations
)

@pytest.fixture
def sample_html():
    return """
    <html>
        <nav>Navigation</nav>
        <div class="ad">Advertisement</div>
        <article>
            <h1>Test Article</h1>
            <p>According to Smith et al. (2023), this is a sample text [1].
            Further evidence (doi:10.1234/test) supports these findings.</p>
        </article>
        <footer>Copyright 2025</footer>
    </html>
    """

@pytest.fixture
def sample_texts():
    return {
        'valid': "This is a valid English text that is long enough to pass validation. " * 5,
        'short': "Too short.",
        'non_english': "Este texto está en español y no debería pasar la validación.",
        'with_citations': "Smith et al. (2023) found evidence [1]. See doi:10.1234/test",
        'messy': "This  &amp;  that\n\nHas   Multiple   Spaces &lt;tag&gt;"
    }

def test_clean_html(sample_html):
    cleaned = clean_html(sample_html)
    assert "Navigation" not in cleaned
    assert "Advertisement" not in cleaned
    assert "Test Article" in cleaned
    assert "Copyright" not in cleaned

def test_normalize_text(sample_texts):
    normalized = normalize_text(sample_texts['messy'])
    assert "  " not in normalized  # No double spaces
    assert "&amp;" not in normalized  # No HTML entities
    assert "this & that" in normalized.lower()
    assert "<tag>" not in normalized  # No HTML tags

def test_validate_text(sample_texts):
    # Test valid text
    is_valid, reason = validate_text(sample_texts['valid'])
    assert is_valid
    assert reason == "valid"
    
    # Test short text
    is_valid, reason = validate_text(sample_texts['short'])
    assert not is_valid
    assert "too short" in reason.lower()
    
    # Test non-English
    is_valid, reason = validate_text(sample_texts['non_english'])
    assert not is_valid
    assert "english" in reason.lower()

def test_detect_citations(sample_texts):
    has_citations = detect_citations(sample_texts['with_citations'])
    assert has_citations
    
    no_citations = detect_citations(sample_texts['valid'])
    assert not no_citations

def test_enrich_text(sample_texts):
    result = enrich_text(sample_texts['valid'])
    assert all(k in result for k in ['readability', 'sentiment', 'citations'])
    assert isinstance(result['readability'], float)
    assert result['sentiment'] in ['positive', 'neutral', 'negative']
    assert isinstance(result['citations'], bool)

def test_preprocessing_pipeline(sample_html, sample_texts):
    """Integration test for complete preprocessing pipeline."""
    # Step 1: Clean HTML
    cleaned = clean_html(sample_html)
    assert cleaned
    
    # Step 2: Normalize
    normalized = normalize_text(cleaned)
    assert normalized
    
    # Step 3: Validate
    is_valid, reason = validate_text(normalized)
    assert is_valid, f"Text validation failed: {reason}"
    
    # Step 4: Enrich
    enriched = enrich_text(normalized)
    assert enriched['text']
    assert 'readability' in enriched
    assert 'sentiment' in enriched
    assert 'citations' in enriched

def test_edge_cases():
    """Test edge cases and error handling."""
    # Empty input
    with pytest.raises(ValueError):
        clean_html("")
    
    # None input
    with pytest.raises(ValueError):
        normalize_text(None)
    
    # Invalid HTML
    result = clean_html("<>>>invalid<<<")
    assert result.strip()
