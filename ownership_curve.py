# -*- coding: utf-8 -*-
"""


@author: Erich Rentz
"""

import stat_scraping 
from datetime import datetime
from datetime import timedelta
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from PIL import Image

date_string     = format(datetime.now().strftime('%Y%m%d'), "1")
ownership_db            = "data/ownership.csv"
last_week               = format((datetime.today() - timedelta(days=7)).strftime('%Y%m%d'), "1")

def UpdateOwnershipDB():
    data_file = "data/fp_proj_{0}_{1}.csv"
    # Grab New Data
    hit_df = stat_scraping.get_fantasy_pros_proj(player_type = 'hitters')
    pit_df = stat_scraping.get_fantasy_pros_proj(player_type = 'pitchers')
    hit_df.to_csv(data_file.format('hit', date_string), index = False)
    pit_df.to_csv(data_file.format('pit', date_string), index = False)
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
    ownership_csvs = list(set(ownership_dict.keys()))
    ownership_csvs.sort()
    # Create a DataFrame for every day
    own_df_list = []
    
    for data_date in ownership_csvs:
        # print(data_date)
        # Create DFs
        dfHit = pd.read_csv(data_file.format('hit', data_date))  
        dfHit =dfHit.groupby(['Player', 'PlayerId'], as_index = False).max()
        # dfHit = dfHit.loc[~(dfHit['PlayerId'].isin([4976, 7354,7812]))]
        dfPit = pd.read_csv(data_file.format('pit', data_date))
        dfPit = dfPit.groupby(['Player', 'PlayerId'], as_index = False).max()
        # dfPit = dfPit.loc[~(dfPit['PlayerId'].isin([,7812]))]
        # Concat Hit and Pit
        df = pd.concat([dfHit, dfPit])
        df = df.groupby(['Player', 'PlayerId'], as_index = False).max()
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
    
    # own_df_test = own_df.groupby(['Player', 'PlayerId'], as_index = False)['Team'].count()
    
    # Clean DataFrame by filling nulls with zeros 
    for column in own_df.columns[3:]:
        own_df[column] = own_df[column].fillna(0)
    own_df = own_df.loc[own_df['Player']==own_df['Player']]
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
    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2)  #(loc='lower left')
    return fig

# data_file = "data/fp_proj_{0}_{1}.csv"
# hit_stats = stat_scraping.get_fantasy_pros_stats(player_type = 'hitters')
# dfHit = pd.read_csv(data_file.format('hit', date_string))   
# dfHit_pre = pd.read_csv(data_file.format('hit', '20220519')) 

# def lim_hit_scope(in_df):
#     in_df['R+RBI'] = in_df['R'] + in_df['RBI']   
#     in_df['HR+SB'] = in_df['HR'] + in_df['SB']   
#     in_df = in_df[['Player', 'PlayerId', 'R+RBI', 'HR+SB', 'H', 'Rost' ]]
#     return in_df

# dfHit = lim_hit_scope(dfHit)
# hit_stats = lim_hit_scope(hit_stats)
# hit_stats['PlayerId'] = hit_stats['PlayerId'].astype(int)
# dfHit_pre = lim_hit_scope(dfHit_pre)

# dfHit = pd.concat([dfHit, hit_stats])
# dfHit = dfHit.groupby(['Player', 'PlayerId'], as_index = False).sum()
# dfHit = dfHit.merge(dfHit_pre, how= 'left', on = ['Player', 'PlayerId'])
# dfHit = dfHit.loc[dfHit['Rost_y']==dfHit['Rost_y']]

# interesting_plus = []
# for i in ['R+RBI_', 'HR+SB_', 'H_']:
#     dfHit[i+'Delta'] = dfHit[i+'x'] - dfHit[i+'y']
#     dfHit = dfHit.sort_values(by = [i+'Delta'])
#     highest_climbers = list(dfHit[-5:]['Player'])
#     interesting_plus.extend(highest_climbers)

# interesting_plus = list(set(interesting_plus))

# dfHit_interesting = dfHit.loc[dfHit['Player'].isin(interesting_plus)]

# highest_climbers = list(own_df_sort[-10:]['Player'])
# biggest_fallers = list(own_df_sort[:10]['Player'])


# Main
# own_df = UpdateOwnershipDB()

# # mp_player1 = ['Albert Pujols ', 'Luis Urias ', 'Nathan Eovaldi ', 'Cal Quantrill ']
# # for player in mp_player1:
# #      print(player)
# #      player_own_df = own_df.loc[own_df['Player']== player]
# #      GraphPlayer(player_own_df, player)

# ## Identify  biggest movers in previous week
# ##
# own_df['Delta'] = own_df['Own.{0}'.format(date_string)] - own_df['Own.{0}'.format(last_week)]
# own_df_sort = own_df.sort_values(by = ['Delta'])
# highest_climbers = list(own_df_sort[-10:]['Player'])
# biggest_fallers = list(own_df_sort[:10]['Player'])

# graphs = []
# for player in highest_climbers:
#     GraphPlayer(own_df, player)
#     new_graph = 'graphs/{}.png'.format(player)
#     plt.savefig(new_graph)
#     im1 = Image.open(new_graph)
#     graphs.append(im1)
#     print(player, end = ", ")
    
    
def get_concat_h(image_list):
    dst = Image.new('RGB', (image_list[0].width*2, image_list[0].height *3))
    dst.paste(image_list[0], (0, 0))
    dst.paste(image_list[1], (image_list[0].width, 0))
    dst.paste(image_list[2], (0, image_list[0].height))
    dst.paste(image_list[3], (image_list[0].width, image_list[0].height))
    dst.paste(image_list[4], (0, image_list[0].height*2))
    dst.paste(image_list[5], (image_list[0].width, image_list[0].height*2))
    return dst

# get_concat_h(graphs).save('graphs/pillow_test.jpg')

    
# for player in biggest_fallers:
#     GraphPlayer(own_df, player)
#     print(player, end = ", ")
# #
# #own_df_98 = own_df.loc[own_df['Ownership.{0}'.format('20180601')]==98]


# print("End =",  datetime.now())

#

# for player in interesting_plus:
#     GraphPlayer(own_df, player)
#     print(player, end = ", ")