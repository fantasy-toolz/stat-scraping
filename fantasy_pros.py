# -*- coding: utf-8 -*-
import re
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import os                       


### Create Eligibility DF
def get_eligibility(in_positions, in_player):
    # in_positions, in_player = position, row['PlayerTeamPosition']
    position_dict = {
        'RP': 0, 'C':0, '3B':0, '2B':0, 'SS':0, '1B':0, 'CF':0, 'LF':0, 'OF':0, 'DH':0, 'RF':0, 'SP':0
        }
    
    for i in in_positions:
        position_dict[i]= 1
        if i in ['RP', 'SP']:
            position_dict['pit'] = 1
        if i in ['C', '3B', '2B', 'SS', '1B', 'CF', 'LF', 'OF', 'DH', 'RF']:
            position_dict['bat'] = 1
        if i in ['CF', 'LF', 'RF', 'OF']:
            position_dict['OF'] = 1
            
    pos_df = pd.DataFrame(position_dict, index=[in_player])
    pos_df['PlayerTeamPosition'] = pos_df.index
    return pos_df

def create_overall_ranks_welig():
    url             = "https://www.fantasypros.com/mlb/rankings/{0}.php"
    r               = requests.get(url.format("overall"))
    soup            = BeautifulSoup(r.text, "html5lib")
    with open("output69.html", "w", encoding='utf-8') as file:
        file.write(str(soup))
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
    
    player_list = []
    positions = []
    for index, row in overall_ranks_df.iterrows():
        player, position = row['PlayerTeamPosition'].split("(")
        try:
            team, position = position.split("-")
        except:
            team = 'FreeAgent'
        
        player = player.rstrip()
        
        position = position.split(")")[0]
        position = position.replace(" ", "").split(",")
        play_elig_df = get_eligibility(position, row['PlayerTeamPosition'])
        player_row = [[row['PlayerTeamPosition'], player, team]]
    
        player_df = pd.DataFrame(player_row, columns=[ 'PlayerTeamPosition', 'Player', 'Team'])
        player_df = player_df.merge(play_elig_df, how = 'left', on = 'PlayerTeamPosition')    
    
        player_list.append(player_df)
    
    elig_df = player_list[0]
    for i in player_list[1:]:
        elig_df = pd.concat([elig_df, i])
    
    overall_ranks_df = overall_ranks_df.merge(elig_df, how='left', on='PlayerTeamPosition')
    overall_ranks_df = overall_ranks_df[[
        'Rank', 
        # 'PlayerTeamPosition', 
        'Player', 
        'Team', 
        'Best', 
        'Worst',
        'Avg',
        'StdDev', 
        'ADP',
        # 'vsADP', 
        # 'Notes', 
        'pit',
        'bat',
        'RP', 
        'C', 
        '3B', 
        '2B', 
        'SS', 
        '1B',
        # 'CF', 
        # 'LF', 
        'OF', 
        # 'DH', 
        # 'RF', 
        'SP']
        ]
    
    overall_ranks_df['bat'] = overall_ranks_df['bat'].fillna(0)
    overall_ranks_df['pit'] = overall_ranks_df['pit'].fillna(0)
    
    date_string = format(datetime.now().strftime('%Y%m%d'), "1")
    elig_csv_template = "fantasy_pros_ranks_elig_{}.csv"
    out_csv = os.path.join("data", elig_csv_template.format(date_string))
    overall_ranks_df.to_csv(out_csv , index = False)
    return overall_ranks_df

# overall_ranks_df = create_overall_ranks_welig()
# last_csv = os.path.join("data", elig_csv_template.format('20231218'))

# last_ranks_df = pd.read_csv(last_csv)
# last_ranks_df = last_ranks_df[['Rank', 'Player', 'pit', 'bat']]
# last_ranks_df.columns  = ['2023.Rank', 'Player', 'pit', 'bat']

# overall_ranks_df2 = overall_ranks_df.merge(last_ranks_df, on = ['Player', 'pit', 'bat'], how = 'left')
# overall_ranks_df2['2024.Rank'] = overall_ranks_df2['Rank'].astype(int)
# overall_ranks_df2['delta'] = overall_ranks_df2['2023.Rank'] - overall_ranks_df2['2024.Rank']

# out_csv = os.path.join("data", elig_csv_template.format(date_string+"_wlast"))
# overall_ranks_df2.to_csv(out_csv , index = False)
# overall_ranks_df.to_csv(out_csv , index = False)
