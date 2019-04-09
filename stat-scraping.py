# -*- coding: utf-8 -*-
"""
Created on Mon Apr 08 20:58:29 2019
stat-scraping

@author: Erich Rentz
"""

import requests
from BeautifulSoup import BeautifulSoup
import pandas as pd
import numpy as np
    

def scrape_fangraphs_leaders(stats_type, year = 2019, data_type = 'Dashboard', agg_type='Player'):
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


df = scrape_fangraphs_leaders('bat', data_type = 'Advanced')










    