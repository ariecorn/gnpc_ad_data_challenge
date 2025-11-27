"""
Configuration settings for GNPC Proteomics Analysis Application
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""

    # Project paths
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "mock_data"
    OUTPUT_DIR = BASE_DIR / "outputs"
    FIGURES_DIR = OUTPUT_DIR / "figures"
    RESULTS_DIR = OUTPUT_DIR / "results"

    # Data files
    PARTICIPANTS_FILE = "participants.csv"
    ASSESSMENTS_FILE = "clinical_assessments.csv"
    BIOSAMPLES_FILE = "biosamples.csv"
    MEASUREMENTS_FILE = "protein_measurements.csv"
    PROTEINS_FILE = "protein_annotations.csv"
    COHORTS_FILE = "cohort_metadata.csv"

    # Analysis parameters
    SIGNIFICANCE_LEVEL = 0.05
    RANDOM_STATE = 42

    # Visualization
    FIGURE_DPI = 300
    FIGURE_FORMAT = "png"

    # Optional: Database connection (for real GNPC data access)
    DATABASE_URL = os.getenv("DATABASE_URL", None)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "gnpc")
    DB_USER = os.getenv("DB_USER", "user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

    @classmethod
    def create_output_dirs(cls):
        """Create output directories if they don't exist."""
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        cls.FIGURES_DIR.mkdir(exist_ok=True)
        cls.RESULTS_DIR.mkdir(exist_ok=True)


# Create output directories on module import
Config.create_output_dirs()
