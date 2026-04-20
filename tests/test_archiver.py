"""Tests for src/archiver.py following TDD principles."""

from pathlib import Path
from unittest.mock import patch, MagicMock

from src.archiver import archive


def test_archive_move_file():
    """Test that archive moves the file to the processed directory."""
    filepath = Path("/path/to/file.txt")
    processed_dir = Path("/path/to/processed")
    
    with patch('pathlib.Path.mkdir') as mock_mkdir:
        with patch('shutil.move') as mock_move:
            archive(filepath, processed_dir, delete=False)
            
            # Verify that mkdir was called to create the processed directory
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
            
            # Verify that shutil.move was called with the correct arguments
            mock_move.assert_called_once_with(str(filepath), processed_dir / filepath.name)


def test_archive_delete_file():
    """Test that archive deletes the file when delete=True."""
    filepath = Path("/path/to/file.txt")
    processed_dir = Path("/path/to/processed")
    
    with patch('pathlib.Path.unlink') as mock_unlink:
        archive(filepath, processed_dir, delete=True)
        
        # Verify that unlink was called to delete the file
        mock_unlink.assert_called_once()


def test_archive_create_processed_dir():
    """Test that archive creates the processed directory if it does not exist."""
    filepath = Path("/path/to/file.txt")
    processed_dir = Path("/path/to/processed")
    
    with patch('pathlib.Path.mkdir') as mock_mkdir:
        with patch('shutil.move') as mock_move:
            archive(filepath, processed_dir, delete=False)
            
            # Verify that mkdir was called to create the processed directory
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)