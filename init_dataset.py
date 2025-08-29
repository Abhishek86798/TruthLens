from src.dataset_version import DatasetVersioning
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_dataset():
    """Initialize dataset structure and versioning."""
    try:
        print("\n=== Initializing TruthLens Dataset ===")
        
        # Create dataset versioning
        dv = DatasetVersioning()
        
        # Create initial version if dataset exists
        data_path = "data/dataset"
        if os.path.exists(data_path) and os.listdir(data_path):
            print("\nSaving initial version...")
            dv.save_version("v0.1", "Initial dataset version")
            
            versions = dv.list_versions()
            print("\nAvailable versions:")
            for v in versions:
                print(f"- {v['tag']}: {v['message']}")
        else:
            print("\nNo data found. Create dataset in 'data/dataset' directory.")
            
        print("\n✓ Dataset versioning initialized!")
        print("\nTo save new versions:")
        print('dv = DatasetVersioning()')
        print('dv.save_version("v0.2", "Added new examples")')
        
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        print("\n✗ Error initializing dataset versioning")

if __name__ == "__main__":
    initialize_dataset()
