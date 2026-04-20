"""Tests for src/parser.py following TDD principles."""

from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
import pytest

from src.parser import parse_email, VALID_EMAIL_TYPES


def test_parse_valid_email():
    """Test that parse_email correctly parses a valid email file."""
    # Create a temporary file with valid email data
    email_content = """
---
from: sender@example.com
to: recipient@example.com
date: 2023-01-01T12:00:00+00:00
subject: Test Subject
subject_hash: abc123
email_type: direct
---

This is the email body.
"""
    with NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(email_content)
        temp_filepath = Path(f.name)

    try:
        result = parse_email(temp_filepath)
        
        # Verify the parsed data
        assert result['sender'] == 'sender@example.com'
        assert result['to'] == 'recipient@example.com'
        assert result['date'] == datetime(2023, 1, 1, 12, 0, tzinfo=timezone.utc)
        assert result['subject'] == 'Test Subject'
        assert result['subject_hash'] == 'abc123'
        assert result['email_type'] == 'direct'
        assert result['body'] == 'This is the email body.'
        assert result['filepath'] == temp_filepath
    finally:
        temp_filepath.unlink()  # Clean up the temporary file


def test_parse_missing_required_field():
    """Test that parse_email raises ValueError if a required field is missing."""
    # Create a temporary file missing the 'from' field
    email_content = """
---
to: recipient@example.com
date: 2023-01-01T12:00:00+00:00
subject: Test Subject
---

This is the email body.
"""
    with NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(email_content)
        temp_filepath = Path(f.name)

    try:
        with pytest.raises(ValueError, match="Missing required field 'from'"):
            parse_email(temp_filepath)
    finally:
        temp_filepath.unlink()


def test_parse_non_timezone_aware_date():
    """Test that parse_email raises ValueError if the date is not timezone-aware."""
    email_content = """
---
from: sender@example.com
to: recipient@example.com
date: 2023-01-01T12:00:00
subject: Test Subject
---

This is the email body.
"""
    with NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(email_content)
        temp_filepath = Path(f.name)

    try:
        with pytest.raises(ValueError, match="'date' field.*not timezone-aware"):
            parse_email(temp_filepath)
    finally:
        temp_filepath.unlink()


def test_parse_invalid_email_type():
    """Test that parse_email raises ValueError if email_type is invalid."""
    email_content = """
---
from: sender@example.com
to: recipient@example.com
date: 2023-01-01T12:00:00+00:00
subject: Test Subject
email_type: invalid_type
---

This is the email body.
"""
    with NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(email_content)
        temp_filepath = Path(f.name)

    try:
        with pytest.raises(ValueError, match="Invalid 'email_type' value"):
            parse_email(temp_filepath)
    finally:
        temp_filepath.unlink()


def test_parse_valid_email_types():
    """Test that parse_email accepts all valid email types."""
    for email_type in VALID_EMAIL_TYPES:
        email_content = f"""
---
from: sender@example.com
to: recipient@example.com
date: 2023-01-01T12:00:00+00:00
subject: Test Subject
email_type: {email_type}
---

This is the email body.
"""
        with NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(email_content)
            temp_filepath = Path(f.name)

        try:
            result = parse_email(temp_filepath)
            assert result['email_type'] == email_type
        finally:
            temp_filepath.unlink()


def test_parse_optional_subject_hash():
    """Test that parse_email handles missing subject_hash correctly."""
    email_content = """
---
from: sender@example.com
to: recipient@example.com
date: 2023-01-01T12:00:00+00:00
subject: Test Subject
---

This is the email body.
"""
    with NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(email_content)
        temp_filepath = Path(f.name)

    try:
        result = parse_email(temp_filepath)
        assert result['subject_hash'] is None
    finally:
        temp_filepath.unlink()


def test_parse_optional_email_type():
    """Test that parse_email handles missing email_type correctly."""
    email_content = """
---
from: sender@example.com
to: recipient@example.com
date: 2023-01-01T12:00:00+00:00
subject: Test Subject
---

This is the email body.
"""
    with NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(email_content)
        temp_filepath = Path(f.name)

    try:
        result = parse_email(temp_filepath)
        assert result['email_type'] is None
    finally:
        temp_filepath.unlink()


def test_parse_datetime_object():
    """Test that parse_email handles datetime objects in the date field."""
    email_content = """
---
from: sender@example.com
to: recipient@example.com
date: 2023-01-01T12:00:00+00:00
subject: Test Subject
---

This is the email body.
"""
    with NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(email_content)
        temp_filepath = Path(f.name)

    try:
        result = parse_email(temp_filepath)
        assert result['date'] == datetime(2023, 1, 1, 12, 0, tzinfo=timezone.utc)
    finally:
        temp_filepath.unlink()