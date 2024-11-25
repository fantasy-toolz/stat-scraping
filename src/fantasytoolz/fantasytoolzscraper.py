
import numpy as np


teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'AZ', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']


# create a dictionary



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


