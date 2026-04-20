#!/usr/bin/env pwsh
# Script to run tests with proper PYTHONPATH setup

# Activate virtual environment
.\.venv\Scripts\activate

# Set PYTHONPATH to current directory
$env:PYTHONPATH = $PWD

# Run pytest
pytest tests/test_config.py -v