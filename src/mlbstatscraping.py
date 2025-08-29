

from fangraphs import fangraphsscraper as fgs
from fantasypros import fantasyprosscraper as fps
from fantasytoolz import fantasytoolzscraper as fts

def get_fangraphs_data(playertype, years, daystart='', dayend=''):
    # Validate playertype
    if playertype not in {'hitting', 'pitching'}:
        raise ValueError("Invalid playertype. Must be 'hitting' or 'pitching'.")
    
    # Validate daystart year matches years
    if daystart:
        try:
            daystart_year = daystart.split('-')[0]  # Extract year from daystart
        except (ValueError, IndexError):
            raise ValueError("daystart must be in the format 'YYYY-MM-DD'.")
        
        if daystart_year not in years:
            raise ValueError(f"daystart year ({daystart_year}) does not match years ({years}).")
    
    # Fetch data based on playertype
    if playertype == 'hitting':
        df = fgs.grab_fangraphs_hitting_data(years, daystart, dayend)
    elif playertype == 'pitching':
        df = fgs.grab_fangraphs_pitching_data(years, daystart, dayend)
    
    return df



def get_fantasypros_projections(playertype,preseason=False):
    return fps.get_fantasy_pros_proj(playertype,preseason)


#def get_fantasypros_ranks():
#    return fps.get_fantasy_pros_rank()

"""
Fantasy Toolz block
"""

def get_fantasytoolz_lineups(team,year=2024):
    if int(year)<2021:
        raise ValueError('Year must be 2021 or later.') 
    return fts.analyze_team_batting_order(year,team)


def get_fantasytoolz_lineup_summary(year):
    if int(year)<2021:
        raise ValueError('Year must be 2021 or later.') 
    return fts.analyze_all_teams(year)


def get_fantasytoolz_date_lineups(date):
    return fts.get_date_lineups(date)

def get_fantasytoolz_team_lineup(year,team):
    return fts.get_team_lineup(year,team)

def get_fantasytoolz_all_lineups(year):
    return fts.get_all_lineups(year)

def get_fantasytoolz_date_matchups(date):
    return fts.get_date_matchups(date)