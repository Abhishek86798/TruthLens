from src.data_collection import fetch_url, collect_from_urls
from src.preprocessing import clean_text, validate_content
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_claim(claim_text: str, evidence_urls: list[str]) -> dict:
    """
    Demo function to check a claim using current capabilities
    """
    logger.info(f"Checking claim: {claim_text}")
    
    # Step 1: Collect evidence
    logger.info("Collecting evidence from URLs...")
    evidence_data = collect_from_urls(evidence_urls)
    
    # Step 2: Process evidence
    processed_evidence = []
    for data in evidence_data:
        if data['html']:
            clean_content = clean_text(data['html'])
            is_valid, reasons = validate_content(clean_content)
            processed_evidence.append({
                'url': data['url'],
                'content': clean_content[:200] + "...",  # Preview
                'is_valid': is_valid,
                'validation_issues': reasons
            })
    
    return {
        'claim': claim_text,
        'evidence_count': len(processed_evidence),
        'valid_evidence': sum(1 for e in processed_evidence if e['is_valid']),
        'evidence_details': processed_evidence
    }

if __name__ == "__main__":
    # Example usage
    test_claim = "Global temperatures have risen significantly in the past century"
    test_urls = [
        "https://climate.nasa.gov/evidence/",
        "https://www.noaa.gov/climate"
    ]
    
    print("\n🔍 TruthLens Demo")
    print("=" * 50)
    print("\nThis demo shows current capabilities (Phase 1-2):")
    print("- URL fetching")
    print("- Content extraction")
    print("- Text validation")
    print("\nNote: Fact verification not yet implemented")
    
    result = check_claim(test_claim, test_urls)
    
    print("\nResults:")
    print("-" * 20)
    print(f"Claim: {result['claim']}")
    print(f"Evidence sources checked: {result['evidence_count']}")
    print(f"Valid evidence pieces: {result['valid_evidence']}")
    
    print("\nEvidence Details:")
    for i, evidence in enumerate(result['evidence_details'], 1):
        print(f"\n{i}. {evidence['url']}")
        print(f"Valid: {'✓' if evidence['is_valid'] else '✗'}")
        if not evidence['is_valid']:
            print("Issues:", ', '.join(evidence['validation_issues']))
        print("Preview:", evidence['content'])
