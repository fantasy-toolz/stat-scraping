

from .fangraphs import fangraphsscraper as fgs
from .fantasypros import fantasyprosscraper as fps
from .fantasytoolz import fantasytoolzscraper as fts

def get_fangraphs_data(playertype,years):
    if playertype == 'hitting':
        df = fgs.grab_fangraphs_hitting_data(years)
    elif playertype == 'pitching':
        df = fgs.grab_fangraphs_pitching_data(years)
    return df


def get_fantasypros_projections(playertype,preseason=False):
    return fps.get_fantasy_pros_proj(playertype,preseason)


def get_fantasytoolz_lineups(team,year='2024'):
    if int(year)<2023:
        raise ValueError('Year must be 2023 or later.') 
    return fts.analyze_team_batting_order(year,team)


def get_alllineupes(year):
    if int(year)<2023:
        raise ValueError('Year must be 2023 or later.') 
    return fts.analyze_all_teams('2024')