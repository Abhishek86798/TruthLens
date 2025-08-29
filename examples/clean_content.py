from src.preprocessing import clean_html, validate_content
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def demo_content_cleaning():
    # Sample HTML with boilerplate
    sample_html = """
    <html>
        <nav>Menu items...</nav>
        <div class="ads">Advertisement here...</div>
        <article>
            <h1>Main Article Title</h1>
            <p>This is the actual content we want to keep.
            It contains meaningful information about the topic.</p>
        </article>
        <footer>Copyright notice...</footer>
    </html>
    """
    
    print("\n=== Content Cleaning Demo ===")
    print("\n1. Original HTML length:", len(sample_html))
    
    # Clean HTML
    cleaned = clean_html(sample_html)
    print("\n2. Cleaned content:")
    print("-" * 40)
    print(cleaned)
    
    # Validate content
    is_valid, reasons = validate_content(cleaned)
    print("\n3. Content validation:")
    print(f"Valid: {is_valid}")
    if not is_valid:
        print("Issues:", reasons)

if __name__ == "__main__":
    print("TruthLens Content Cleaning Demo")
    print("First, install required packages:")
    print("pip install trafilatura beautifulsoup4")
    print("\nThen run this demo:")
    demo_content_cleaning()
