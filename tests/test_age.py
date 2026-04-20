"""Tests for src/age.py following TDD principles."""

from datetime import datetime, timezone, timedelta
from unittest.mock import patch

from src.age import age_in_days


def test_age_in_days_past_date():
    """Test that age_in_days returns the correct number of days for a past date."""
    past_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
    expected_days = (datetime.now(timezone.utc) - past_date).days
    
    result = age_in_days(past_date)
    
    assert result == expected_days


def test_age_in_days_current_date():
    """Test that age_in_days returns 0 for the current date."""
    current_date = datetime.now(timezone.utc)
    
    result = age_in_days(current_date)
    
    assert result == 0


def test_age_in_days_future_date():
    """Test that age_in_days returns a negative number for a future date."""
    future_date = datetime.now(timezone.utc) + timedelta(days=5)
    
    result = age_in_days(future_date)
    
    assert result == -5


def test_age_in_days_with_mock():
    """Test that age_in_days uses the current time correctly by mocking datetime.now."""
    fixed_now = datetime(2023, 1, 10, tzinfo=timezone.utc)
    past_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
    
    with patch('src.age.datetime') as mock_datetime:
        mock_datetime.now.return_value = fixed_now
        
        result = age_in_days(past_date)
        
        assert result == 9