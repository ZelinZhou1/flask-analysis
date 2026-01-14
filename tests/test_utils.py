# -*- coding: utf-8 -*-
"""
Tests for utils module.
"""

import pytest
from datetime import datetime
from src.utils.date_utils import parse_date, get_weekday_name, is_weekend, get_quarter


def test_parse_date():
    """Test date parsing with various formats."""
    # Standard format
    d1 = parse_date("2023-01-01 12:00:00")
    assert isinstance(d1, datetime)
    assert d1.year == 2023
    assert d1.month == 1

    # ISO format
    d2 = parse_date("2023-01-01T12:00:00")
    assert d2.year == 2023

    # Date only
    d3 = parse_date("2023-01-01")
    assert d3.year == 2023

    # Invalid
    d4 = parse_date("invalid")
    assert d4 is None

    # None
    assert parse_date(None) is None


def test_get_weekday_name():
    """Test weekday name retrieval."""
    dt = datetime(2023, 1, 1)  # Sunday

    # CN
    assert get_weekday_name(dt, "cn") == "周日"

    # EN
    assert get_weekday_name(dt, "en") == "Sun"


def test_is_weekend():
    """Test weekend detection."""
    sun = datetime(2023, 1, 1)  # Sunday
    mon = datetime(2023, 1, 2)  # Monday

    assert is_weekend(sun) is True
    assert is_weekend(mon) is False


def test_get_quarter():
    """Test quarter calculation."""
    d1 = datetime(2023, 1, 1)  # Q1
    d2 = datetime(2023, 4, 1)  # Q2
    d3 = datetime(2023, 9, 1)  # Q3
    d4 = datetime(2023, 12, 1)  # Q4

    assert get_quarter(d1) == 1
    assert get_quarter(d2) == 2
    assert get_quarter(d3) == 3
    assert get_quarter(d4) == 4
