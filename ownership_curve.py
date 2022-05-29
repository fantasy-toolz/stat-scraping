# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 12:28:50 2018

@author: Erich Rentz
"""

#import requests
import stat_scraping 
from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

print("Start =",  datetime.now())

date_string     = format(datetime.now().strftime('%Y%m%d'), "1")
ownership_db            = "data/ownership.csv"

def UpdateOwnershipDB():
    data_file = "data/fp_proj_{0}_{1}.csv"
    # Grab New Data
#    hit_df = stat_scraping.get_fantasy_pros_proj(player_type = 'hitters')
#    pit_df = stat_scraping.get_fantasy_pros_proj(player_type = 'pitchers')
#    hit_df.to_csv(data_file.format('hit', date_string), index = False)
#    pit_df.to_csv(data_file.format('pit', date_string), index = False)
    # Find all ownership data files by day
    data_files = os.listdir(os.path.join('data'))
    ownership_dict = {}
    for data_f in data_files:
        if data_f[:8] == data_file[5:13]:
            try:
                cur_csv = ownership_dict[data_f[-12:-4]]
                ownership_dict[int(data_f[-12:-4])] = [cur_csv, data_f]
            except:
                ownership_dict[int(data_f[-12:-4])] = data_f
    ownership_csvs = set(ownership_dict.keys())
    # Create a DataFrame for every day
    own_df_list = []
    
    for data_date in ownership_csvs:
        # Create DFs
        dfHit = pd.read_csv(data_file.format('hit', data_date))   
        dfPit = pd.read_csv(data_file.format('pit', data_date))
        # Concat Hit and Pit
        df = pd.concat([dfHit, dfPit])
        # Get Columns formatted
        df.rename(columns={'Rost':'Own.'+str(data_date)}, inplace=True)
        df = df[['Player', 'Team', 'PlayerId', 'Own.'+str(data_date)]]
        own_df_list.append(df)    
    #
    #   Update Ownership CSV
    #
    # Create Ownership DataFrame remove extra fields
    own_df = own_df_list[0]
    # Add each day of ownership to DataFrame
    for df in own_df_list[1:]:
        df = df[df.columns[2:]]
        own_df = own_df.merge(df, on = ['PlayerId'], how = 'outer')
    # Clean DataFrame by filling nulls with zeros 
    for column in own_df.columns[3:]:
        own_df[column] = own_df[column].fillna(0)

    own_df.to_csv(ownership_db.format(date_string), index=False)

    return own_df

def QueryPlayer(in_df, in_player):
#    in_df, in_player = player_own_df, player
    days = []
    for column in in_df.columns[3:]:
        if column != 'Delta':# <---- make sure you add new columsn here
            days.append(column.split(".")[1])
            ownstart_type = column.split(".")[0]
    new_df = in_df.loc[in_df['Player'] == in_player]
    temp_list = list(new_df.iloc[0])
    # Transpose
    out_xy_list = []
    for day in range(0, len(days)):
        out_xy_list.append([days[day], temp_list[day+3]])
    out_df = pd.DataFrame(out_xy_list, columns=['Day', ownstart_type])
    out_df['Day'] = pd.to_datetime(out_df['Day'])
    return out_df 

def GraphPlayer(in_own_df, in_player):
#    in_own_df, in_player = player_own_df, player
    myFmt = mdates.DateFormatter('%m.%d')
    fig, ax = plt.subplots()
    ax.tick_params(
            axis='x',
            which='both',
            bottom='off',
            top='off')
    plt.xticks(rotation=35)
    plt.ylim((0, 1))
    plt.xlabel("Day")
    plt.ylabel("%")
    plt.tick_params(
            axis='y',
            which='both',
            left='off',
            right='off')
    ax.xaxis.set_major_formatter(myFmt)
    # Grab Ownership Data
    playerDF = QueryPlayer(in_own_df, in_player)
    plt.plot(playerDF['Day'], playerDF['Own'], '-', color= 'r', label = 'Ownership')
    plt.title('{0} Ownership Graph'.format(in_player))
    # Grab Start Data
#    playerDF = QueryPlayer(in_start_df, in_player)
#    plt.plot(playerDF['Day'], playerDF['Start'], dashes=[6, 2], color= 'gray', label = 'Startership')
    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2)  #(loc='lower left')
    return fig


# Main
own_df = UpdateOwnershipDB()

mp_player1 = ['Albert Pujols ', 'Luis Urias ', 'Nathan Eovaldi ', 'Cal Quantrill ']
for player in mp_player1:
     print(player)
     player_own_df = own_df.loc[own_df['Player']== player]
     GraphPlayer(player_own_df, player)

## Identify  biggest movers in previous week
##
#try:
#    own_df['Delta'] = own_df['Ownership.{0}'.format(date_string)] - own_df['Ownership.{0}'.format(last_week)]
#except:
#    own_df['Delta'] = own_df['Ownership.{0}'.format(date_string)] - own_df['Ownership.{0}'.format(last_week)]
#own_df_sort = own_df.sort_values(by = ['Delta'])
#highest_climbers = list(own_df_sort[-10:]['Player'])
#biggest_fallers = list(own_df_sort[:10]['Player'])
#
#for player in highest_climbers:
#    GraphPlayer(own_df, start_df, player)
#    
#for player in biggest_fallers:
#    GraphPlayer(own_df, start_df, player)
#
#own_df_98 = own_df.loc[own_df['Ownership.{0}'.format('20180601')]==98]


print("End =",  datetime.now())

#last_week               = format((datetime.datetime.today() - timedelta(days=7)).strftime('%Y%m%d'), "1")

