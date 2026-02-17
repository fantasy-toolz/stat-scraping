
import numpy as np
import pandas as pd



def analyze_team_batting_order(year,team):
    PositionTotal = dict()
    TeamTotal = dict()
    PlrTeam = dict()
    D = np.genfromtxt('https://raw.githubusercontent.com/fantasy-toolz/batting-order/refs/heads/main/data/{}/{}.csv'.format(year,team),delimiter=',',dtype='S26',skip_header=1)   
    print('team: ',team,' games played: ',len(D[:,0]))   
    TeamTotal[team] = len(D[:,0])
    #print('date,lineup1,lineup2,lineup3,lineup4,lineup5,lineup6,lineup7,lineup8,lineup9,',file=f)  
    ngames = len(D[:,0])
    for n in range(1,ngames):
        for i in range(0,10):
            if i==0:
                # this is the date, so skip ahead
                pass
            else:
                try:
                    PositionTotal[D[n][i].decode().lstrip()][i-1] += 1
                except:
                    PositionTotal[D[n][i].decode().lstrip()] = np.zeros(9)
                    PositionTotal[D[n][i].decode().lstrip()][i-1] += 1
                    PlrTeam[D[n][i].decode().lstrip()] = team
    return PositionTotal#,PlrTeam,TeamTotal


#PositionTotal,PlrTeam,TeamTotal = analyze_team_batting_order(year,team)

def get_all_lineups(year):
    AllLineups = pd.read_csv('https://raw.githubusercontent.com/fantasy-toolz/batting-order/refs/heads/main/data/Aggregate/{}-all-lineups.csv'.format(year))
    return AllLineups

def get_team_lineup(year,team):
    AllLineups = get_all_lineups(year)
    TeamLineups = AllLineups[AllLineups['team']==team]
    return TeamLineups

def get_date_lineups(date):
    year = date.split('-')[0]
    AllLineups = get_all_lineups(year)
    DateLineups = AllLineups[AllLineups['date']==date]
    return DateLineups

def analyze_all_teams(year):
    """ # this is the manual solution: we now have a consolidated version
    teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'AZ', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']
    AllPlayers = dict()
    for team in teams:
        PositionTotal = analyze_team_batting_order(year,team)
        for player in PositionTotal.keys():
            try:
                AllPlayers[player] += PositionTotal[player]
            except:
                AllPlayers[player] = PositionTotal[player]
    return AllPlayers
    """
    if int(year) < 2021:
        raise ValueError('Year must be 2021 or later.')
    AllPlayers = pd.read_csv('https://raw.githubusercontent.com/fantasy-toolz/batting-order/refs/heads/main/data/Aggregate/Summaries/{}player-batting-order.csv'.format(year))
    return AllPlayers


def get_date_matchups(date,postfacto=False):
    year = date.split('-')[0]

    # first look to see if validation is available?

    if postfacto:
        valid = 'validation'
    else:
        valid = ''

    AllMatchups = pd.read_csv('https://raw.githubusercontent.com/fantasy-toolz/mlb-predictions/refs/heads/main/predictions/archive/{}/{}{}.csv'.format(year,date,valid))

    Matchups = AllMatchups[AllMatchups['date']==date]
    return Matchups