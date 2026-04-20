import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.folder_classifier import propose_path, record_decision, _llm_propose_path


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


def test_propose_path_small_corpus():
    """Test that propose_path uses LLM when corpus is too small."""
    email = {
        "subject": "Test email",
        "sender": "test@example.com",
        "email_type": "direct"
    }
    config = {"classify": {"min_samples_before_ml": 100}}
    
    with patch('src.folder_classifier._load_corpus') as mock_load_corpus:
        mock_load_corpus.return_value = []  # Empty corpus
        
        with patch('src.folder_classifier._llm_propose_path') as mock_llm_propose_path:
            mock_llm_propose_path.return_value = "Test/Test/Test"
            
            result = propose_path(email, config)
            
            # Verify that _llm_propose_path was called
            mock_llm_propose_path.assert_called_once()
            assert result == "Test/Test/Test"


def test_propose_path_no_model():
    """Test that propose_path uses LLM when model is None."""
    email = {
        "subject": "Test email",
        "sender": "test@example.com",
        "email_type": "direct"
    }
    config = {"classify": {"min_samples_before_ml": 10}}
    
    with patch('src.folder_classifier._load_corpus') as mock_load_corpus:
        mock_load_corpus.return_value = [{"subject": "Test", "sender": "test", "label": "Test/Test/Test"}] * 20
        
        with patch('src.folder_classifier._load_model') as mock_load_model:
            mock_load_model.return_value = (None, None)
            
            with patch('src.folder_classifier._llm_propose_path') as mock_llm_propose_path:
                mock_llm_propose_path.return_value = "Test/Test/Test"
                
                result = propose_path(email, config)
                
                # Verify that _llm_propose_path was called
                mock_llm_propose_path.assert_called_once()
                assert result == "Test/Test/Test"


def test_propose_path_low_confidence():
    """Test that propose_path uses LLM when confidence is too low."""
    email = {
        "subject": "Test email",
        "sender": "test@example.com",
        "email_type": "direct"
    }
    config = {"classify": {"min_samples_before_ml": 10, "confidence_threshold": 0.9}}
    
    with patch('src.folder_classifier._load_corpus') as mock_load_corpus:
        mock_load_corpus.return_value = [{"subject": "Test", "sender": "test", "label": "Test/Test/Test"}] * 20
        
        with patch('src.folder_classifier._load_model') as mock_load_model:
            mock_model = MagicMock()
            mock_vectorizer = MagicMock()
            mock_load_model.return_value = (mock_model, mock_vectorizer)
            
            with patch('src.folder_classifier._ml_propose_path') as mock_ml_propose_path:
                mock_ml_propose_path.return_value = ("Test/Test/Test", 0.5)
                
                with patch('src.folder_classifier._llm_propose_path') as mock_llm_propose_path:
                    mock_llm_propose_path.return_value = "Test/Test/Test"
                    
                    result = propose_path(email, config)
                    
                    # Verify that _llm_propose_path was called due to low confidence
                    mock_llm_propose_path.assert_called_once()
                    assert result == "Test/Test/Test"


def test_propose_path_high_confidence():
    """Test that propose_path returns ML label when confidence is high."""
    email = {
        "subject": "Test email",
        "sender": "test@example.com",
        "email_type": "direct"
    }
    config = {"classify": {"min_samples_before_ml": 10, "confidence_threshold": 0.5}}
    
    with patch('src.folder_classifier._load_corpus') as mock_load_corpus:
        mock_load_corpus.return_value = [{"subject": "Test", "sender": "test", "label": "Test/Test/Test"}] * 20
        
        with patch('src.folder_classifier._load_model') as mock_load_model:
            mock_model = MagicMock()
            mock_vectorizer = MagicMock()
            mock_load_model.return_value = (mock_model, mock_vectorizer)
            
            with patch('src.folder_classifier._ml_propose_path') as mock_ml_propose_path:
                mock_ml_propose_path.return_value = ("Test/Test/Test", 0.9)
                
                result = propose_path(email, config)
                
                # Verify that ML label was returned
                assert result == "Test/Test/Test"


def test_record_decision():
    """Test that record_decision records the decision correctly."""
    email = {
        "subject": "Test email",
        "sender": "test@example.com",
        "email_type": "direct"
    }
    path = "Test/Test/Test"
    config = {"classify": {"data_dir": "test_data"}}
    
    with patch('pathlib.Path.mkdir'):
        with patch('pathlib.Path.open') as mock_open:
            mock_file = MagicMock()
            mock_open.return_value.__enter__.return_value = mock_file
            
            with patch('json.dumps') as mock_json_dumps:
                mock_json_dumps.return_value = '{"test": "data"}'
                
                with patch('json.load') as mock_json_load:
                    mock_json_load.return_value = []
                    
                    with patch('json.dump'):
                        with patch('src.folder_classifier.rebuild_model_from_corpus'):
                            record_decision(email, path, config)
                            
                            # Verify that the decision was recorded
                            mock_json_dumps.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])