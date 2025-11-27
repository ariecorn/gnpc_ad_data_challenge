"""
GNPC Alzheimer's Proteomics Data Analysis Application
Main entry point for the application.
"""

import sys
from pathlib import Path
from src.data_loader import DataLoader
from src.analyzer import ProteomicsAnalyzer
from config import Config


def main():
    """Main application entry point."""
    print("GNPC Alzheimer's Proteomics Analysis")
    print("=" * 50)

    # Initialize configuration
    config = Config()

    # Load data
    print("\nLoading data...")
    loader = DataLoader(config.DATA_DIR)
    data = loader.load_all_data()

    print(f"Loaded {len(data['participants'])} participants")
    print(f"Loaded {len(data['biosamples'])} biosamples")
    print(f"Loaded {len(data['protein_measurements'])} protein measurements")

    # Initialize analyzer
    analyzer = ProteomicsAnalyzer(data)

    # Example: Get summary statistics
    print("\nGenerating summary statistics...")
    summary = analyzer.get_summary_stats()
    print(summary)

    return 0


if __name__ == "__main__":
    sys.exit(main())
