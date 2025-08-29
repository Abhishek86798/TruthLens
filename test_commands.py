from src.data_collection import fetch_url, collect_from_urls
from src.preprocessing import clean_text, validate_content, check_data_quality
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_tests():
    print("\n=== TruthLens Test Commands ===")
    
    # Test 1: Data Collection
    print("\n1. Testing URL Fetching:")
    result = fetch_url("https://example.com")
    print(f"Status: {result['status']}")
    print(f"Error: {result['error']}")
    
    # Test 2: Text Cleaning
    print("\n2. Testing Text Cleaning:")
    html = "<html><body><h1>Test</h1><p>Sample content</p></body></html>"
    cleaned = clean_text(html)
    print(f"Cleaned text: {cleaned}")
    
    # Test 3: Content Validation
    print("\n3. Testing Content Validation:")
    is_valid, reasons = validate_content("This is a test text")
    print(f"Valid: {is_valid}")
    if not is_valid:
        print(f"Reasons: {reasons}")

if __name__ == "__main__":
    run_tests()
