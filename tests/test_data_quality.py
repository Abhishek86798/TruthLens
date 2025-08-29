import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.preprocessing import check_data_quality, check_label_balance

class TestDataQuality(unittest.TestCase):
    def setUp(self):
        self.sample_dataset = [
            {
                "id": "001",
                "text": "Test claim 1",
                "label": "true",
                "confidence": "high",
                "sources": ["Source1", "Source2"]
            },
            {
                "id": "002",
                "text": "Test claim 2",
                "label": "false",
                "confidence": "medium",
                "sources": ["Source1"]
            }
        ]

    def test_quality_checks(self):
        report = check_data_quality(self.sample_dataset)
        self.assertIn('quality_score', report)
        self.assertGreaterEqual(report['quality_score'], 0)
        self.assertLessEqual(report['quality_score'], 100)

    def test_label_balance(self):
        distribution = check_label_balance(self.sample_dataset)
        self.assertEqual(sum(distribution.values()), 1.0)

    def test_balanced_dataset(self):
        """Test quality check with well-formed dataset."""
        dataset = [
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
                "annotator": "user1"
            }
        ]
        
        result = check_data_quality(dataset)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["total_examples"], 2)
        self.assertEqual(result["class_balance"], 1.0)
        self.assertFalse(result["issues"]["missing_fields"])
        self.assertFalse(result["issues"]["duplicate_ids"])

    def test_missing_fields(self):
        """Test quality check with missing fields."""
        dataset = [
            {
                "id": "1",
                "text": "Sample text"
                # Missing label and annotator
            }
        ]
        
        result = check_data_quality(dataset)
        self.assertEqual(result["status"], "issues")
        self.assertIn("label", result["issues"]["missing_fields"])
        self.assertIn("annotator", result["issues"]["missing_fields"])

    def test_duplicate_ids(self):
        """Test quality check with duplicate IDs."""
        dataset = [
            {
                "id": "1",
                "text": "First text",
                "label": "RELIABLE",
                "annotator": "user1"
            },
            {
                "id": "1",  # Duplicate ID
                "text": "Second text",
                "label": "UNRELIABLE",
                "annotator": "user1"
            }
        ]
        
        result = check_data_quality(dataset)
        self.assertEqual(result["status"], "issues")
        self.assertIn("1", result["issues"]["duplicate_ids"])

    def test_empty_dataset(self):
        """Test quality check with empty dataset."""
        result = check_data_quality([])
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["total_examples"], 0)

if __name__ == '__main__':
    unittest.main()
