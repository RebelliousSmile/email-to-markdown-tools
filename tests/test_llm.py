"""Tests for src/llm.py following TDD principles."""

import os
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from src.llm import _load_config, classify_email


def test_load_config_no_file():
    """Test that _load_config returns an empty dict when config file does not exist."""
    # Mock the config file path to not exist
    with patch('src.llm.Path') as mock_path:
        mock_path.return_value.exists.return_value = False
        config = _load_config()
        assert config == {}


def test_load_config_with_file():
    """Test that _load_config loads the config file when it exists."""
    # Mock the config file path to exist and return a mock config
    with patch('src.llm.Path') as mock_path:
        mock_path.return_value.exists.return_value = True
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = "llm:\n  api_key: test_key\n  model: test_model"
        mock_path.return_value.open.return_value = mock_file
        
        with patch('src.llm.yaml.safe_load') as mock_yaml:
            mock_yaml.return_value = {"llm": {"api_key": "test_key", "model": "test_model"}}
            config = _load_config()
            assert config == {"llm": {"api_key": "test_key", "model": "test_model"}}


def test_classify_email_api_failure():
    """Test that classify_email returns 'travail' when the API call fails."""
    # Mock the anthropic import to raise an ImportError
    with patch('src.llm.anthropic', side_effect=ImportError):
        result = classify_email("Test Subject", "Test Body")
        assert result == "travail"


def test_classify_email_invalid_response():
    """Test that classify_email returns 'travail' when the API response is invalid."""
    # Mock the anthropic client to return an invalid response
    with patch('src.llm.anthropic.Anthropic') as mock_anthropic:
        mock_client = MagicMock()
        mock_message = MagicMock()
        mock_message.content = [MagicMock(text="invalid_category")]
        mock_client.messages.create.return_value = mock_message
        mock_anthropic.return_value = mock_client
        
        result = classify_email("Test Subject", "Test Body")
        assert result == "travail"


def test_classify_email_valid_response():
    """Test that classify_email returns the correct category when the API response is valid."""
    # Mock the anthropic client to return a valid response
    with patch('src.llm.anthropic.Anthropic') as mock_anthropic:
        mock_client = MagicMock()
        mock_message = MagicMock()
        mock_message.content = [MagicMock(text="newsletter")]
        mock_client.messages.create.return_value = mock_message
        mock_anthropic.return_value = mock_client
        
        result = classify_email("Test Subject", "Test Body")
        assert result == "newsletter"


def test_classify_email_with_env_api_key():
    """Test that classify_email uses the API key from environment variables."""
    # Set a temporary environment variable for the API key
    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "env_key"}):
        with patch('src.llm.anthropic.Anthropic') as mock_anthropic:
            mock_client = MagicMock()
            mock_message = MagicMock()
            mock_message.content = [MagicMock(text="travail")]
            mock_client.messages.create.return_value = mock_message
            mock_anthropic.return_value = mock_client
            
            result = classify_email("Test Subject", "Test Body")
            # Verify that the client was initialized with the environment API key
            mock_anthropic.assert_called_once_with(api_key="env_key")
            assert result == "travail"


def test_classify_email_with_config_api_key():
    """Test that classify_email uses the API key from the config file."""
    # Mock the config file to return an API key
    with patch('src.llm._load_config') as mock_load_config:
        mock_load_config.return_value = {"llm": {"api_key": "config_key", "model": "test_model"}}
        
        with patch('src.llm.anthropic.Anthropic') as mock_anthropic:
            mock_client = MagicMock()
            mock_message = MagicMock()
            mock_message.content = [MagicMock(text="associatif")]
            mock_client.messages.create.return_value = mock_message
            mock_anthropic.return_value = mock_client
            
            result = classify_email("Test Subject", "Test Body")
            # Verify that the client was initialized with the config API key
            mock_anthropic.assert_called_once_with(api_key="config_key")
            assert result == "associatif"