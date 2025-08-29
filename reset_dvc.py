import subprocess
import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_dvc():
    """Reset and reinitialize DVC setup."""
    try:
        print("\n=== Resetting DVC Setup ===")
        
        # Remove existing DVC files
        dvc_paths = ['.dvc', 'data/dataset.dvc']
        for path in dvc_paths:
            if Path(path).exists():
                print(f"\nRemoving {path}...")
                if Path(path).is_dir():
                    shutil.rmtree(path)
                else:
                    Path(path).unlink()
        
        # Initialize Git if needed
        if not Path(".git").exists():
            print("\nInitializing Git...")
            subprocess.run(["git", "init"], check=True)
        
        # Reinitialize DVC
        print("\nReinitializing DVC...")
        subprocess.run(["dvc", "init", "-f"], check=True)
        
        # Setup data directory
        data_dir = Path("data/dataset")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Track dataset with DVC
        print("\nTracking dataset with DVC...")
        subprocess.run(["dvc", "add", "data/dataset"], check=True)
        
        # Add to Git
        subprocess.run(["git", "add", ".dvc", ".dvcignore", "data/.gitignore", "data/dataset.dvc"], check=True)
        subprocess.run(["git", "commit", "-m", "Initialize DVC"], check=True)
        
        print("\n✓ DVC reset and initialized successfully!")
        print("\nYou can now:")
        print("1. Add files to data/dataset/")
        print("2. Run: dvc add data/dataset")
        print("3. Run: dvc push (if remote storage configured)")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Reset failed: {e}")
        print(f"\n✗ Reset failed: {e}")

if __name__ == "__main__":
    reset_dvc()
