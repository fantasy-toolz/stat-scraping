import pytest
import numpy as np

from src import statscraping as ss


#HittingDF = ss.get_fangraphs_data('hitting',['2024'])

def test_nonsense_fangraphs_input():
    """Test that providing a nonsensical stat type raises an error."""
    with pytest.raises(ValueError):
        HittingDF = ss.get_fangraphs_data('hittin',['2024'])
