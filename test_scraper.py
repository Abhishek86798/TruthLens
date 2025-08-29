import asyncio
import logging
import os
from src.data_collection import collect_from_urls

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def run_tests():
    """Run scraper tests"""
    # Test with example.com (reliable test site)
    urls = ["https://example.com"]
    
    print("\n=== TruthLens Scraper Test ===")
    print(f"Testing URLs: {urls}")
    print("=" * 40)
    
    try:
        logger.info("Starting URL fetch...")
        results = await collect_from_urls(urls, concurrency=1)
        
        print("\nResults:")
        print("-" * 40)
        for result in results:
            status = '✓' if result['status'] == 200 else '✗'
            print(f"\nURL: {result['url']}")
            print(f"Status: {status} ({result['status']})")
            if result['error']:
                print(f"Error: {result['error']}")
            else:
                print(f"Content: {len(result['html'])} bytes")
                print(f"Sample: {result['html'][:100]}...")
        
        print("\nTest Summary:")
        print("-" * 40)
        successes = sum(1 for r in results if r['status'] == 200)
        print(f"Total URLs: {len(urls)}")
        print(f"Successful: {successes}")
        print(f"Failed: {len(urls) - successes}")
                
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")

def main():
    """Entry point"""
    try:
        print("Starting scraper tests...")
        asyncio.run(run_tests())
    finally:
        # Clean up test file
        print("\nCleaning up test script...")
        os.remove(__file__)

if __name__ == "__main__":
    main()
