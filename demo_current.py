from src.data_collection import fetch_url, collect_from_urls
from src.preprocessing import clean_text, validate_content, check_data_quality
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_demo():
    print("🔍 TruthLens Current Functionality Demo")
    print("=" * 50)
    
    # Test data collection
    print("\n1. Testing Data Collection")
    print("-" * 30)
    urls = ["https://example.com", "https://httpbin.org/html"]
    results = collect_from_urls(urls)
    
    for result in results:
        print(f"\nURL: {result['url']}")
        print(f"Status: {result['status']}")
        if result['error']:
            print(f"Error: {result['error']}")
            
    # Test preprocessing
    print("\n2. Testing Preprocessing")
    print("-" * 30)
    sample_html = """
    <article>
        <h1>Climate Change Impact</h1>
        <p>Global temperatures have risen significantly in the past century.
        Scientists have observed multiple indicators of climate change.
        These changes are affecting ecosystems worldwide.</p>
        <p>Multiple studies confirm human activity's role in global warming.
        The evidence comes from various sources including satellite data.</p>
    </article>
    """
    
    cleaned_text = clean_text(sample_html)
    print("\nCleaned text preview:")
    print(cleaned_text[:100] + "...")
    
    is_valid, reasons = validate_content(cleaned_text)
    print(f"\nContent validation: {'✓' if is_valid else '✗'}")
    if not is_valid:
        print("Validation issues:", reasons)
    
    # Test quality checks
    print("\n3. Testing Quality Checks")
    print("-" * 30)
    sample_dataset = [
        {"text": "Sample 1", "label": "true", "sources": ["source1"]},
        {"text": "Sample 2", "label": "false", "sources": ["source2"]},
        {"text": "Sample 3", "label": "true", "sources": []}
    ]
    
    quality_report = check_data_quality(sample_dataset)
    print("\nQuality Report:")
    for key, value in quality_report.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    run_demo()
