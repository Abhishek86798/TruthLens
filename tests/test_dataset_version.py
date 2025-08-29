import pytest
from unittest.mock import patch, MagicMock
from src.dataset_version import DatasetVersioning
import tempfile
from pathlib import Path

@pytest.fixture
def mock_dvc():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="v1\nv2\n")
        yield mock_run

@pytest.fixture
def temp_dataset_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

def test_save_version(mock_dvc, temp_dataset_dir):
    versioning = DatasetVersioning(str(temp_dataset_dir))
    
    # Test saving version
    success = versioning.save_version("v1", "Initial version")
    assert success
    
    # Verify DVC commands were called
    calls = [call.args[0] for call in mock_dvc.call_args_list]
    assert ["dvc", "add", str(temp_dataset_dir)] in calls
    assert ["dvc", "tag", "add", "v1"] in calls

def test_list_versions(mock_dvc, temp_dataset_dir):
    versioning = DatasetVersioning(str(temp_dataset_dir))
    
    # Test listing versions
    versions = versioning.list_versions()
    assert len(versions) == 2
    assert any(v["tag"] == "v1" for v in versions)
    assert any(v["tag"] == "v2" for v in versions)
