"""Tests for src/config.py following TDD principles."""

import sys
import pytest
import yaml
from unittest.mock import patch, MagicMock
from pathlib import Path

from src.config import load_config


def test_load_config_file_not_found():
    """Test that load_config exits with error when config file does not exist."""
    # Create a mock Path object
    config_path = MagicMock(spec=Path)
    config_path.exists.return_value = False
    config_path.__str__ = lambda self: "/non/existent/path/config.yaml"
    
    # Mock sys.exit to avoid exiting the test process
    with patch('sys.exit') as mock_exit:
        with patch('sys.stderr.write') as mock_stderr:
            load_config(config_path)
            
            # Verify that an error message was printed to stderr
            mock_stderr.assert_called_once()
            assert "Erreur: fichier de configuration introuvable" in mock_stderr.call_args[0][0]
            
            # Verify that sys.exit was called with error code 1
            mock_exit.assert_called_once_with(1)


def test_load_config_valid_yaml():
    """Test that load_config loads a valid YAML file correctly."""
    config_path = MagicMock(spec=Path)
    config_path.exists.return_value = True
    
    mock_file = MagicMock()
    mock_file.__enter__.return_value.read.return_value = "key: value\nanother_key: 123"
    
    with patch('builtins.open', return_value=mock_file):
        with patch('yaml.safe_load') as mock_yaml_load:
            mock_yaml_load.return_value = {"key": "value", "another_key": 123}
            
            result = load_config(config_path)
            assert result == {"key": "value", "another_key": 123}


def test_load_config_empty_yaml():
    """Test that load_config returns an empty dict when YAML file is empty."""
    config_path = MagicMock(spec=Path)
    config_path.exists.return_value = True
    
    mock_file = MagicMock()
    mock_file.__enter__.return_value.read.return_value = ""
    
    with patch('builtins.open', return_value=mock_file):
        with patch('yaml.safe_load') as mock_yaml_load:
            mock_yaml_load.return_value = None
            
            result = load_config(config_path)
            assert result == {}


def test_load_config_invalid_yaml():
    """Test that load_config handles invalid YAML gracefully."""
    config_path = MagicMock(spec=Path)
    config_path.exists.return_value = True
    
    mock_file = MagicMock()
    mock_file.__enter__.return_value.read.return_value = "invalid: yaml: content:"
    
    with patch('builtins.open', return_value=mock_file):
        with patch('yaml.safe_load') as mock_yaml_load:
            # Simulate a YAML parsing error
            mock_yaml_load.side_effect = yaml.YAMLError("Invalid YAML")
            
            # Verify that the error is propagated
            with pytest.raises(yaml.YAMLError):
                load_config(config_path)