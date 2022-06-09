# -*- coding: utf-8 -*-
"""
Created on Mon Apr 08 20:58:29 2019
stat_scraping

@author: Erich Rentz
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

    

def scrape_fangraphs_leaders(stats_type, year = 2019, data_type = 'Standard', agg_type='Player'):
    '''
    Scrape baseball stats from Fangraphs
    :param str stats_type: The type of stat ('pit', 'bat', 'fld') being scraped
    :param str data_type: The fangraphs data table ("Dashboard", "Standard", "Advanced", "Batted Ball",
                                                    "Win Probability", "Pitch Type", "Pitch Value", "Plate Discipline",
                                                    "Value", "Pitch Info - Pitch Type", "Pitch Info - Velocity","Pitch Info - H-Movement", "Pitch Info - V-Movement",
                                                    "Pitch Info - Pitch Type Value", "Pitch Info - Pitch Type Value/100", "Pitch Info - Plate Discipline") 
    : param str agg_type: The aggregation level of stat being scraped ('Player', 'Team', 'League)
    :param int year: The year of the data being scraped
    :return: DataFrame of scraped data table
    ''' 
#    stats_type = 'bat'
#    data_type = 'Advanced'
#    agg_type = 'Player'
#    year = 2019
    data_type_dict = dict([
                ("Dashboard", 8),
                ("Standard", 0),
                ("Advanced", 1),
                ("Batted Ball", 2),
                ("Win Probability", 3),
                ("Pitch Type", 4),
                ("Pitch Value", 7),
                ("Plate Discipline", 5),
                ("Value", 6),
                ("Pitch Info - Pitch Type", 16),
                ("Pitch Info - Velocity", 17),
                ("Pitch Info - H-Movement", 18),
                ("Pitch Info - V-Movement", 19),
                ("Pitch Info - Pitch Type Value", 20),
                ("Pitch Info - Pitch Type Value/100", 21),
                ("Pitch Info - Plate Discipline", 22)
        ]
    )
    agg_type_dict = dict([
            ('Player', ''),
            ('Team', ',ts'),
            ('League', ',ss')
            ]
    )
    # Define the webpage of interest
    url             = "https://www.fangraphs.com/leaders.aspx?pos=all&stats={0}&lg=all&qual=0&type={1}&season={2}&month=0&season1={2}&ind=0&team=0{3}&rost=0&age=0&filter=&players=0&page=1_10000".format(stats_type, data_type_dict[data_type], year, agg_type_dict[agg_type])
    # Pull the information
    r               = requests.get(url.format(year))
    soup            = BeautifulSoup(r.content)
    table_data      = soup.find("table", { "class" : "rgMasterTable"})      
    # Grab table headers
    headers = [header.text for header in table_data.findAll('th')]
    # Grab all row type data into a list of lists
    rows = []
    for row in table_data.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) != 0:
            for td in row.findAll("td"):       
                sav2 = [td.getText() for td in row.findAll("td")] 
            rows.append(sav2)
    # Convert the List of Lists into a DataFrame
    df = pd.DataFrame(rows, columns=headers)
    # Query out non-value rows and set string column count for column formatting
    if agg_type == 'Player':
        df = df[df['Name'] == df['Name']]
        str_columns = 3
    elif agg_type == 'Team':
        df = df[df['Team'] == df['Team']]
        str_columns = 2
    else:
        df = df[df['Season'] == df['Season']]
        str_columns = 2
        
    # Cleanup field data stypes
    for column in df.columns[str_columns:]:
        try:
            df[column] = df[column].astype(float)
        except: 
            try: # if string has % sign
                df[column] = df[column].str[:-1]
                df[column] = df[column].astype(float)
            except: # if value is null
                df[column] = df[column].replace('&nbsp', np.nan)
                df[column] = df[column].replace('-', np.nan)
                df[column] = df[column].replace('', np.nan)
                df[column] = df[column].astype(float)
    # Fin
    return df

def update_statcast_player_id(player_type):
    '''
    Scrape baseball player ids from Statcast
    :param str player_type: The type of player ('pitcher', 'batter') being scraped
    :
    :return: null
    :action: overwrite player id dictionary csv
    :
    ''' 
    player_df = pd.DataFrame({'player_name' : ['nobody'], player_type : [-9999]})
    
    teams = [
            'LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL', 
            'CHC', 'ARI', 'LAD', 'SF', 'CLE', 'SEA', 'MIA', 
            'NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX', 
            'TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN', 
            'CWS', 'NYY'
            ]

    
    for team in teams:
    
        link = 'https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=&hfC=&hfSea=2019%7C&hfSit=&player_type={0}&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&team={1}&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name-event&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&min_abs=0&type=details&'.format(player_type, team)
        df = pd.read_csv(link, low_memory=False)
            
        df = df.groupby(['player_name'], as_index=False)[player_type].first()
        df['Team'] = team
        player_df = pd.concat([player_df, df])
        
    player_df = player_df.loc[(player_df['Team'] == player_df['Team'])]
    
    player_df.to_csv('{0}_dict.csv'.format(player_type), index = False)
    
def scrape_statcast_fromlist(in_list, player_type):
    '''
    Scrape baseball Statcast data for a list of players
    :param list in_list: A list of players (str) to be scraped
    :param str player_type: The type of player ('pitcher', 'batter') being scraped
    :
    :return: a dataframe with data for all players from in_list 
    :
    ''' 
    # Cleanup list to ensure no repeated players
    in_list = list(set(in_list))
    # Pick link type or throw warning
    if player_type == 'batter':
        print("Batter scraping pending")
        skip_scrape = True
    elif player_type == 'pitcher':
        link_template = 'https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C&hfSit=&player_type={0}&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&pitchers_lookup%5B%5D={1}&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=pitches&player_event_sort=h_launch_speed&sort_order=desc&min_abs=0&type=details&'
        skip_scrape = False
    else:
        print("Invalid 'player_type' choose between 'batter' and 'pitcher'")
        skip_scrape = True
    # If we made it through the player type warnings...
    if not skip_scrape:
        # Create Player Dictionary From CSV
        try:
            PlayerDict = {}
            player_df = pd.read_csv('{0}_dict.csv'.format(player_type))
            for indx,pname in enumerate(player_df.player_name):
                PlayerDict[pname] = player_df['{0}'.format(player_type)][indx]
        except:
            "Error: Importing Player ID data failed"
        # Grab data for each player from input list and shove into a list of dataframes
        bp_dfs = []
        for player in in_list:
            try:
                link = link_template.format(player_type, PlayerDict[player])
                df = pd.read_csv(link, low_memory=False)
                bp_dfs.append(df)
            except:
                print('Error: {0} is an invalid Player Name. Try updating player keys.'.format(player))
        # Combine all dataframes from list of dataframes
        output_df = bp_dfs[0]
        if len(bp_dfs) >1:
            for df in bp_dfs[1:]:
                output_df = pd.concat([output_df, df])
    return output_df


def get_fantasy_pros_proj(player_type = 'hitters'):
    '''
    Scrape Fantasy Pros data for rest of season projections and current roster%
    :
    :param str player_type: The type of player ('pitchers', 'hiters') being scraped
    :
    :return: a dataframe with data for all players
    :
    ''' 
    url = 'https://www.fantasypros.com/mlb/projections/ros-{}.php'
      
    r               = requests.get(url.format(player_type))
    soup            = BeautifulSoup(r.text, "html5lib")
    with open("output1.html", "w", encoding='utf-8') as file:
        file.write(str(soup))
    
    table_data      = soup.findAll("table")[0]
    headers = [re.sub(r'\W+', '', header.text) for header in table_data.findAll('th')]
    headers.extend(['Yahoo','ESPN', 'PlayerId'])
    rows = []
    for row in table_data.findAll("tr")[:1000]:
        player_str = str(row)
        player_id = player_str[:300].find('mpb-player-')
        player_id = player_str[player_id+11:player_id+18].replace('"', '').replace(">", '').replace('<','')
        # print(player_id, end = ", ")
        cells = row.findAll("td")
        if len(cells) != 0:
            for td in cells:
                sav2 = [td.getText() for td in row.findAll("td")] 
                sav2.append(player_id)
            rows.append(sav2)      
    
    # Convert to datframe
    df = pd.DataFrame(rows, columns=headers)
    df['Team'] = df['Player'].str.split('(').str[1]   
    df['Team'] = df['Team'].str.split('-').str[0] 
    df['Player'] = df['Player'].str.split('(').str[0]   
        
    # Cleanup field data stypes
    for column in df.columns:
        if column in ['Player', 'Team']:
            pass
        elif column in [ 'AB', 'R', 'HR', 'RBI', 'SB',  'H', '2B', '3B','BB', 'SO']:
           df[column] = df[column].astype(int)
        elif  column in [  'AVG', 'OBP', 'SLG', 'OPS']:
            df[column] = df[column].astype(float)
        elif  column in [  'Rost', 'Yahoo', 'ESPN']:
            df[column] = df[column].str[:-1]
            df[column] = np.where(df[column]=="",
                                  0,
                                  df[column])
            df[column] = df[column].astype(float)/100
            
    return df

def get_fantasy_pros_stats(player_type = 'hitters'):
    '''
    Scrape Fantasy Pros data for rest of season projections and current roster%
    :
    :param str player_type: The type of player ('pitchers', 'hiters') being scraped
    :
    :return: a dataframe with data for all players
    :
    ''' 
    url = 'https://www.fantasypros.com/mlb/stats/{}.php'
      
    r               = requests.get(url.format(player_type))
    soup            = BeautifulSoup(r.text, "html5lib")
    with open("output1.html", "w", encoding='utf-8') as file:
        file.write(str(soup))
    
    table_data      = soup.findAll("table")[0]
    headers = [re.sub(r'\W+', '', header.text) for header in table_data.findAll('th')]
    headers.extend(['Yahoo','ESPN', 'PlayerId'])
    rows = []
    for row in table_data.findAll("tr")[:1000]:
        player_str = str(row)
        player_id = player_str[:300].find('mpb-player-')
        player_id = player_str[player_id+11:player_id+18].replace('"', '').replace(">", '').replace('<','')
        # print(player_id, end = ", ")
        cells = row.findAll("td")
        if len(cells) != 0:
            for td in cells:
                sav2 = [td.getText() for td in row.findAll("td")] 
                sav2.append(player_id)
            rows.append(sav2)      
    
    # Convert to datframe
    df = pd.DataFrame(rows, columns=headers)
    df['Team'] = df['Player'].str.split('(').str[1]   
    df['Team'] = df['Team'].str.split('-').str[0] 
    df['Player'] = df['Player'].str.split('(').str[0]   
        
    # Cleanup field data stypes
    for column in df.columns:
        if column in ['Player', 'Team']:
            pass
        elif column in [ 'AB', 'R', 'HR', 'RBI', 'SB',  'H', '2B', '3B','BB', 'SO']:
           df[column] = df[column].astype(int)
        elif  column in [  'AVG', 'OBP', 'SLG', 'OPS']:
            df[column] = df[column].astype(float)
        elif  column in [  'Rost', 'Yahoo', 'ESPN']:
            df[column] = df[column].str[:-1]
            df[column] = np.where(df[column]=="",
                                  0,
                                  df[column])
            df[column] = df[column].astype(float)/100
            
    return df



    