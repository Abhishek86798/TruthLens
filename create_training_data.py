import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_training_data():
    """Create sample training dataset with sufficient examples per class."""
    
    # Sample training data
    training_data = [
        # Reliable examples
        {
            "id": "r1",
            "text": "According to NASA's latest data from 2023, global temperatures have risen by 1.1°C since pre-industrial times. Multiple satellite measurements confirm this trend.",
            "label": "RELIABLE"
        },
        {
            "id": "r2",
            "text": "A peer-reviewed study in Nature shows that renewable energy costs have decreased by 80% over the past decade, based on market data from 60 countries.",
            "label": "RELIABLE"
        },
        {
            "id": "r3",
            "text": "Research published in Science demonstrates that ocean acidification has increased by 30% since the industrial revolution, supported by pH measurements from 500 monitoring stations.",
            "label": "RELIABLE"
        },
        
        # Unreliable examples
        {
            "id": "u1",
            "text": "Random blogger claims climate change is a hoax without providing any evidence. The post ignores decades of scientific research and makes unfounded accusations.",
            "label": "UNRELIABLE"
        },
        {
            "id": "u2",
            "text": "Social media post spreads conspiracy theory about weather control without any scientific basis or credible sources to support wild claims.",
            "label": "UNRELIABLE"
        },
        {
            "id": "u3",
            "text": "Website makes extreme predictions about immediate climate collapse, contradicting peer-reviewed research and using sensationalized language without data.",
            "label": "UNRELIABLE"
        }
    ]
    
    # Create output directory
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save dataset
    output_file = output_dir / "dataset.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in training_data:
            f.write(json.dumps(item) + '\n')
    
    logger.info(f"Created training dataset with {len(training_data)} examples")
    logger.info(f"Saved to: {output_file}")
    logger.info("You can now run: python models/baseline.py")

if __name__ == "__main__":
    create_training_data()
