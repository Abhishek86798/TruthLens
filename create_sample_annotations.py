import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sample_annotations():
    """Create sample annotations for testing."""
    # Sample data
    annotations = [
        {
            "id": "1",
            "text": "According to NASA's latest data, global temperatures have risen significantly over the past century. Multiple independent studies confirm this trend, showing an average increase of 1.1°C since pre-industrial times.",
            "label": "RELIABLE",
            "annotator": "user1"
        },
        {
            "id": "2",
            "text": "Scientists published in Nature journal demonstrate that renewable energy adoption has accelerated worldwide, with solar and wind power showing the fastest growth rates in the energy sector.",
            "label": "RELIABLE",
            "annotator": "user1"
        },
        {
            "id": "3",
            "text": "Some people say climate change isn't real because it's cold outside. This proves all scientists are wrong!",
            "label": "UNRELIABLE",
            "annotator": "user2"
        }
    ]
    
    # Create directories
    annotations_dir = Path("data/annotations")
    annotations_dir.mkdir(parents=True, exist_ok=True)
    
    # Save annotations
    output_path = annotations_dir / "raw_annotations.jsonl"
    with open(output_path, 'w', encoding='utf-8') as f:
        for ann in annotations:
            f.write(json.dumps(ann) + '\n')
    
    logger.info(f"Created {len(annotations)} sample annotations in {output_path}")

if __name__ == "__main__":
    create_sample_annotations()
    print("\nNow you can run: python build_actual_dataset.py")
