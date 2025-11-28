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

    # Part 2: Drug Discovery paths
    STRUCTURES_DIR = BASE_DIR / "structures"
    PROTEINS_DIR = STRUCTURES_DIR / "proteins"
    LIGANDS_DIR = STRUCTURES_DIR / "ligands"
    DOCKING_DIR = BASE_DIR / "docking_results"
    CACHE_DIR = BASE_DIR / "cache"

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

    # Part 1: Statistical Analysis parameters
    PROGRESSOR_PERCENTILE = 50.0  # Median split for fast/slow progressors
    MIN_VISITS_LONGITUDINAL = 2   # Minimum visits for longitudinal analysis
    MIN_EFFECT_SIZE = 0.5         # Minimum Cohen's d for clinical relevance

    # Target prioritization scoring weights
    SCORING_WEIGHTS = {
        'early_upregulation': 0.25,
        'disease_correlation': 0.20,
        'trajectory_steepness': 0.20,
        'hazard_ratio': 0.20,
        'statistical_significance': 0.15
    }

    # Visualization
    FIGURE_DPI = 300
    FIGURE_FORMAT = "png"

    # Part 2: Drug Discovery parameters
    VINA_EXHAUSTIVENESS = 8
    VINA_N_POSES = 9
    DOCKING_BOX_SIZE = (20, 20, 20)  # Angstroms (x, y, z)
    DOCKING_AFFINITY_CUTOFF = -7.0   # kcal/mol
    BBB_REQUIRED = True
    MAX_MW = 500                     # Daltons (Lipinski Rule of 5)
    MAX_LOGP = 5
    MAX_TPSA = 90                    # Ų (for BBB permeability)

    # Optional: Database connection (for real GNPC data access)
    DATABASE_URL = os.getenv("DATABASE_URL", None)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "gnpc")
    DB_USER = os.getenv("DB_USER", "user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

    # API keys (from .env)
    CHEMBL_API_KEY = os.getenv("CHEMBL_API_KEY", None)
    PUBCHEM_API_KEY = os.getenv("PUBCHEM_API_KEY", None)

    @classmethod
    def create_output_dirs(cls):
        """Create output directories if they don't exist."""
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        cls.FIGURES_DIR.mkdir(exist_ok=True)
        cls.RESULTS_DIR.mkdir(exist_ok=True)
        cls.STRUCTURES_DIR.mkdir(exist_ok=True)
        cls.PROTEINS_DIR.mkdir(exist_ok=True)
        cls.LIGANDS_DIR.mkdir(exist_ok=True)
        cls.DOCKING_DIR.mkdir(exist_ok=True)
        cls.CACHE_DIR.mkdir(exist_ok=True)


# Create output directories on module import
Config.create_output_dirs()
