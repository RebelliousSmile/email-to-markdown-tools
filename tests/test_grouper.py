"""Tests for src/grouper.py following TDD principles."""

from src.grouper import _normalize_subject, group_emails


def test_normalize_subject_strip_prefixes():
    """Test that _normalize_subject strips thread prefixes correctly."""
    assert _normalize_subject("Re: Subject") == "subject"
    assert _normalize_subject("Fwd: Re: Subject") == "subject"
    assert _normalize_subject("RE: FW: Subject") == "subject"
    assert _normalize_subject("Tr: Subject") == "subject"


def test_normalize_subject_lowercase_and_strip():
    """Test that _normalize_subject lowercases and strips whitespace."""
    assert _normalize_subject("  SUBJECT  ") == "subject"
    assert _normalize_subject("Re:  SUBJECT  ") == "subject"


def test_group_emails_travail_category():
    """Test that group_emails groups travail emails by normalized subject."""
    emails = [
        {"category": "travail", "sender": "sender1", "subject": "Re: Meeting"},
        {"category": "travail", "sender": "sender2", "subject": "Meeting"},
        {"category": "travail", "sender": "sender3", "subject": "Re: Meeting"},
    ]
    
    result = group_emails(emails)
    
    # All emails should be grouped under the same normalized subject key
    assert len(result) == 1
    assert "travail::meeting" in result
    assert len(result["travail::meeting"]) == 3


def test_group_emails_other_categories():
    """Test that group_emails groups other categories by sender."""
    emails = [
        {"category": "notification", "sender": "sender1", "subject": "Notification 1"},
        {"category": "notification", "sender": "sender1", "subject": "Notification 2"},
        {"category": "notification", "sender": "sender2", "subject": "Notification 3"},
        {"category": "newsletter", "sender": "sender3", "subject": "Newsletter 1"},
        {"category": "associatif", "sender": "sender4", "subject": "Associatif 1"},
    ]
    
    result = group_emails(emails)
    
    # Emails should be grouped by sender for each category
    assert len(result) == 4
    assert "notification::sender1" in result
    assert "notification::sender2" in result
    assert "newsletter::sender3" in result
    assert "associatif::sender4" in result


def test_group_emails_mixed_categories():
    """Test that group_emails handles mixed categories correctly."""
    emails = [
        {"category": "travail", "sender": "sender1", "subject": "Re: Meeting"},
        {"category": "notification", "sender": "sender2", "subject": "Notification"},
        {"category": "travail", "sender": "sender3", "subject": "Project Update"},
        {"category": "newsletter", "sender": "sender4", "subject": "Newsletter"},
    ]
    
    result = group_emails(emails)
    
    # Emails should be grouped by normalized subject for travail and by sender for others
    assert len(result) == 4
    assert "travail::meeting" in result
    assert "travail::project update" in result
    assert "notification::sender2" in result
    assert "newsletter::sender4" in result


def test_group_emails_empty_list():
    """Test that group_emails handles an empty list correctly."""
    emails = []
    
    result = group_emails(emails)
    
    assert result == {}


def test_group_emails_missing_category():
    """Test that group_emails defaults to 'travail' when category is missing."""
    emails = [
        {"sender": "sender1", "subject": "Subject"},
    ]
    
    result = group_emails(emails)
    
    assert "travail::subject" in result
    assert len(result["travail::subject"]) == 1