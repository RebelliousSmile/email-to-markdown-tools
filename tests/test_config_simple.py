"""Simplified tests for src/config.py without complex mocking."""

import sys
from pathlib import Path
import pytest
import yaml
from unittest.mock import patch, MagicMock

# Import the function to test
from src.config import load_config

def test_load_config_with_valid_file():
    """Test that load_config works with a valid file."""
    # Create a temporary config file for testing
    config_path = Path("config/config.yaml")
    
    # Since the file exists in our project, this should work
    if config_path.exists():
        result = load_config(config_path)
        assert isinstance(result, dict)
        # Should have some keys from the actual config
        assert len(result) > 0

def test_load_config_file_not_found_simple():
    """Simple test for file not found - without complex mocking."""
    # Create a path that definitely doesn't exist
    config_path = Path("/definitely/does/not/exist/config.yaml")
    
    # This should raise SystemExit
    with pytest.raises(SystemExit) as exc_info:
        load_config(config_path)
    
    # SystemExit should have code 1
    assert exc_info.value.code == 1