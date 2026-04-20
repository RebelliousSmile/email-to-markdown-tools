"""Tests for src/deduplicator.py following TDD principles."""

from datetime import datetime, timezone

from src.deduplicator import deduplicate


def test_deduplicate_none_subject_hash():
    """Test that emails with subject_hash=None are never deduplicated."""
    emails = [
        {"subject_hash": None, "sender": "sender1", "date": datetime(2023, 1, 1, tzinfo=timezone.utc)},
        {"subject_hash": None, "sender": "sender1", "date": datetime(2023, 1, 2, tzinfo=timezone.utc)},
        {"subject_hash": "hash1", "sender": "sender1", "date": datetime(2023, 1, 3, tzinfo=timezone.utc)},
    ]
    
    result = deduplicate(emails)
    
    # All emails should be kept since None-hash emails are never deduplicated
    assert len(result) == 3
    assert result[0]["subject_hash"] is None
    assert result[1]["subject_hash"] is None
    assert result[2]["subject_hash"] == "hash1"


def test_deduplicate_same_hash_and_sender():
    """Test that emails with the same subject_hash and sender are deduplicated, keeping the earliest."""
    emails = [
        {"subject_hash": "hash1", "sender": "sender1", "date": datetime(2023, 1, 3, tzinfo=timezone.utc)},
        {"subject_hash": "hash1", "sender": "sender1", "date": datetime(2023, 1, 2, tzinfo=timezone.utc)},
        {"subject_hash": "hash1", "sender": "sender1", "date": datetime(2023, 1, 1, tzinfo=timezone.utc)},
    ]
    
    result = deduplicate(emails)
    
    # Only the earliest email should be kept
    assert len(result) == 1
    assert result[0]["date"] == datetime(2023, 1, 1, tzinfo=timezone.utc)


def test_deduplicate_preserve_order():
    """Test that the original order of emails is preserved."""
    emails = [
        {"subject_hash": "hash1", "sender": "sender1", "date": datetime(2023, 1, 1, tzinfo=timezone.utc)},
        {"subject_hash": None, "sender": "sender2", "date": datetime(2023, 1, 2, tzinfo=timezone.utc)},
        {"subject_hash": "hash2", "sender": "sender3", "date": datetime(2023, 1, 3, tzinfo=timezone.utc)},
        {"subject_hash": "hash1", "sender": "sender1", "date": datetime(2023, 1, 4, tzinfo=timezone.utc)},
    ]
    
    result = deduplicate(emails)
    
    # The order should be preserved: hash1 (first occurrence), None-hash, hash2, and hash1 (second occurrence) is deduplicated
    assert len(result) == 3
    assert result[0]["subject_hash"] == "hash1"
    assert result[1]["subject_hash"] is None
    assert result[2]["subject_hash"] == "hash2"


def test_deduplicate_different_hash_or_sender():
    """Test that emails with different subject_hash or sender are not deduplicated."""
    emails = [
        {"subject_hash": "hash1", "sender": "sender1", "date": datetime(2023, 1, 1, tzinfo=timezone.utc)},
        {"subject_hash": "hash2", "sender": "sender1", "date": datetime(2023, 1, 2, tzinfo=timezone.utc)},
        {"subject_hash": "hash1", "sender": "sender2", "date": datetime(2023, 1, 3, tzinfo=timezone.utc)},
    ]
    
    result = deduplicate(emails)
    
    # All emails should be kept since they have different keys
    assert len(result) == 3
    assert result[0]["subject_hash"] == "hash1"
    assert result[1]["subject_hash"] == "hash2"
    assert result[2]["subject_hash"] == "hash1"


def test_deduplicate_empty_list():
    """Test that deduplicate handles an empty list correctly."""
    emails = []
    
    result = deduplicate(emails)
    
    assert result == []


def test_deduplicate_all_none_hash():
    """Test that deduplicate keeps all emails when all have subject_hash=None."""
    emails = [
        {"subject_hash": None, "sender": "sender1", "date": datetime(2023, 1, 1, tzinfo=timezone.utc)},
        {"subject_hash": None, "sender": "sender2", "date": datetime(2023, 1, 2, tzinfo=timezone.utc)},
        {"subject_hash": None, "sender": "sender1", "date": datetime(2023, 1, 3, tzinfo=timezone.utc)},
    ]
    
    result = deduplicate(emails)
    
    # All emails should be kept since None-hash emails are never deduplicated
    assert len(result) == 3