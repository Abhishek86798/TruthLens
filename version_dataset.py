from src.dataset_version import DatasetVersioning
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    print("\n=== TruthLens Dataset Versioning ===")
    
    # Initialize versioning
    dv = DatasetVersioning()
    
    # Save new version
    version_tag = f"v{datetime.now().strftime('%Y%m%d')}"
    message = input("\nEnter version message (e.g., 'Added 100 new examples'): ")
    
    if dv.save_version(version_tag, message):
        print(f"\n✓ Saved version: {version_tag}")
    
    # Show all versions
    print("\nAll versions:")
    for version in dv.list_versions():
        print(f"- {version['tag']}: {version['message']}")

if __name__ == "__main__":
    main()
