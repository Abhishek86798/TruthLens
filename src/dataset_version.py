import subprocess
import logging
from typing import List, Dict
from pathlib import Path
import json

logger = logging.getLogger(__name__)

class DatasetVersioning:
    def __init__(self, dataset_path: str = "data/dataset"):
        self.dataset_path = Path(dataset_path)
        self._init_dvc()
    
    def _init_dvc(self):
        """Initialize DVC tracking for dataset folder."""
        try:
            if not self.dataset_path.exists():
                self.dataset_path.mkdir(parents=True)
            
            # Initialize DVC tracking if not already tracked
            subprocess.run(["dvc", "add", str(self.dataset_path)], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to initialize DVC: {e}")
            raise
    
    def save_version(self, tag: str, message: str = "") -> bool:
        """Save current dataset state with a version tag."""
        try:
            # Add changes to DVC
            subprocess.run(["dvc", "add", str(self.dataset_path)], check=True)
            
            # Commit changes
            subprocess.run(["dvc", "commit"], check=True)
            
            # Add version tag
            subprocess.run(["dvc", "tag", "add", tag, "-d", str(self.dataset_path)], check=True)
            
            # Save metadata
            self._save_version_metadata(tag, message)
            
            logger.info(f"Saved dataset version: {tag}")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to save version {tag}: {e}")
            return False
    
    def list_versions(self) -> List[Dict]:
        """List all saved dataset versions."""
        try:
            result = subprocess.run(
                ["dvc", "tag", "list"], 
                capture_output=True, 
                text=True,
                check=True
            )
            
            versions = []
            for line in result.stdout.splitlines():
                if line.strip():
                    tag = line.strip()
                    metadata = self._load_version_metadata(tag)
                    versions.append({
                        "tag": tag,
                        "timestamp": metadata.get("timestamp"),
                        "message": metadata.get("message", "")
                    })
            
            return versions
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to list versions: {e}")
            return []
    
    def _save_version_metadata(self, tag: str, message: str):
        """Save version metadata to JSON."""
        metadata = {
            "tag": tag,
            "timestamp": datetime.now().isoformat(),
            "message": message
        }
        
        metadata_file = self.dataset_path / ".metadata.json"
        existing = self._load_all_metadata()
        existing[tag] = metadata
        
        with open(metadata_file, "w") as f:
            json.dump(existing, f, indent=2)
    
    def _load_version_metadata(self, tag: str) -> Dict:
        """Load metadata for specific version."""
        all_metadata = self._load_all_metadata()
        return all_metadata.get(tag, {})
    
    def _load_all_metadata(self) -> Dict:
        """Load all version metadata."""
        metadata_file = self.dataset_path / ".metadata.json"
        if metadata_file.exists():
            with open(metadata_file) as f:
                return json.load(f)
        return {}
