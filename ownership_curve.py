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

print("Start =",  datetime.now())

date_string = format(datetime.now().strftime('%Y%m%d'), "1")

hit_df = stat_scraping.get_fantasy_pros_proj(player_type = 'hitters')
pit_df = stat_scraping.get_fantasy_pros_proj(player_type = 'pitchers')

hit_df.to_csv('data/fp_proj_hit_{}.csv'.format(date_string), index = False)
pit_df.to_csv('data/fp_proj_pit_{}.csv'.format(date_string), index = False)

print("End =",  datetime.now())

working_directory       =   r'C:\Users\Erich\Documents\GitHub\ownership-modeling'

date_string                 =   format(datetime.datetime.now().strftime('%Y%m%d'), "1")
#last_week               = format((datetime.datetime.today() - timedelta(days=7)).strftime('%Y%m%d'), "1")
os.chdir(working_directory)
cbs_ownership_db            = "Data/CBS_ownership.csv"
cbs_startship_db                = "Data/CBS_startship.csv"



def UpdateCBSOwnershipDB():
    # Find all ownership data files by day
    data_files = os.listdir(os.path.join('data'))
    string_test = 'fp_proj_'
    ownership_csvs = []
    for data_file in data_files:
        if data_file[:14] == string_test:
            ownership_csvs.append(os.path.join(working_directory, 'Data',data_file))
    # Create a DataFrame for every day
    own_df_list = []
    for data_file in ownership_csvs:
        # Create DF
        df = pd.read_csv(data_file)    
        # Query DF
        df = df.loc[df[df.columns[2]]>0]
        # Add DF to list as Item
        own_df_list.append(df)    
    #
    #   Update Ownership CSV
    #
    # Create Ownership DataFrame remove extra fields
    own_df = own_df_list[0]
    own_df = own_df[own_df.columns[:3]]
    # Add each day of ownership to DataFrame
    for df in own_df_list[1:]:
        df = df[df.columns[:3]]
        own_df = own_df.merge(df, on = ['Player', 'Team'], how = 'outer')
    # Clean DataFrame by filling nulls with zeros 
    for column in own_df.columns[2:]:
        own_df[column] = own_df[column].fillna(0)
    # Save DataFrame to file
    own_df.to_csv(cbs_ownership_db.format(date_string), index=False)
    #
    #   Update Start CSV
    #
    # Create Start DataFrame remove extra fields
    start_df = own_df_list[0]
    column_list = list(start_df.columns[:2])
    column_list.append(start_df.columns[3])
    start_df = start_df[column_list]
    # For DF in List...
    for df in own_df_list[1:]:
        column_list = list(df.columns[:2])
        column_list.append(df.columns[3])
        df = df[column_list]
        start_df = start_df.merge(df, on = ['Player', 'Team'], how = 'outer')
    
    for column in start_df.columns[2:]:
        start_df[column] = start_df[column].fillna(0)
      # Save DataFrame to file
    start_df.to_csv(cbs_startship_db.format(date_string), index=False)   
    return own_df, start_df

def QueryPlayer(in_df, in_player):
    columns = in_df.columns[2:]
    days = []
    for column in columns:
        if column != 'Delta':# <---- make sure you add new columsn here
            days.append(column.split(".")[1])
            ownstart_type = column.split(".")[0]
    new_df = in_df.loc[in_df['Player'] == in_player]
    temp_list = list(new_df.iloc[0])
    # Transpose
    out_xy_list = []
    for day in range(0, len(days)):
        out_xy_list.append([days[day], temp_list[day+2]])
    out_df = pd.DataFrame(out_xy_list, columns=['Day', ownstart_type])
    out_df['Day'] = pd.to_datetime(out_df['Day'])
    return out_df 

def GraphPlayer(in_own_df, in_start_df, in_player):
    myFmt = mdates.DateFormatter('%m.%d')
    fig, ax = plt.subplots()
    ax.tick_params(
            axis='x',
            which='both',
            bottom='off',
            top='off')
    plt.xticks(rotation=35)
    plt.ylim((0, 100))
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
    plt.plot(playerDF['Day'], playerDF['Ownership'], '-', color= 'r', label = 'Ownership')
    plt.title('{0} Ownership Graph'.format(in_player))
    # Grab Start Data
    playerDF = QueryPlayer(in_start_df, in_player)
    plt.plot(playerDF['Day'], playerDF['Start'], dashes=[6, 2], color= 'gray', label = 'Startership')
    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2)  #(loc='lower left')
    return fig


#cbs_own_df = pd.read_csv("Data\CBS_ownership.csv")



# Main
own_df, start_df = UpdateCBSOwnershipDB()

#
## Mp Stuff
#mp_players = pd.read_csv("player_query.csv")
#
##cbs_own_df = own_df.loc[own_df['Player'].isin(mp_players['Player'])]
#
##cbs_own_df.to_csv("Data\CBS_ownership.csv", index = False)
#
#for player in mp_player1:
#     print player
#     player_own_df = own_df.loc[own_df['Player']== player]
#     player_start_df = start_df.loc[own_df['Player']== player]
#     GraphPlayer(player_own_df, player_start_df, player)
#
#
#mp_player1 = ['Albert Pujols', 'Luis Urias', 'Nathan Eovaldi', 'Ian Kinsler', 'Clay Buchholz', 'Cal Quantrill']