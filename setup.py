#!/usr/bin/env python3
"""Setup script for WellPath Scoring System."""

from setuptools import setup, find_packages
import os

# Read requirements.txt
def read_requirements():
    """Read requirements from requirements.txt."""
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

# Read README for long description
def read_readme():
    """Read README.md for long description."""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "WellPath Scoring System"

setup(
    name="wellpath-scoring",
    version="1.0.0",
    author="WellPath Team",
    author_email="team@wellpath.ai",
    description="Comprehensive health assessment pipeline with biomarker, survey, and recommendation scoring",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/wellpath/preliminary_data",
    
    # Package configuration
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    
    # Dependencies
    install_requires=read_requirements(),
    
    # Entry points for command-line scripts
    entry_points={
        'console_scripts': [
            'wellpath-score=wellpath.cli:main',
            'wellpath-generate-config=wellpath.recommendation.config_generator:main',
        ],
    },
    
    # Package data
    package_data={
        "wellpath": [
            "ref_csv_files_airtable/*.csv",
            "schemas/*.json",
            "generated_configs/*.json",
        ],
    },
    include_package_data=True,
    
    # Classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    
    # Keywords
    keywords="health, scoring, biomarkers, survey, recommendations, wellpath",
    
    # Project URLs
    project_urls={
        "Bug Reports": "https://github.com/wellpath/preliminary_data/issues",
        "Source": "https://github.com/wellpath/preliminary_data",
        "Documentation": "https://github.com/wellpath/preliminary_data/docs",
    },
)