"""
Tests for data_loader module.
"""

import pytest
from pathlib import Path
from src.data_loader import DataLoader


def test_data_loader_initialization():
    """Test DataLoader initialization."""
    loader = DataLoader(Path("mock_data"))
    assert loader.data_dir == Path("mock_data")


def test_load_all_data():
    """Test loading all data files."""
    loader = DataLoader(Path("mock_data"))
    data = loader.load_all_data()

    assert "participants" in data
    assert "clinical_assessments" in data
    assert "biosamples" in data
    assert "protein_measurements" in data
    assert "protein_annotations" in data
    assert "cohort_metadata" in data

    assert len(data["participants"]) > 0
    assert len(data["protein_measurements"]) > 0
