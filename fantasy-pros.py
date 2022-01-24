# -*- coding: utf-8 -*-
import re
import pandas as pd
from bs4 import BeautifulSoup
import requests
                            
url             = "https://www.fantasypros.com/mlb/rankings/{0}.php"
r               = requests.get(url.format("overall"))
soup            = BeautifulSoup(r.text, "html5lib")
# with open("output1.html", "w", encoding='utf-8') as file:
#     file.write(str(soup))
table_data      = soup.find("table", { "class" : "table table-bordered table-condensed player-table table-striped table-hover"})
headers = [re.sub(r'\W+', '', header.text) for header in table_data.findAll('th')]

rows = []
for row in table_data.findAll("tr"):
    cells = row.findAll("td")
    if len(cells) != 0:
        for td in row.findAll("td"):       
            sav2 = [td.getText() for td in row.findAll("td")] 
        rows.append(sav2)      
        
# Create DF from overall rankings
overall_ranks_df = pd.DataFrame(rows, columns=headers)

def get_eligibility(in_positions, in_player):
    in_positions, in_player = position, row['PlayerTeamPosition']
    position_dict = {
        'RP': 0, 'C':0, '3B':0, '2B':0, 'SS':0, '1B':0, 'CF':0, 'LF':0, 'OF':0, 'DH':0, 'RF':0, 'SP':0
        }
    
    for i in in_positions:
        position_dict[i]= 1
    pos_df = pd.DataFrame(position_dict, index=[in_player])
    pos_df['PlayerTeamPosition'] = pos_df.index
    return pos_df

player_list = []
positions = []
for index, row in overall_ranks_df.iterrows():
    player, position = row['PlayerTeamPosition'].split("(")
    try:
        team, position = position.split("-")
    except:
        # print(player)
        team = 'FreeAgent'
    
    player = player.rstrip()
    
    position = position.split(")")[0]
    position = position.replace(" ", "").split(",")
    play_elig_df = get_eligibility(position, row['PlayerTeamPosition'])
    player_row = [[row['PlayerTeamPosition'], player, team]]

    player_df = pd.DataFrame(player_row, columns=[ 'PlayerTeamPosition', 'Player', 'Team'])
    player_df = player_df.merge(play_elig_df, how = 'left', on = 'PlayerTeamPosition')    

    player_list.append(player_df)
    # positions.extend(position)
# positions = list(set(positions))

elig_df = player_list[0]
for i in player_list[1:]:
    elig_df = pd.concat([elig_df, i])






