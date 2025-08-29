import subprocess
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_dvc_setup():
    """Fix DVC and Git configuration."""
    try:
        print("\n=== Fixing DVC Setup ===")
        
        # 1. Create data directory
        data_dir = Path("data/dataset")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # 2. Create proper .gitignore
        root_gitignore = Path(".gitignore")
        root_gitignore.write_text("""
/data/dataset
*.dvc
.dvc/cache
        """.strip())
        print("✓ Created root .gitignore")
        
        # 3. Initialize Git if needed
        if not Path(".git").exists():
            subprocess.run(["git", "init"], check=True)
            print("✓ Initialized Git")
        
        # 4. Configure Git
        subprocess.run(["git", "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], check=True)
        print("✓ Configured Git")
        
        # 5. Initialize DVC
        subprocess.run(["dvc", "init", "--force"], check=True)
        print("✓ Initialized DVC")
        
        # 6. Create test file
        test_file = data_dir / "test.txt"
        test_file.write_text("Test content")
        print("✓ Created test file")
        
        # 7. Add and commit Git files
        subprocess.run(["git", "add", ".gitignore", ".dvc"], check=True)
        subprocess.run(["git", "commit", "-m", "Initialize DVC"], check=True)
        print("✓ Committed DVC files")
        
        # 8. Track data with DVC
        subprocess.run(["dvc", "add", "data/dataset"], check=True)
        print("✓ Added dataset to DVC")
        
        # 9. Add DVC file to Git
        subprocess.run(["git", "add", "data/dataset.dvc"], check=True)
        subprocess.run(["git", "commit", "-m", "Add dataset tracking"], check=True)
        print("✓ Committed dataset tracking")
        
        print("\nDVC setup fixed successfully!")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Setup failed: {e}")
        print(f"\n✗ Error: {e}")

if __name__ == "__main__":
    fix_dvc_setup()
