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

def scrape_year(year='2019',cat='pit',verbose=0,date1='2019-03-20',date2='2019-10-30', stat_typ = 0):
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
                      "&lg=all&qual=0&type={}&season=".format(stat_typ)+str(year)+\
                      "&month=1000&season1="+str(year)+\
                      "&ind=0&team=0&rost=0&age=0&filter=&players=0&page=1_1200"+\
                      "&startdate="+date1+"&enddate="+date2
    if verbose: print('The year is {}'.format(year))
    # print(year_url)

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


df_2019_stand = scrape_year(year='2019',cat='pit',verbose=0,date1='2019-03-20',date2='2019-08-14')
df_2019 = scrape_year(year='2019',cat='pit',verbose=0,date1='2019-03-20',date2='2019-08-14', stat_typ = 1)
cols = list(df_2019.columns)
cols.remove('Name')
cols.remove('Team')
df_2019 = df_2019.loc[~df_2019['Name'].isin(['Andrew Vasquez', 'Gerardo Parra'])]
for col in cols:
    try:
        df_2019[col] = df_2019[col].astype(float)
    except:
        df_2019[col] = df_2019[col].str[:-1].astype(float)
    
stand_cols = ['G', 'GS', 'W', 'IP', 'SO']
for col in ['G', 'GS', 'W', 'IP', 'SO']:
    df_2019_stand[col] = df_2019_stand[col].astype(float)

stand_cols.extend(['Name', 'Team'])       
df_2019 = df_2019.merge(df_2019_stand[stand_cols])
df_2019 = df_2019.loc[(df_2019['G']<df_2019['GS']+2)&(df_2019['G']>5)]

# df_2019 = df_2019.loc[(df_2019['SV']+df_2019['BS']+df_2019['HLD'])>0]

print("Count of eligible pitchers: " + str(len(df_2019)))
print("Sum of eligible ip: " + str(int(df_2019['IP'].sum())))
print("Sum of 2019 K by 8/14: " + str(int(df_2019['SO'].sum())))
print("Total K/9 by 8/14: " +  str(9*df_2019['SO'].sum()/int(df_2019['IP'].sum())))
print("Max of 2019 K by 8/14: " + str(int(df_2019['SO'].max())))
print(list(df_2019.loc[df_2019['SO'] == df_2019['SO'].max()]['Name']))
print("Med of 2019 K by 8/14: " + str(int(df_2019['SO'].median())))
print("Mean of 2019 K by 8/14: " + str(int(df_2019['SO'].mean())))
# print(list(df_2019.loc[df_2019['SB'] == df_2019['SB'].median()]['Name']))
# df_2019.hist(column='SB')
col1s = ["ERA", 'W', 'xFIP', 'FIP', 'SIERA', 'IP']
col2 = 'SO'
top5_2019 = []
for col1 in col1s:
    print(col1)
    corr = df_2019[col1].corr(df_2019[col2])
    print("2019 Correlation between ", col1, " and ", col2, "is: ", round(corr, 2))
    if col1 in ['W', 'IP']:
        df_2019 = df_2019.sort_values(by=[col1], ascending=False)
    else:
        df_2019 = df_2019.sort_values(by=[col1])
    top_5 = list(df_2019['Name'][:5])
    print(top_5)
    top5_2019.extend(top_5)
top5_2019 = list(set(top5_2019))


df_2022_stand = scrape_year(year='2022',cat='pit',verbose=0,date1='2022-03-20',date2='2022-08-14')
df_2022 = scrape_year(year='2022',cat='pit',verbose=0,date1='2022-03-20',date2='2022-08-14', stat_typ = 1)
cols = list(df_2022.columns)
cols.remove('Name')
cols.remove('Team')
for col in cols:
    try:
        df_2022[col] = df_2022[col].astype(float)
    except:
        df_2022[col] = df_2022[col].str[:-1].astype(float)
    
stand_cols = ['G', 'GS', 'W', 'IP', 'SO']
for col in ['G', 'GS', 'W', 'IP', 'SO']:
    df_2022_stand[col] = df_2022_stand[col].astype(float)

stand_cols.extend(['Name', 'Team'])       
df_2022 = df_2022.merge(df_2022_stand[stand_cols])
df_2022 = df_2022.loc[(df_2022['G']<df_2022['GS']+2)&(df_2022['G']>5)]
# df_2022 = df_2022.loc[(df_2022['SV']+df_2022['BS']+df_2022['HLD'])>0]

