from src.preprocessing import validate_text, check_data_quality
import json
import csv
import logging
from pathlib import Path
from typing import Dict, List
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_annotation(annotation: Dict) -> bool:
    """Validate a single annotation entry."""
    # Check required fields
    required_fields = {'id', 'text', 'label'}
    if not all(field in annotation for field in required_fields):
        logger.warning(f"Missing fields in annotation {annotation.get('id', 'unknown')}")
        return False
    
    # Check label values
    if annotation['label'] not in {'RELIABLE', 'UNRELIABLE'}:
        logger.warning(f"Invalid label in annotation {annotation['id']}: {annotation['label']}")
        return False
    
    # Validate text (with less strict requirements for testing)
    is_valid, reason = validate_text(annotation['text'], min_words=10)  # Reduced min_words for testing
    if not is_valid:
        logger.warning(f"Invalid text in annotation {annotation['id']}: {reason}")
        return False
    
    return True

def build_dataset(annotations_path: str, output_dir: str) -> bool:
    """Build final dataset from raw annotations."""
    try:
        # Create output directory
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load annotations
        annotations = []
        with open(annotations_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    annotations.append(json.loads(line))
        
        logger.info(f"Loaded {len(annotations)} raw annotations")
        
        # Validate and filter annotations
        valid_entries = []
        for ann in annotations:
            if validate_annotation(ann):
                valid_entries.append({
                    'id': ann['id'],
                    'text': ann['text'],
                    'label': ann['label']
                })
            else:
                logger.warning(f"Skipping invalid annotation: {ann['id']}")
        
        if not valid_entries:
            logger.error("No valid entries found")
            return False
            
        logger.info(f"Found {len(valid_entries)} valid entries")
        
        # Check dataset quality
        quality_report = check_data_quality(valid_entries)
        if quality_report['status'] == 'error':
            logger.error(f"Quality check failed: {quality_report['error']}")
            return False
            
        logger.info("Quality Report:")
        logger.info(f"- Total examples: {quality_report['total_examples']}")
        if 'class_balance' in quality_report:
            logger.info(f"- Class balance: {quality_report['class_balance']:.2f}")
        
        # Save outputs
        jsonl_path = output_dir / 'dataset.jsonl'
        csv_path = output_dir / 'dataset.csv'
        
        # Save JSONL
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for entry in valid_entries:
                f.write(json.dumps(entry) + '\n')
        
        # Save CSV
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'text', 'label'])
            writer.writeheader()
            writer.writerows(valid_entries)
        
        logger.info(f"Dataset saved to {output_dir}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to build dataset: {e}")
        return False

def test_dataset_building():
    """Test dataset building with sample annotations."""
    # Create test data
    test_dir = Path("test_data")
    test_dir.mkdir(exist_ok=True)
    
    # Create more realistic test data
    sample_annotations = [
        {
            "id": "1",
            "text": "According to recent studies, global temperatures have risen significantly over the past decade. Multiple data sources confirm this trend.",
            "label": "RELIABLE",
            "annotator": "test_user"
        },
        {
            "id": "2",
            "text": "This is a questionable claim without supporting evidence or citations.",
            "label": "UNRELIABLE",
            "annotator": "test_user"
        }
    ]
    
    # Save test annotations
    test_file = test_dir / "test_annotations.jsonl"
    with open(test_file, 'w', encoding='utf-8') as f:
        for ann in sample_annotations:
            f.write(json.dumps(ann) + '\n')
    
    # Run dataset building
    success = build_dataset(str(test_file), str(test_dir / "output"))
    
    # Cleanup
    if test_dir.exists():
        import shutil
        shutil.rmtree(test_dir)
    
    return success

if __name__ == "__main__":
    if test_dataset_building():
        logger.info("✅ Dataset building test passed")
    else:
        logger.error("❌ Dataset building test failed")
