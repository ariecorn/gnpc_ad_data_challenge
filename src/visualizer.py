"""
Visualization utilities for GNPC proteomics data.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


class ProteomicsVisualizer:
    """Create visualizations for proteomics data."""

    def __init__(self, output_dir: Path = None):
        """
        Initialize visualizer.

        Args:
            output_dir: Directory to save figures
        """
        self.output_dir = output_dir
        sns.set_style("whitegrid")

    def plot_diagnosis_distribution(self, participants: pd.DataFrame, save: bool = False):
        """
        Plot distribution of diagnosis groups.

        Args:
            participants: Participant dataframe
            save: Whether to save the figure
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        diagnosis_counts = participants["diagnosis"].value_counts()
        diagnosis_counts.plot(kind="bar", ax=ax, color=["#2ecc71", "#f39c12", "#e74c3c"])

        ax.set_title("Diagnosis Distribution", fontsize=14, fontweight="bold")
        ax.set_xlabel("Diagnosis", fontsize=12)
        ax.set_ylabel("Count", fontsize=12)
        ax.tick_params(axis="x", rotation=45)

        plt.tight_layout()

        if save and self.output_dir:
            plt.savefig(self.output_dir / "diagnosis_distribution.png", dpi=300)

        plt.show()

    def plot_protein_by_diagnosis(self, data: pd.DataFrame, protein_name: str, save: bool = False):
        """
        Plot protein levels across diagnosis groups.

        Args:
            data: Merged dataframe with protein measurements
            protein_name: Name of protein to plot
            save: Whether to save the figure
        """
        protein_data = data[data["protein_name"] == protein_name]

        fig, ax = plt.subplots(figsize=(10, 6))

        sns.boxplot(
            data=protein_data, x="diagnosis", y="normalized_value", ax=ax, palette="Set2"
        )
        sns.swarmplot(
            data=protein_data, x="diagnosis", y="normalized_value", ax=ax, color="black", alpha=0.5, size=3
        )

        ax.set_title(f"{protein_name} Levels by Diagnosis", fontsize=14, fontweight="bold")
        ax.set_xlabel("Diagnosis", fontsize=12)
        ax.set_ylabel("Normalized Value", fontsize=12)

        plt.tight_layout()

        if save and self.output_dir:
            filename = f"{protein_name.replace(' ', '_').lower()}_by_diagnosis.png"
            plt.savefig(self.output_dir / filename, dpi=300)

        plt.show()

    def plot_correlation_heatmap(self, data: pd.DataFrame, proteins: list, save: bool = False):
        """
        Plot correlation heatmap between proteins.

        Args:
            data: Merged dataframe with protein measurements
            proteins: List of protein names to include
            save: Whether to save the figure
        """
        pivot_data = data[data["protein_name"].isin(proteins)].pivot_table(
            index="sample_id", columns="protein_name", values="normalized_value"
        )

        fig, ax = plt.subplots(figsize=(12, 10))

        sns.heatmap(
            pivot_data.corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax, square=True
        )

        ax.set_title("Protein Correlation Heatmap", fontsize=14, fontweight="bold")

        plt.tight_layout()

        if save and self.output_dir:
            plt.savefig(self.output_dir / "protein_correlation_heatmap.png", dpi=300)

        plt.show()
