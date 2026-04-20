import pytest
from unittest.mock import patch
from src.folder_classifier import _llm_propose_path


def test_llm_propose_path_format():
    """Test that _llm_propose_path returns a valid 3-level path."""
    email = {
        "subject": "Test email",
        "sender": "test@example.com",
        "email_type": "direct"
    }
    path = _llm_propose_path(email, "qwen3:8b")
    
    # Check that the path has exactly 2 slashes
    assert path.count("/") == 2, f"Expected 2 slashes in path, got: {path}"
    
    # Check that no invalid characters are present
    invalid_chars = ['?', '*', '"', '<', '>', '|']
    assert not any(char in path for char in invalid_chars), f"Invalid characters in path: {path}"
    
    # Check that each part is <= 50 characters
    parts = path.split("/")
    for part in parts:
        assert len(part.strip()) <= 50, f"Part '{part}' exceeds 50 characters"


def test_llm_propose_path_fallback():
    """Test that _llm_propose_path falls back to rule-based if LLM fails."""
    email = {
        "subject": "Test email",
        "sender": "test@example.com",
        "email_type": "invalid_type"
    }
    
    # Mock ollama.chat to raise an exception and test fallback
    with patch('ollama.chat', side_effect=Exception("LLM failed")):
        path = _llm_propose_path(email, "qwen3:8b")
        # Should return default path for unknown email_type
        assert path == "Divers/Divers/Divers", f"Expected fallback path, got: {path}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
