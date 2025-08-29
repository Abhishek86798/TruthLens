import subprocess
import shutil
from pathlib import Path
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_dvc():
    """Setup DVC with proper Git configuration."""
    try:
        print("\n=== Setting up DVC for TruthLens ===")
        
        # 1. Create directory structure
        data_dir = Path("data/dataset")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # 2. Clean up existing DVC files if any
        dvc_files = ['.dvc', 'data/dataset.dvc', '.dvcignore']
        for file in dvc_files:
            if Path(file).exists():
                if Path(file).is_dir():
                    shutil.rmtree(file)
                else:
                    Path(file).unlink()
        
        # 3. Initialize Git if needed
        if not Path(".git").exists():
            subprocess.run(["git", "init"], check=True)
        
        # 4. Create .gitignore
        with open(".gitignore", "w") as f:
            f.write("/data/dataset\n")
            f.write(".dvc/cache\n")
        
        # 5. Initialize DVC
        subprocess.run(["dvc", "init", "--force"], check=True)
        
        # 6. Configure DVC to not use Git for .dvc files
        subprocess.run(["dvc", "config", "core.autostage", "true"], check=True)
        
        # 7. Add dataset to DVC
        if any(data_dir.iterdir()):  # Only if directory has content
            subprocess.run(["dvc", "add", str(data_dir)], check=True)
        
        # 8. Commit DVC initialization
        subprocess.run(["git", "add", ".dvc", ".dvcignore", ".gitignore"], check=True)
        subprocess.run(["git", "commit", "-m", "Initialize DVC"], check=True)
        
        print("\n✓ DVC setup completed successfully!")
        print("\nNext steps:")
        print("1. Add files to data/dataset/")
        print("2. Run: python version_dataset.py")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Setup failed: {e}")
        print(f"\n✗ Error: {e}")

if __name__ == "__main__":
    setup_dvc()
