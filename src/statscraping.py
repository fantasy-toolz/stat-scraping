

from .fangraphs import fangraphsscraper as fgs
from .fantasypros import fantasyprosscraper as fps

def get_fangraphs_data(playertype,years):
    if playertype == 'hitting':
        df = fgs.grab_fangraphs_hitting_data(years)
    elif playertype == 'pitching':
        df = fgs.grab_fangraphs_pitching_data(years)
    return df


def get_fantasypros_projections(playertype,preseason=False):
    return fps.get_fantasy_pros_proj(playertype,preseason)

