import unittest
from unittest.mock import patch
import requests
import os
from langdetect import detect, DetectorFactory
from typing import Tuple, List
import json
from datetime import datetime
from typing import Dict, Any
from sklearn.datasets import make_classification
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np
import logging

# Set seed for consistent results
DetectorFactory.seed = 0

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_status(url: str) -> int:
    """Fetch HTTP status code for given URL"""
    response = requests.get(url)
    return response.status_code

def validate_content(text: str, min_words: int = 50, required_lang: str = 'en') -> Tuple[bool, List[str]]:
    """
    Validate content based on word count and language.
    Returns (is_valid, list_of_failure_reasons)
    """
    failures = []
    
    # Check word count
    word_count = len(text.split())
    if word_count < min_words:
        failures.append(f"Word count too low: {word_count} words (minimum {min_words})")
    
    # Check language
    try:
        detected_lang = detect(text)
        if detected_lang != required_lang:
            failures.append(f"Wrong language: detected '{detected_lang}' (required '{required_lang}')")
    except Exception as e:
        failures.append(f"Language detection failed: {str(e)}")
    
    return len(failures) == 0, failures

def create_versioned_dataset() -> Dict[str, Any]:
    """Create a sample dataset with version metadata."""
    dataset = {
        "metadata": {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "created_by": "TruthLens",
            "description": "Initial annotated dataset for fact-checking",
            "schema_version": "1.0",
            "stats": {
                "total_examples": 3,
                "label_distribution": {
                    "true": 1,
                    "partially_true": 1,
                    "false": 1
                }
            }
        },
        "data": [
            {
                "id": "v1_001",
                "text": "Global temperatures have risen significantly",
                "label": "true",
                "confidence": "high",
                "annotator": "expert_1",
                "version_added": "1.0.0"
            },
            {
                "id": "v1_002",
                "text": "Social media always harms mental health",
                "label": "partially_true",
                "confidence": "medium",
                "annotator": "expert_2",
                "version_added": "1.0.0"
            },
            {
                "id": "v1_003",
                "text": "5G causes health problems",
                "label": "false",
                "confidence": "high",
                "annotator": "expert_1",
                "version_added": "1.0.0"
            }
        ]
    }
    return dataset

def run_cross_validation():
    """Run k-fold cross-validation and report results."""
    # Generate sample data
    logger.info("Generating sample dataset...")
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_classes=2,
        n_informative=15,
        random_state=42
    )
    
    # Initialize model and cross-validation
    model = LogisticRegression(random_state=42)
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    # Store results
    fold_scores = []
    
    print("\n🔄 Cross-Validation Results")
    print("=" * 30)
    
    # Perform cross-validation
    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y), 1):
        # Split data
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]
        
        # Train and evaluate
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)
        score = accuracy_score(y_val, y_pred)
        fold_scores.append(score)
        
        # Print fold results
        print(f"\nFold {fold}:")
        print(f"Training samples: {len(X_train)}")
        print(f"Validation samples: {len(X_val)}")
        print(f"Accuracy: {score:.3f}")
    
    # Print summary statistics
    print("\n📊 Summary Statistics")
    print("-" * 20)
    print(f"Mean Accuracy: {np.mean(fold_scores):.3f}")
    print(f"Std Accuracy: {np.std(fold_scores):.3f}")
    print(f"Min Accuracy: {np.min(fold_scores):.3f}")
    print(f"Max Accuracy: {np.max(fold_scores):.3f}")

class TestFetchStatus(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_status_success(self, mock_get):
        # Configure mock
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Test
        result = fetch_status('https://example.com')
        
        # Assertions
        mock_get.assert_called_once_with('https://example.com')
        self.assertEqual(result, 200)

if __name__ == '__main__':
    try:
        unittest.main(argv=[''], exit=False)
    finally:
        print("\nCleaning up test file...")
        os.remove(__file__)

    try:
        dataset = create_versioned_dataset()
        version = dataset["metadata"]["version"]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create temporary filename with version
        filename = f"truthlens_dataset_v{version}_{timestamp}.json"
        
        # Simulate saving
        print(f"💾 Saving versioned dataset...")
        print(f"Version: {version}")
        print(f"Filename: {filename}")
        print(f"Total examples: {dataset['metadata']['stats']['total_examples']}")
        
        # In production, you would actually save the file:
        # with open(filename, 'w') as f:
        #     json.dump(dataset, f, indent=2)
        
        print("\n✅ Dataset versioning simulated successfully")
        
    finally:
        print("\nCleaning up test file...")
        os.remove(__file__)

    try:
        run_cross_validation()
    finally:
        print("\nCleaning up test file...")
        os.remove(__file__)
