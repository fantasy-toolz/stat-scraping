# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 08:16:50 2023

@author: rentz
"""

# standard imports
import numpy as np
import os

# scraping tools
import requests
from bs4 import BeautifulSoup

# data management tools
import pandas as pd

def scrape_year(year='2019',cat='pit',verbose=0,date1='2019-03-20',date2='2019-10-30'):
    '''

    scrape the total, season-long player data

    inputs
    ---------
    year    : string of the year to query
    cat     : 'bat' or 'pit' for batting or pitching statistics
    verbose : level of reporting. 0=none.

    returns
    ---------
    PDict
    NDict
    NDict2
    TDict

    todo
    ---------
    -change internal nomenclature to be sensical
    -check table query number


    '''


    year_url      =   "https://www.fangraphs.com/leaders.aspx?pos=all&stats="+str(cat)+\
                      "&lg=all&qual=0&type=0&season="+str(year)+\
                      "&month=1000&season1="+str(year)+\
                      "&ind=0&team=0&rost=0&age=0&filter=&players=0&page=1_1200"+\
                      "&startdate="+date1+"&enddate="+date2

    if verbose: print('The year is {}'.format(year))
    print(year_url)

    # perform the lookup
    r               = requests.get(year_url)

    # old compatibility version: save which checking
    #soup            = BeautifulSoup(r.content, "html5lib")

    soup            = BeautifulSoup(r.text, "html5lib")

    # identify the master table
    table_data      = soup.find("table", { "class" : "rgMasterTable"})

    # populate header values
    headers = [header.text for header in table_data.findAll('th')]

    # cycle through all rows in the table
    rows = []
    for row in table_data.findAll("tr")[3:]:
        cells = row.findAll("td")
        if len(cells) != 0:
            for td in row.findAll("td"):
                sav2 = [td.getText() for td in row.findAll("td")]
            rows.append(sav2)

    # transform to a pandas table
    df = pd.DataFrame(rows, columns=headers)
    df['Year'] = year

    # return the dataframe
    return df


df_2022 = scrape_year(year='2022',cat='bat',verbose=0,date1='2022-03-20',date2='2022-06-19')
df_2022['SB'] = df_2022['SB'].astype(float)
df_2022['PA'] = df_2022['PA'].astype(float)
df_2022['1B'] = df_2022['1B'].astype(float)
df_2022 = df_2022.loc[df_2022['PA']>0]
print("Sum of 2022 SB by 6/19: " + str(int(df_2022['SB'].sum())))
print("Max of 2022 SB by 6/19: " + str(int(df_2022['SB'].max())))
print(list(df_2022.loc[df_2022['SB'] == df_2022['SB'].max()]['Name']))
print("Med of 2022 SB by 6/19: " + str(int(df_2022['SB'].median())))
print(list(df_2022.loc[df_2022['SB'] == df_2022['SB'].median()]['Name']))
df_2022.hist(column='SB')
df_2022 = df_2022.loc[df_2022['PA']>30]
col1, col2 = "PA", "SB"
corr = df_2022[col1].corr(df_2022[col2])
print("2022 Correlation between ", col1, " and ", col2, "is: ", round(corr, 2))

col1, col2 = "1B", "SB"
df_2022 = df_2022.loc[df_2022['PA']>30]
corr = df_2022[col1].corr(df_2022[col2])
print("2022 Correlation between ", col1, " and ", col2, "is: ", round(corr, 2))


df_2023 = scrape_year(year='2023',cat='bat',verbose=0,date1='2023-03-20',date2='2023-06-19')
df_2023['SB'] = df_2023['SB'].astype(float)
df_2023['PA'] = df_2023['PA'].astype(float)
df_2023['1B'] = df_2023['1B'].astype(float)
df_2023['HR'] = df_2023['HR'].astype(float)
df_2023 = df_2023.loc[df_2023['PA']>0]
print("Sum of 2023 SB by 6/19: " + str(int(df_2023['SB'].sum())))
print("Max of 2023 SB by 6/19: " + str(int(df_2023['SB'].max())))
print(list(df_2023.loc[df_2023['SB'] == df_2023['SB'].max()]['Name']))
print("Med of 2023 SB by 6/19: " + str(int(df_2023['SB'].median())))
print(list(df_2023.loc[df_2023['SB'] == df_2023['SB'].median()]['Name']))
df_2023.hist(column='SB')
col1, col2 = "PA", "SB"
df_2023 = df_2023.loc[df_2023['PA']>30]
corr = df_2023[col1].corr(df_2023[col2])
print("2023 Correlation between ", col1, " and ", col2, "is: ", round(corr, 2))

col1, col2 = "HR", "SB"
df_2023 = df_2023.loc[df_2023['PA']>30]
corr = df_2023[col1].corr(df_2023[col2])
print("2023 Correlation between ", col1, " and ", col2, "is: ", round(corr, 2))

# if __name__ == "__main__":
#     # go week by week to get stats

#     # in 2021, the first Sunday is 87: you will need to adjust this for other years
#     yr = 2021
#     sun = 87
#     for week in range(0,26):
#         week = 26
#         # dfs =[]
#         for play_typ in ('bat', 'pit'):
        
#             dayval = pd.to_datetime((sun+7*week), unit='D', origin=str(yr))
#             dayval1 = str(dayval).split()[0]
#             dayval = pd.to_datetime((sun+7*week)+6, unit='D', origin=str(yr))
#             dayval2 = str(dayval).split()[0]
#             print(dayval1,dayval2)
    
#             df = scrape_year(year=yr,cat=play_typ,verbose=0,date1=dayval1,date2=dayval2)
#             df['PlayerType'] = play_typ
#             # dfs.append(df)
#             # df = pd.concat(dfs)
#             df.to_csv('data/{0}_week{1}_{2}.csv'.format(play_typ, week, yr))