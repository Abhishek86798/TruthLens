from src.preprocessing import check_data_quality
import json

# Test dataset
test_data = [
    {
        "text": "Sample factual claim with evidence",
        "label": "FACTUAL",
        "sources": ["NASA", "IPCC"]
    },
    {
        "text": "Another claim for testing",
        "label": "QUESTIONABLE",
        "sources": ["Blog"]
    }
]

# Run quality check
result = check_data_quality(test_data)

# Print results in readable format
print("\nData Quality Report:")
print("-" * 20)
print(f"Total examples: {result['total_examples']}")
print(f"Quality score: {result['quality_score']}")
print("\nLabel distribution:")
for label, freq in result['label_distribution'].items():
    print(f"- {label}: {freq:.1%}")
