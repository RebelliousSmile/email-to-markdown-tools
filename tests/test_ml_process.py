import pytest
import logging
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.folder_classifier import rebuild_model_from_corpus, record_decision


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create a temporary data directory with a corpus."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    corpus_path = data_dir / "corpus.jsonl"
    corpus_path.write_text(
        '{"subject": "Test 1", "sender": "test1@example.com", "email_type": "direct", "label": "Travail/Projets/Test"}\n'
        '{"subject": "Test 2", "sender": "test2@example.com", "email_type": "group", "label": "Personnel/Famille/Vacances"}\n'
    )
    return data_dir


def test_rebuild_model_from_corpus(temp_data_dir, caplog):
    """Test that rebuild_model_from_corpus reconstructs the model and logs correctly."""
    with caplog.at_level(logging.INFO):
        rebuild_model_from_corpus(temp_data_dir)
        
        # Check that logs were generated
        assert any("Reconstruction du modèle depuis" in record.message for record in caplog.records)
        assert any("Modèle reconstruit et sauvegardé avec succès" in record.message for record in caplog.records)
        
        # Check that model files were created
        assert (temp_data_dir / "model.pkl").exists()
        assert (temp_data_dir / "vectorizer.pkl").exists()


def test_rebuild_model_from_corpus_empty_corpus(tmp_path, caplog):
    """Test that rebuild_model_from_corpus handles empty corpus correctly."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    corpus_path = data_dir / "corpus.jsonl"
    corpus_path.write_text("")
    
    with caplog.at_level(logging.WARNING):
        rebuild_model_from_corpus(data_dir)
        
        # Check that a warning was logged
        assert any("Corpus vide, impossible de reconstruire le modèle" in record.message for record in caplog.records)


def test_record_decision_updates_model(temp_data_dir, caplog):
    """Test that record_decision updates the model and logs correctly."""
    # First, rebuild the model
    rebuild_model_from_corpus(temp_data_dir)
    
    # Mock the config
    config = {"classify": {"data_dir": str(temp_data_dir)}}
    
    # Record a new decision with a known class
    email = {
        "subject": "Test 3",
        "sender": "test3@example.com",
        "email_type": "direct"
    }
    
    with caplog.at_level(logging.INFO):
        record_decision(email, "Travail/Projets/Test2", config)
        
        # Check that logs were generated
        assert any("Modèle mis à jour avec la décision utilisateur" in record.message for record in caplog.records)
        
        # Check that corpus was updated
        corpus_path = temp_data_dir / "corpus.jsonl"
        assert "Test 3" in corpus_path.read_text()


def test_record_decision_rebuilds_model_if_missing(temp_data_dir, caplog):
    """Test that record_decision rebuilds the model if it doesn't exist."""
    # Ensure no model exists
    (temp_data_dir / "model.pkl").unlink(missing_ok=True)
    (temp_data_dir / "vectorizer.pkl").unlink(missing_ok=True)
    
    # Mock the config
    config = {"classify": {"data_dir": str(temp_data_dir)}}
    
    # Record a decision
    email = {
        "subject": "Test 4",
        "sender": "test4@example.com",
        "email_type": "direct"
    }
    
    with caplog.at_level(logging.INFO):
        record_decision(email, "Travail/Projets/Test2", config)
        
        # Check that logs were generated
        assert any("Modèle non trouvé, reconstruction depuis le corpus" in record.message for record in caplog.records)
        assert any("Modèle reconstruit et sauvegardé avec succès" in record.message for record in caplog.records)


def test_rebuild_model_from_corpus_corrupted(tmp_path, caplog):
    """Test that rebuild_model_from_corpus handles corrupted corpus entries."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    corpus_path = data_dir / "corpus.jsonl"
    corpus_path.write_text(
        '{"subject": "Test 1", "sender": "test1@example.com", "email_type": "direct", "label": "Travail/Projets/Test"}\n'
        '{"corrupted": "entry"}\n'  # Corrupted entry
        '{"subject": "Test 2", "sender": "test2@example.com", "email_type": "group", "label": "Personnel/Famille/Vacances"}\n'
    )
    
    with caplog.at_level(logging.WARNING):
        rebuild_model_from_corpus(data_dir)
        
        # Check that model was rebuilt despite corrupted entry
        assert (data_dir / "model.pkl").exists()
        assert (data_dir / "vectorizer.pkl").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
