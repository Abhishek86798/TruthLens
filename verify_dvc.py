import subprocess
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_dvc():
    print("\n=== Verifying DVC Setup ===")
    
    try:
        # 1. Check DVC status
        print("\nChecking DVC status...")
        subprocess.run(["dvc", "status"], check=True)
        
        # 2. Create test data
        data_dir = Path("data/dataset")
        data_dir.mkdir(parents=True, exist_ok=True)
        test_file = data_dir / "test.txt"
        test_file.write_text("Test content")
        
        # 3. Track with DVC
        print("\nTracking test data...")
        subprocess.run(["dvc", "add", "data/dataset"], check=True)
        
        print("\n✓ DVC is working correctly!")
        print("\nNext steps:")
        print("1. Add your data files to data/dataset/")
        print("2. Run: dvc add data/dataset")
        print("3. Run: git add data/dataset.dvc")
        print("4. Run: git commit -m 'Add dataset'")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Verification failed: {e}")

if __name__ == "__main__":
    verify_dvc()
