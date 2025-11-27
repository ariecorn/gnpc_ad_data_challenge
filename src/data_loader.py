"""
Data loading utilities for GNPC proteomics dataset.
"""

import pandas as pd
from pathlib import Path
from typing import Dict


class DataLoader:
    """Load and manage GNPC proteomics data."""

    def __init__(self, data_dir: Path):
        """
        Initialize DataLoader.

        Args:
            data_dir: Path to directory containing data files
        """
        self.data_dir = Path(data_dir)

    def load_participants(self) -> pd.DataFrame:
        """Load participant demographic data."""
        file_path = self.data_dir / "participants.csv"
        return pd.read_csv(file_path)

    def load_clinical_assessments(self) -> pd.DataFrame:
        """Load clinical assessments data."""
        file_path = self.data_dir / "clinical_assessments.csv"
        return pd.read_csv(file_path)

    def load_biosamples(self) -> pd.DataFrame:
        """Load biosample data."""
        file_path = self.data_dir / "biosamples.csv"
        return pd.read_csv(file_path)

    def load_protein_measurements(self) -> pd.DataFrame:
        """Load protein measurement data."""
        file_path = self.data_dir / "protein_measurements.csv"
        return pd.read_csv(file_path)

    def load_protein_annotations(self) -> pd.DataFrame:
        """Load protein annotation data."""
        file_path = self.data_dir / "protein_annotations.csv"
        return pd.read_csv(file_path)

    def load_cohort_metadata(self) -> pd.DataFrame:
        """Load cohort metadata."""
        file_path = self.data_dir / "cohort_metadata.csv"
        return pd.read_csv(file_path)

    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load all datasets.

        Returns:
            Dictionary containing all dataframes
        """
        return {
            "participants": self.load_participants(),
            "clinical_assessments": self.load_clinical_assessments(),
            "biosamples": self.load_biosamples(),
            "protein_measurements": self.load_protein_measurements(),
            "protein_annotations": self.load_protein_annotations(),
            "cohort_metadata": self.load_cohort_metadata(),
        }
