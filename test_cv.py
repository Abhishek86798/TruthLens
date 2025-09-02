import os
import json
import logging
from models import baseline

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_cross_validation():
    """Run cross-validation test with balanced dataset."""
    # Create test dataset
    test_file = "test_data.jsonl"
    test_data = [
        {"text": "According to NASA's latest research published in Nature, global temperatures have risen significantly over the past decade, supported by satellite data and ground measurements.", "label": "RELIABLE"},
        {"text": "Multiple independent studies from leading climate scientists confirm the acceleration of ice melt in polar regions, as documented in peer-reviewed journals.", "label": "RELIABLE"},
        {"text": "Recent geological surveys published by USGS demonstrate clear evidence of changing weather patterns supported by long-term data collection.", "label": "RELIABLE"},
        {"text": "SHOCKING: Secret government agents controlling weather with hidden machines! No evidence provided but trust us!", "label": "UNRELIABLE"},
        {"text": "Anonymous source claims all climate scientists are lying, provides no data or verification of credentials.", "label": "UNRELIABLE"},
        {"text": "Blog post alleges global conspiracy without citing any scientific studies or providing verifiable evidence.", "label": "UNRELIABLE"}
    ]
    
    with open(test_file, "w", encoding="utf-8") as f:
        for item in test_data:
            f.write(json.dumps(item) + "\n")

    try:
        classifier = baseline.BaselineClassifier()
        metrics = classifier.train_and_evaluate(test_file, "models")
        logger.info(f"Test completed. Metrics: {metrics}")
    except Exception as e:
        logger.error(f"Training failed: {e}")
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)
            logger.info(f"Cleaned up test file: {test_file}")

if __name__ == "__main__":
    test_cross_validation()
