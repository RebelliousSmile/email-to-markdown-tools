"""Tests for src/config.py following TDD principles."""

import sys
import pytest
import yaml
from unittest.mock import patch, MagicMock
from pathlib import Path

from src.config import load_config

def test_load_config_file_not_found():
    """Test that load_config exits with error when config file does not exist."""
    # Create a path that definitely doesn't exist
    config_path = Path("/definitely/does/not/exist/config.yaml")
    
    # This should raise SystemExit
    with pytest.raises(SystemExit) as exc_info:
        load_config(config_path)
    
    # SystemExit should have code 1
    assert exc_info.value.code == 1

def test_load_config_valid_yaml():
    """Test that load_config loads a valid YAML file correctly."""
    # Test with the actual config file which should exist
    config_path = Path("config/config.yaml")
    if config_path.exists():
        result = load_config(config_path)
        assert isinstance(result, dict)
        assert len(result) > 0

def test_load_config_empty_yaml():
    """Test that load_config returns an empty dict when YAML file is empty."""
    config_path = MagicMock(spec=Path)
    config_path.exists.return_value = True
    
    mock_file = MagicMock()
    mock_file.__enter__.return_value.read.return_value = ""
    
    with patch('builtins.open', return_value=mock_file):
        with patch('yaml.safe_load') as mock_yaml_load:
            mock_yaml_load.return_value = None
            
            # We need to patch the internal functions
            with patch('src.config._validate_config_path'):
                with patch('src.config._load_yaml_content') as mock_load_content:
                    mock_load_content.return_value = None
                    
                    from src.config import load_config as actual_load_config
                    result = actual_load_config(config_path)
                    assert result == {}

def test_load_config_invalid_yaml():
    """Test that load_config handles invalid YAML gracefully."""
    config_path = MagicMock(spec=Path)
    config_path.exists.return_value = True
    
    # We need to patch the internal functions to test this properly
    with patch('src.config._validate_config_path'):
        with patch('src.config._load_yaml_content') as mock_load_content:
            # Simulate a YAML parsing error
            mock_load_content.side_effect = yaml.YAMLError("Invalid YAML")
            
            from src.config import load_config as actual_load_config
            # Verify that the error is propagated
            with pytest.raises(yaml.YAMLError):
                actual_load_config(config_path)