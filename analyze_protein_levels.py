"""
Analyze mean protein levels by diagnosis group.
"""

from src.data_loader import DataLoader
from src.analyzer import ProteomicsAnalyzer
from config import Config
import pandas as pd


def main():
    """Analyze mean protein levels by diagnosis."""
    print("Mean Protein Levels by Diagnosis Group")
    print("=" * 70)

    # Load data
    config = Config()
    loader = DataLoader(config.DATA_DIR)
    data = loader.load_all_data()

    # Initialize analyzer
    analyzer = ProteomicsAnalyzer(data)

    # Merge all data
    merged_data = analyzer.merge_data()

    # Get unique proteins
    unique_proteins = sorted(merged_data['protein_name'].unique())
    print(f"\nTotal unique proteins: {len(unique_proteins)}\n")

    # Calculate mean protein levels for each unique protein by diagnosis
    print("Mean Protein Levels by Diagnosis Group (for each unique protein)")
    print("=" * 90)

    for protein in unique_proteins:
        print(f"\n{protein}:")
        print("-" * 90)

        protein_data = merged_data[merged_data['protein_name'] == protein]

        # Calculate mean for each diagnosis group
        stats = protein_data.groupby('diagnosis')['normalized_value'].agg([
            ('Mean', 'mean'),
            ('Std Dev', 'std'),
            ('Count', 'count'),
            ('Min', 'min'),
            ('Max', 'max')
        ]).round(4)

        print(stats.to_string())

    # Summary table with all proteins
    print("\n" + "=" * 90)
    print("SUMMARY TABLE: Mean Protein Levels by Diagnosis")
    print("=" * 90)

    pivot_mean = merged_data.pivot_table(
        index='protein_name',
        columns='diagnosis',
        values='normalized_value',
        aggfunc='mean'
    ).round(4)

    # Reorder columns if they exist
    column_order = ['Healthy Control', 'MCI', 'AD']
    existing_columns = [col for col in column_order if col in pivot_mean.columns]
    pivot_mean = pivot_mean[existing_columns]

    print(pivot_mean.to_string())
    print("\n")


if __name__ == "__main__":
    main()
