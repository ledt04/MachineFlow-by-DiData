# MachineFlow-by-DiData

Automated data extraction and API integration pipeline for laboratory instruments. Developed as part of a Bachelor's internship project at the University of Zurich (UZH).

## Overview
MashineFlow-by-DiData acts as an intelligent middleware between lab hardware and the central DiData management system. It reads output CSV files from laboratory machines, cleans and processes the data, matches samples with existing DiData entities, and automatically batch-uploads the results via the DiData API.

Currently, the system supports data flows for two primary machines:
* **Qubit:** Handles DNA, 16S PCR, and 16S Library quantification.
* **Fragment Analyzer:** Handles Post PCR Visualization & Clean up, and Library Visualization.

## Key Features
* **Automated Data Extraction:** Parses raw CSV files while filtering out noise (e.g., standardizing headers, removing "BLANK", "LADDER", and "Standard" calibration rows).
* **Intelligent Sample Matching:** Maps raw machine data to corresponding DiData State IDs, cross-referencing sample names and handling missing library IDs via sequential ID checking.
* **Complex Pooling Logic:** Supports both monolithic and modular PCR pooling for the Qubit machine, automatically distributing quantification values across pool groups based on existing DiData records.
* **Validation Thresholds:** Automatically flags Fragment Analyzer samples for "Human Validation" if base pair peaks fall outside the expected 500-700 bp range.
* **Dynamic API Integration:** Securely fetches workflows, state IDs, and project entities, then constructs batched `PUT` requests to seamlessly update the DiData system.

## Project Structure

```text
MashineFlow-by-DiData/
├── .env                    # Environment variables (API keys, Base URLs)
├── readme.md               # Project documentation
├── requirements.txt        # Python dependencies
├── tests/                  # Test data directories
└── src/
    ├── config/
    │   ├── config.json     # Machine IDs, Kit values, and State ID mapping
    │   └── settings.py     # Global variables and config loaders
    ├── mashines/
    │   ├── fragmentanalyzer/
    │   │   ├── api_manager.py
    │   │   ├── data_extracter.py
    │   │   ├── main.py
    │   │   ├── sample_classifier.py
    │   │   ├── sample_filter.py
    │   │   └── sample_uploader.py
    │   └── qubit/
    │       ├── api_manager.py
    │       ├── main.py
    │       ├── sample_classifier.py
    │       └── sample_uploader.py
    ├── mastercontroller/
    │   └── main.py
    └── utils/
        ├── auth.py         # Handles API headers
        ├── csv_manager.py  # Pandas CSV operations
        ├── error_handling.py
        └── logger.py
