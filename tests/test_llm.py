"""Tests for src/llm.py — classification via Ollama local."""

import pytest
from unittest.mock import patch, MagicMock

from src.llm import _get_llm_config, classify_email


def test_get_llm_config_returns_dict():
    with patch('src.llm.load_config') as mock_load:
        mock_load.return_value = {"ollama": {"url": "http://localhost:11434", "model": "qwen3:8b"}}
        config = _get_llm_config()
        assert config == {"url": "http://localhost:11434", "model": "qwen3:8b"}


def test_get_llm_config_missing_section():
    with patch('src.llm.load_config') as mock_load:
        mock_load.return_value = {}
        config = _get_llm_config()
        assert config == {}


def _make_ollama_response(text: str) -> MagicMock:
    response = MagicMock()
    response.message.content = text
    return response


def test_classify_email_valid_category():
    with patch('src.llm.ollama') as mock_ollama:
        mock_client = MagicMock()
        mock_ollama.Client.return_value = mock_client
        mock_client.chat.return_value = _make_ollama_response("newsletter")

        result = classify_email("Test Subject", "Test Body")
        assert result == "newsletter"


def test_classify_email_invalid_response_falls_back():
    with patch('src.llm.ollama') as mock_ollama:
        mock_client = MagicMock()
        mock_ollama.Client.return_value = mock_client
        mock_client.chat.return_value = _make_ollama_response("invalid_category")

        result = classify_email("Test Subject", "Test Body")
        assert result == "travail"


def test_classify_email_api_failure_falls_back():
    with patch('src.llm.ollama') as mock_ollama:
        mock_client = MagicMock()
        mock_ollama.Client.return_value = mock_client
        mock_client.chat.side_effect = Exception("connection refused")

        result = classify_email("Test Subject", "Test Body")
        assert result == "travail"


def test_classify_email_empty_subject_falls_back():
    result = classify_email("", "Some body")
    assert result == "travail"


def test_classify_email_empty_body_falls_back():
    result = classify_email("Some subject", "")
    assert result == "travail"


def test_classify_email_all_categories():
    for category in ("travail", "notification", "newsletter", "associatif"):
        with patch('src.llm.ollama') as mock_ollama:
            mock_client = MagicMock()
            mock_ollama.Client.return_value = mock_client
            mock_client.chat.return_value = _make_ollama_response(category)
            result = classify_email("Subject", "Body")
            assert result == category
