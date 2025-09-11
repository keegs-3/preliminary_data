"""
Centralized path configuration for WellPath Scoring System.

This module provides consistent path management across the entire project.
Update paths here to change directory structure without breaking scripts.
"""

import os
from pathlib import Path

# Base directories
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
CONFIG_DIR = PROJECT_ROOT / "config"
DOCS_DIR = PROJECT_ROOT / "docs"
TESTS_DIR = PROJECT_ROOT / "tests"

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
REFERENCE_DATA_DIR = SRC_DIR / "ref_csv_files_airtable"
GENERATED_CONFIGS_DIR = SRC_DIR / "generated_configs"

# Output directories (keeping current structure for now)
MARKERS_OUTPUT_DIR = PROJECT_ROOT / "WellPath_Score_Markers"
SURVEY_OUTPUT_DIR = PROJECT_ROOT / "WellPath_Score_Survey"
COMBINED_OUTPUT_DIR = PROJECT_ROOT / "WellPath_Score_Combined"
BREAKDOWN_OUTPUT_DIR = PROJECT_ROOT / "WellPath_Score_Breakdown"
IMPACT_SCORES_DIR = PROJECT_ROOT / "Recommendation_Impact_Scores"

# Algorithm and schema paths
ALGORITHMS_DIR = SRC_DIR / "algorithms"
SCHEMAS_DIR = SRC_DIR / "schemas"

# Input data files
UNITS_CSV = REFERENCE_DATA_DIR / "units_v3-Grid view.csv"
METRICS_CSV = REFERENCE_DATA_DIR / "metric_types_v3-Grid view.csv"
ADHERENCE_CSV = REFERENCE_DATA_DIR / "adherence_scoring_v2-Grid view (1).csv"

# Configuration files
RECOMMENDATIONS_JSON = PROJECT_ROOT / "recommendations_list.json"
ALL_CONFIGS_JSON = GENERATED_CONFIGS_DIR / "all_generated_configs.json"

# Utility functions
def ensure_dir_exists(path):
    """Ensure a directory exists, create if it doesn't."""
    Path(path).mkdir(parents=True, exist_ok=True)
    return path

def get_output_file_path(directory, filename):
    """Get a full path for an output file, ensuring the directory exists."""
    ensure_dir_exists(directory)
    return Path(directory) / filename

# Create essential directories on import
for directory in [MARKERS_OUTPUT_DIR, SURVEY_OUTPUT_DIR, COMBINED_OUTPUT_DIR, BREAKDOWN_OUTPUT_DIR]:
    ensure_dir_exists(directory)

# Environment-specific overrides
if "WELLPATH_DATA_DIR" in os.environ:
    DATA_DIR = Path(os.environ["WELLPATH_DATA_DIR"])
    
if "WELLPATH_OUTPUT_DIR" in os.environ:
    output_base = Path(os.environ["WELLPATH_OUTPUT_DIR"])
    MARKERS_OUTPUT_DIR = output_base / "markers"
    SURVEY_OUTPUT_DIR = output_base / "survey"
    COMBINED_OUTPUT_DIR = output_base / "combined"
    BREAKDOWN_OUTPUT_DIR = output_base / "breakdowns"