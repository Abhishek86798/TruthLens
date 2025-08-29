from datetime import datetime
import json
from typing import Dict, List, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class AnnotationManager:
    def __init__(self, output_file: str = "annotations.jsonl"):
        self.output_file = output_file
        self.ensure_file_exists()
    
    def ensure_file_exists(self):
        """Create annotation file if it doesn't exist."""
        if not Path(self.output_file).exists():
            Path(self.output_file).touch()
    
    def save_annotation(self, annotation: Dict) -> bool:
        """Save single annotation to JSONL file."""
        try:
            annotation["timestamp"] = datetime.now().isoformat()
            with open(self.output_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(annotation) + "\n")
            return True
        except Exception as e:
            logger.error(f"Failed to save annotation: {e}")
            return False
    
    def get_annotations(self) -> List[Dict]:
        """Read all annotations from file."""
        annotations = []
        try:
            with open(self.output_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        annotations.append(json.loads(line))
            return annotations
        except Exception as e:
            logger.error(f"Failed to read annotations: {e}")
            return []