print("Count of eligible pitchers: " + str(len(df_2022)))
print("Sum of eligible ip: " + str(int(df_2022['IP'].sum())))
print("Sum of 2022 K by 8/14: " + str(int(df_2022['SO'].sum())))
print("Total K/9 by 8/14: " +  str(9*df_2022['SO'].sum()/int(df_2022['IP'].sum())))
print("Max of 2022 K by 8/14: " + str(int(df_2022['SO'].max())))
print(list(df_2022.loc[df_2022['SO'] == df_2022['SO'].max()]['Name']))
print("Med of 2022 K by 8/14: " + str(int(df_2022['SO'].median())))
print("Mean of 2022 K by 8/14: " + str(int(df_2022['SO'].mean())))
# print(list(df_2022.loc[df_2022['SB'] == df_2022['SB'].median()]['Name']))
# df_2022.hist(column='SB')
col1s = ["ERA", 'W', 'xFIP', 'FIP', 'SIERA', 'IP']
col2 = 'SO'
top5_2022 = []
for col1 in col1s:
    print(col1)
    corr = df_2022[col1].corr(df_2022[col2])
    print("2022 Correlation between ", col1, " and ", col2, "is: ", round(corr, 2))
    if col1 in ['W', 'IP']:
        df_2022 = df_2022.sort_values(by=[col1], ascending=False)
    else:
        df_2022 = df_2022.sort_values(by=[col1])
    top_5 = list(df_2022['Name'][:5])
    print(top_5)
    top5_2022.extend(top_5)
top5_2022 = list(set(top5_2022))


df_2023_stand = scrape_year(year='2023',cat='pit',verbose=0,date1='2023-03-20',date2='2023-08-14')
df_2023 = scrape_year(year='2023',cat='pit',verbose=0,date1='2023-03-20',date2='2023-08-14', stat_typ = 1)
cols = list(df_2023.columns)
cols.remove('Name')
cols.remove('Team')
for col in cols:
    try:
        df_2023[col] = df_2023[col].astype(float)
    except:
        df_2023[col] = df_2023[col].str[:-1].astype(float)
    
stand_cols = ['G', 'GS', 'W', 'IP', 'SO']
for col in ['G', 'GS', 'W', 'IP', 'SO']:
    df_2023_stand[col] = df_2023_stand[col].astype(float)

stand_cols.extend(['Name', 'Team'])       
df_2023 = df_2023.merge(df_2023_stand[stand_cols])
df_2023 = df_2023.loc[(df_2023['G']<df_2023['GS']+2)&(df_2023['G']>5)]
# df_2023 = df_2023.loc[(df_2023['SV']+df_2023['BS']+df_2023['HLD'])>0]

print("Count of eligible pitchers: " + str(len(df_2023)))
print("Sum of eligible ip: " + str(int(df_2023['IP'].sum())))
print("Sum of 2023 K by 8/14: " + str(int(df_2023['SO'].sum())))
print("Total K/9 by 8/14: " +  str(9*df_2023['SO'].sum()/int(df_2023['IP'].sum())))
print("Max of 2023 K by 8/14: " + str(int(df_2023['SO'].max())))
print(list(df_2023.loc[df_2023['SO'] == df_2023['SO'].max()]['Name']))
print("Med of 2023 K by 8/14: " + str(int(df_2023['SO'].median())))
print("Mean of 2023 K by 8/14: " + str(int(df_2023['SO'].mean())))
# print(list(df_2023.loc[df_2023['SB'] == df_2023['SB'].median()]['Name']))
# df_2023.hist(column='SB')
col1s = ["ERA", 'W', 'xFIP', 'FIP', 'SIERA', 'IP']
col2 = 'SO'
top5_2023 = []
for col1 in col1s:
    print(col1)
    corr = df_2023[col1].corr(df_2023[col2])
    print("2023 Correlation between ", col1, " and ", col2, "is: ", round(corr, 2))
    if col1 in ['W', 'IP']:
        df_2023 = df_2023.sort_values(by=[col1], ascending=False)
    else:
        df_2023 = df_2023.sort_values(by=[col1])
    top_5 = list(df_2023['Name'][:5])
    print(top_5)
    top5_2023.extend(top_5)
top5_2023 = list(set(top5_2023))