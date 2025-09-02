from build_dataset import build_dataset
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Build actual dataset from annotations."""
    print("\n=== Building TruthLens Dataset ===")
    
    # Set paths
    annotations_path = "data/annotations/raw_annotations.jsonl"
    output_dir = "data/processed"
    
    # Ensure directories exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Build dataset
    success = build_dataset(annotations_path, output_dir)
    
    if success:
        print("\n✅ Dataset built successfully!")
        print(f"Output files:")
        print(f"- {output_dir}/dataset.jsonl")
        print(f"- {output_dir}/dataset.csv")
    else:
        print("\n❌ Dataset building failed")

if __name__ == "__main__":
    main()
