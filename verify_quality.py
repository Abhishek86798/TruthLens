from src.preprocessing import check_data_quality
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_quality_checks():
    print("\n=== Data Quality Verification ===")
    
    # 1. Good Dataset (Should show "ok" status)
    print("\n1. Testing Good Dataset:")
    print("-" * 50)
    good_dataset = [
        {
            "id": "1",
            "text": "Sample text one",
            "label": "RELIABLE",
            "annotator": "user1"
        },
        {
            "id": "2",
            "text": "Sample text two",
            "label": "UNRELIABLE",
            "annotator": "user2"
        }
    ]
    
    result = check_data_quality(good_dataset)
    print(f"Status: {result['status']}")
    print(f"Issues found: {result['issues']}")
    
    # 2. Bad Dataset (Should show "issues" status)
    print("\n2. Testing Problematic Dataset:")
    print("-" * 50)
    bad_dataset = [
        {
            "id": "1",
            "text": "First text"  # Missing label and annotator
        },
        {
            "id": "1",  # Duplicate ID!
            "text": "Second text",
            "label": "RELIABLE"  # Missing annotator
        }
    ]
    
    result = check_data_quality(bad_dataset)
    print(f"Status: {result['status']}")
    print(f"Missing Fields: {result['issues']['missing_fields']}")
    print(f"Duplicate IDs: {result['issues']['duplicate_ids']}")
    
    print("\nExplanation:")
    print("- Status 'ok' means no issues found")
    print("- Status 'issues' means problems detected")
    print("- Missing fields and duplicate IDs should be fixed")

if __name__ == "__main__":
    verify_quality_checks()
