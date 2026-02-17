import pytest
import numpy as np

import mlbstatscraping as ss


import pytest
import numpy as np
import pandas as pd
import mlbstatscraping as ss

@pytest.fixture
def hitting_data():
    """Fixture to get hitting data for 2024."""
    return ss.get_fangraphs_data('hitting', ['2024'])


@pytest.fixture
def pitching_data():
    """Fixture to get pitching data for 2024."""
    return ss.get_fangraphs_data('pitching', ['2024'])


def test_get_fangraphs_data_hitting_returns_dataframe(hitting_data):
    """Test that hitting data returns a DataFrame."""
    assert isinstance(hitting_data, pd.DataFrame)
    assert len(hitting_data) > 0


def test_get_fangraphs_data_pitching_returns_dataframe(pitching_data):
    """Test that pitching data returns a DataFrame."""
    assert isinstance(pitching_data, pd.DataFrame)
    assert len(pitching_data) > 0


def test_invalid_stat_type_raises_error():
    """Test that invalid stat type raises ValueError."""
    with pytest.raises(ValueError):
        ss.get_fangraphs_data('invalid_type', ['2024'])


def test_multiple_years(hitting_data):
    """Test retrieving data for multiple years."""
    multi_year = ss.get_fangraphs_data('hitting', ['2023', '2024'])
    assert isinstance(multi_year, pd.DataFrame)
    assert len(multi_year) > len(hitting_data)


def test_hitting_data_has_expected_columns(hitting_data):
    """Test that hitting data contains expected columns."""
    assert len(hitting_data.columns) > 0
    assert 'Name' in hitting_data.columns or 'Player' in hitting_data.columns


def test_pitching_data_has_expected_columns(pitching_data):
    """Test that pitching data contains expected columns."""
    assert len(pitching_data.columns) > 0