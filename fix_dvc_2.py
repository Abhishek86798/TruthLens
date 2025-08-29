import subprocess
import logging
from pathlib import Path
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_setup():
    """Clean and reinitialize DVC with proper Git configuration."""
    try:
        print("\n=== Cleaning and Reinitializing DVC ===")
        
        # 1. Remove existing DVC and Git files
        cleanup_paths = ['.dvc', '.git', 'data/dataset.dvc', '.gitignore']
        for path in cleanup_paths:
            if Path(path).exists():
                if Path(path).is_dir():
                    shutil.rmtree(path)
                else:
                    Path(path).unlink()
        print("✓ Cleaned existing files")
        
        # 2. Create data directory
        data_dir = Path("data/dataset")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # 3. Create proper .gitignore first
        gitignore_content = """
/data/dataset
*.pyc
__pycache__/
!.dvc
.dvc/cache
""".strip()
        
        with open(".gitignore", "w") as f:
            f.write(gitignore_content)
        print("✓ Created .gitignore")
        
        # 4. Initialize Git
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], check=True)
        print("✓ Initialized Git")
        
        # 5. Initial Git commit
        subprocess.run(["git", "add", ".gitignore"], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
        print("✓ Created initial commit")
        
        # 6. Now initialize DVC
        subprocess.run(["dvc", "init"], check=True)
        print("✓ Initialized DVC")
        
        # 7. Create sample data
        sample_file = data_dir / "sample.txt"
        sample_file.write_text("Test content")
        print("✓ Created sample data")
        
        # 8. Track with DVC
        subprocess.run(["dvc", "add", "data/dataset"], check=True)
        print("✓ Added dataset to DVC")
        
        # 9. Commit DVC files
        subprocess.run(["git", "add", ".dvc", "data/.gitignore", "data/dataset.dvc"], check=True)
        subprocess.run(["git", "commit", "-m", "Initialize DVC tracking"], check=True)
        print("✓ Committed DVC files")
        
        print("\nDVC setup completed successfully!")
        print("\nVerify with:")
        print("dvc status")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Setup failed: {e}")
        print(f"\n✗ Error: {e}")

if __name__ == "__main__":
    clean_setup()
