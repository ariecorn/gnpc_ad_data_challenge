"""
Analysis utilities for GNPC proteomics data.
"""

import pandas as pd
from typing import Dict


class ProteomicsAnalyzer:
    """Analyze GNPC proteomics data."""

    def __init__(self, data: Dict[str, pd.DataFrame]):
        """
        Initialize analyzer with loaded data.

        Args:
            data: Dictionary containing all dataframes
        """
        self.participants = data["participants"]
        self.assessments = data["clinical_assessments"]
        self.biosamples = data["biosamples"]
        self.measurements = data["protein_measurements"]
        self.proteins = data["protein_annotations"]
        self.cohorts = data["cohort_metadata"]

    def get_summary_stats(self) -> pd.DataFrame:
        """
        Generate summary statistics for the dataset.

        Returns:
            DataFrame with summary statistics
        """
        stats = {
            "Total Participants": len(self.participants),
            "Total Biosamples": len(self.biosamples),
            "Total Measurements": len(self.measurements),
            "Unique Proteins": self.measurements["protein_id"].nunique(),
            "Cohorts": len(self.cohorts),
        }

        # Diagnosis distribution
        diagnosis_counts = self.participants["diagnosis"].value_counts()
        for diagnosis, count in diagnosis_counts.items():
            stats[f"{diagnosis} Participants"] = count

        # Sample type distribution
        sample_counts = self.biosamples["sample_type"].value_counts()
        for sample_type, count in sample_counts.items():
            stats[f"{sample_type} Samples"] = count

        return pd.Series(stats)

    def merge_data(self) -> pd.DataFrame:
        """
        Merge all tables into a single analysis-ready dataframe.

        Returns:
            Merged dataframe
        """
        # Merge measurements with samples
        data = self.measurements.merge(self.biosamples, on="sample_id", how="left")

        # Merge with participants
        data = data.merge(self.participants, on="participant_id", how="left")

        # Merge with protein annotations
        # Use suffixes to handle overlapping columns, then drop duplicates
        data = data.merge(
            self.proteins,
            on="protein_id",
            how="left",
            suffixes=("", "_annotation")
        )

        # Drop annotation columns if the main columns exist
        cols_to_drop = [col for col in data.columns if col.endswith("_annotation")]
        if cols_to_drop:
            data = data.drop(columns=cols_to_drop)

        return data

    def filter_by_diagnosis(self, diagnosis: str) -> pd.DataFrame:
        """
        Filter merged data by diagnosis group.

        Args:
            diagnosis: Diagnosis to filter (e.g., 'Healthy Control', 'MCI', 'AD')

        Returns:
            Filtered dataframe
        """
        merged = self.merge_data()
        return merged[merged["diagnosis"] == diagnosis]

    def get_protein_by_diagnosis(self, protein_name: str) -> pd.DataFrame:
        """
        Get protein measurements grouped by diagnosis.

        Args:
            protein_name: Name of protein to analyze

        Returns:
            DataFrame with protein values by diagnosis
        """
        merged = self.merge_data()
        protein_data = merged[merged["protein_name"] == protein_name]

        summary = (
            protein_data.groupby("diagnosis")["normalized_value"]
            .agg(["mean", "std", "count"])
            .reset_index()
        )

        return summary
