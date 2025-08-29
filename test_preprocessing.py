from src.preprocessing import (
    clean_text, validate_text, normalize_text, 
    clean_html, check_data_quality
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_all_preprocessing():
    print("\n=== TruthLens Preprocessing Tests ===")
    
    # 1. Test HTML Cleaning
    print("\n1. HTML Cleaning:")
    print("-" * 40)
    sample_html = """
    <html><body>
        <nav>Menu...</nav>
        <div class="ad">Advertisement</div>
        <article>
            <h1>Main Content</h1>
            <p>This is the actual content we want to extract and analyze.</p>
        </article>
        <footer>Copyright 2025</footer>
    </body></html>
    """
    cleaned = clean_html(sample_html)
    print(f"Cleaned content:\n{cleaned}\n")
    
    # 2. Test Text Normalization
    print("\n2. Text Normalization:")
    print("-" * 40)
    messy_text = "This &amp; that\n\nHas   Multiple   Spaces &lt;tag&gt;"
    normalized = normalize_text(messy_text)
    print(f"Original: {messy_text}")
    print(f"Normalized: {normalized}")
    
    # 3. Test Content Validation
    print("\n3. Content Validation:")
    print("-" * 40)
    texts = [
        "Short text.",
        "Este es un texto en español.",
        "This is a longer English text that should pass validation because it contains more than fifty words. " * 3
    ]
    
    for text in texts:
        print(f"\nInput: {text[:50]}...")
        is_valid, reason = validate_text(text)
        print(f"✓ Valid" if is_valid else f"✗ Invalid")
        print(f"Reason: {reason}")
    
    # 4. Test Quality Checks
    print("\n4. Quality Metrics:")
    print("-" * 40)
    dataset = [
        {"text": "Sample 1", "label": "FACTUAL", "sources": ["source1"]},
        {"text": "Sample 2", "label": "QUESTIONABLE", "sources": ["source2"]},
        {"text": "Sample 3", "label": "FACTUAL", "sources": []}
    ]
    
    quality_report = check_data_quality(dataset)
    print("\nDataset Quality:")
    for key, value in quality_report.items():
        if isinstance(value, float):
            print(f"• {key}: {value:.2f}")
        else:
            print(f"• {key}: {value}")

if __name__ == "__main__":
    test_all_preprocessing()
