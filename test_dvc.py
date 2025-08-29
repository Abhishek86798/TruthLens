import subprocess
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_dvc_setup():
    """Test DVC initialization and basic functionality."""
    try:
        print("\n=== Testing DVC Setup ===")
        
        # 1. Create test data directory
        data_dir = Path("data/dataset")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # 2. Create sample file
        sample_file = data_dir / "sample.txt"
        sample_file.write_text("Test content")
        
        # 3. Initialize Git if needed
        if not Path(".git").exists():
            subprocess.run(["git", "init"], check=True)
            print("✓ Git initialized")
        
        # 4. Initialize DVC
        subprocess.run(["dvc", "init", "--force"], check=True)
        print("✓ DVC initialized")
        
        # 5. Track dataset
        subprocess.run(["dvc", "add", "data/dataset"], check=True)
        print("✓ Dataset tracked")
        
        # 6. Commit DVC files
        subprocess.run(["git", "add", ".dvc", ".dvcignore", "data/.gitignore", "data/dataset.dvc"], check=True)
        subprocess.run(["git", "commit", "-m", "Initialize DVC tracking"], check=True)
        print("✓ DVC files committed")
        
        print("\nDVC setup successful!")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"DVC setup failed: {e}")
        print(f"\n✗ Error: {e}")

if __name__ == "__main__":
    test_dvc_setup()
