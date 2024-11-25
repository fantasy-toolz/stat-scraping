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



def get_fantasy_pros_proj(player_type = 'hitters', preseason = False):
    '''
    Scrape Fantasy Pros data for rest of season projections and current roster%
    :
    :param str player_type: The type of player ('pitchers', 'hiters') being scraped
    :
    :return: a dataframe with data for all players
    :
    '''
    # player_type, preseason = 'hitters', False
    url = 'https://www.fantasypros.com/mlb/projections/ros-{}.php'
    if preseason:
       url = 'https://www.fantasypros.com/mlb/projections/{}.php'

    r               = requests.get(url.format(player_type))
    soup            = BeautifulSoup(r.text, "html5lib")
    with open("output1.html", "w", encoding='utf-8') as file:
        file.write(str(soup))

    table_data      = soup.findAll("table")[0]
    headers = [re.sub(r'\W+', '', header.text) for header in table_data.findAll('th')]
    if not preseason:
        headers.extend(['Yahoo','ESPN'])
    headers.append('PlayerId')
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

def get_fantasy_pros_rank():
    '''
    Scrape Fantasy Pros data for rest of season projections and current roster%
    :
    :param str player_type: The type of player ('pitchers', 'hiters') being scraped
    :
    :return: a dataframe with data for all players
    :
    '''
    #player_type, preseason = 'hitters', True
    url = 'https://www.fantasypros.com/mlb/rankings/overall.php'

    r               = requests.get(url)
    soup            = BeautifulSoup(r.text, "html5lib")
    with open("output1.html", "w", encoding='utf-8') as file:
        file.write(str(soup))

    table_data      = soup.findAll("table")[0]
    headers = [re.sub(r'\W+', '', header.text) for header in table_data.findAll('th')]
    # if not preseason:
    #     headers.extend(['Yahoo','ESPN'])
    headers.append('PlayerId')
    rows = []
    for row in table_data.findAll("tr")[:1000]:
        player_str = str(row)
        player_id = player_str[:300].find('mpb-player-')
        player_id = player_str[player_id+11:player_id+16].replace('"', '').replace(">", '').replace('<','')
        # print(player_id, end = ", ")
        cells = row.findAll("td")
        if len(cells) != 0:
            for td in cells:
                sav2 = [td.getText() for td in row.findAll("td")]
                sav2.append(player_id)
            rows.append(sav2)

    # Convert to datframe
    df = pd.DataFrame(rows, columns=headers)
    df['Team'] = df['PlayerTeamPosition'].str.split('(').str[1]
    df['Team'] = df['Team'].str.split('-').str[0]
    df['Player'] = df['PlayerTeamPosition'].str.split('(').str[0]


    return df
