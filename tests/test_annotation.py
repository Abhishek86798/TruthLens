import pytest
from src.annotation import AnnotationManager
import json
import os
from datetime import datetime

@pytest.fixture
def temp_annotation_file(tmp_path):
    return str(tmp_path / "test_annotations.jsonl")

def test_annotation_saving(temp_annotation_file):
    manager = AnnotationManager(temp_annotation_file)
    
    # Test annotation
    annotation = {
        "id": "test-123",
        "text": "Sample document",
        "label": "Reliable",
        "annotator": "test_user"
    }
    
    # Save annotation
    assert manager.save_annotation(annotation)
    
    # Verify saved data
    annotations = manager.get_annotations()
    assert len(annotations) == 1
    assert annotations[0]["id"] == "test-123"
    assert annotations[0]["label"] == "Reliable"
    assert "timestamp" in annotations[0]

def test_multiple_annotations(temp_annotation_file):
    manager = AnnotationManager(temp_annotation_file)
    
    # Save multiple annotations
    for i in range(3):
        annotation = {
            "id": f"test-{i}",
            "text": f"Document {i}",
            "label": "Reliable",
            "annotator": "test_user"
        }
        manager.save_annotation(annotation)
    
    # Verify all annotations saved
    annotations = manager.get_annotations()
    assert len(annotations) == 3
