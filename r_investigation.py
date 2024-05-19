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


    year_url      =   "https://www.fangraphs.com/leaders-legacy.aspx?pos=all&stats="+str(cat)+\
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


df_2019_stand = scrape_year(year='2019',cat='bat',verbose=0,date1='2019-03-20',date2='2019-09-18')
df_2019 = scrape_year(year='2019',cat='bat',verbose=0,date1='2019-03-20',date2='2019-09-18', stat_typ = 1)

# df_2019 = df_2019.loc[~df_2019['Name'].isin(['Andrew Vasquez', 'Gerardo Parra'])]

    
stand_cols = ['G','R', 'RBI', 'HR' , 'SB']

stand_cols.extend(['Name', 'Team'])       
df_2019 = df_2019.merge(df_2019_stand[stand_cols], on = ['Name', 'Team'], how = 'left')
df_2019['PA'] = df_2019['PA'].astype(float)
df_2019['R'] = df_2019['R'].astype(float)
print("Sum of 2019 R by 9/18: " + str(int(df_2019['R'].sum())))
df_2019 = df_2019.loc[(df_2019['PA']>100)]

cols = list(df_2019.columns)
cols.remove('Name')
cols.remove('Team')

for col in cols:
    # print(col)
    try:
        df_2019[col] = df_2019[col].astype(float)
    except:
        df_2019[col] = df_2019[col].str[:-1].astype(float)
# # df_2019 = df_2019.loc[(df_2019['SV']+df_2019['BS']+df_2019['HLD'])>0]

print("Count of eligible batters: " + str(len(df_2019)))
print("Sum of eligible pa: " + str(int(df_2019['PA'].sum())))
print("Sum of 2019 R by 9/18: " + str(int(df_2019['R'].sum())))
# print("Total R/PA by 9/18: " +  str(df_2019['R'].sum()))
print("Max of 2019 R by 9/18: " + str(int(df_2019['R'].max())))
print(list(df_2019.loc[df_2019['R'] == df_2019['R'].max()]['Name']))
print("Med of 2019 R by 9/18: " + str(int(df_2019['R'].median())))
print("Mean of 2019 R by 9/18: " + str(int(df_2019['R'].mean())))
print(list(df_2019.loc[df_2019['R'] == df_2019['R'].median()]['Name']))
df_2019.hist(column='R')
col1s = ["AVG", 'BABIP', 'Spd', 'SLG', 'OBP', 'PA', 'SB']
col2 = 'R'
top5_2019 = []
for col1 in col1s:
    # print(col1)
    corr = df_2019[col1].corr(df_2019[col2])
    print("2019 Correlation between ", col1, " and ", col2, "is: ", round(corr, 2))
    df_2019 = df_2019.sort_values(by=[col1], ascending=False)
    top_5 = list(df_2019['Name'][:5])
    print(top_5)
    top5_2019.extend(top_5)
top5_2019 = list(set(top5_2019))


df_2020_stand = scrape_year(year='2020',cat='bat',verbose=0,date1='2020-03-20',date2='2020-09-18')
df_2020 = scrape_year(year='2020',cat='bat',verbose=0,date1='2020-03-20',date2='2020-09-18', stat_typ = 1)

# df_2020 = df_2020.loc[~df_2020['Name'].isin(['Andrew Vasquez', 'Gerardo Parra'])]

    
stand_cols = ['G','R', 'RBI', 'HR' , 'SB']

stand_cols.extend(['Name', 'Team'])       
df_2020 = df_2020.merge(df_2020_stand[stand_cols], on = ['Name', 'Team'], how = 'left')
df_2020['PA'] = df_2020['PA'].astype(float)
df_2020['R'] = df_2020['R'].astype(float)
print("Sum of 2020 R by 9/18: " + str(int(df_2020['R'].sum())))
df_2020 = df_2020.loc[(df_2020['PA']>100)]

cols = list(df_2020.columns)
cols.remove('Name')
cols.remove('Team')

for col in cols:
    # print(col)
    try:
        df_2020[col] = df_2020[col].astype(float)
    except:
        df_2020[col] = df_2020[col].str[:-1].astype(float)
# # df_2020 = df_2020.loc[(df_2020['SV']+df_2020['BS']+df_2020['HLD'])>0]

print("Count of eligible batters: " + str(len(df_2020)))
print("Sum of eligible pa: " + str(int(df_2020['PA'].sum())))
print("Sum of 2020 R by 9/18: " + str(int(df_2020['R'].sum())))
# print("Total R/PA by 9/18: " +  str(df_2020['R'].sum()))
print("Max of 2020 R by 9/18: " + str(int(df_2020['R'].max())))
print(list(df_2020.loc[df_2020['R'] == df_2020['R'].max()]['Name']))
print("Med of 2020 R by 9/18: " + str(int(df_2020['R'].median())))
print("Mean of 2020 R by 9/18: " + str(int(df_2020['R'].mean())))
print(list(df_2020.loc[df_2020['R'] == df_2020['R'].median()]['Name']))
df_2020.hist(column='R')
col1s = ["AVG", 'BABIP', 'Spd', 'SLG', 'OBP', 'PA', 'SB']
col2 = 'R'
top5_2020 = []
for col1 in col1s:
    print(col1)
    corr = df_2020[col1].corr(df_2020[col2])
    print("2020 Correlation between ", col1, " and ", col2, "is: ", round(corr, 2))
    df_2020 = df_2020.sort_values(by=[col1], ascending=False)
    top_5 = list(df_2020['Name'][:5])
    print(top_5)
    top5_2020.extend(top_5)
top5_2020 = list(set(top5_2020))


df_2021_stand = scrape_year(year='2021',cat='bat',verbose=0,date1='2021-03-20',date2='2021-09-18')
df_2021 = scrape_year(year='2021',cat='bat',verbose=0,date1='2021-03-20',date2='2021-09-18', stat_typ = 1)

# df_2021 = df_2021.loc[~df_2021['Name'].isin(['Andrew Vasquez', 'Gerardo Parra'])]

    
stand_cols = ['G','R', 'RBI', 'HR' , 'SB']

stand_cols.extend(['Name', 'Team'])       
df_2021 = df_2021.merge(df_2021_stand[stand_cols], on = ['Name', 'Team'], how = 'left')
df_2021['PA'] = df_2021['PA'].astype(float)
df_2021['R'] = df_2021['R'].astype(float)
print("Sum of 2021 R by 9/18: " + str(int(df_2021['R'].sum())))
df_2021 = df_2021.loc[(df_2021['PA']>100)]

cols = list(df_2021.columns)
cols.remove('Name')
cols.remove('Team')

for col in cols:
    print(col)
    try:
        df_2021[col] = df_2021[col].astype(float)
    except:
        df_2021[col] = df_2021[col].str[:-1].astype(float)
# # df_2021 = df_2021.loc[(df_2021['SV']+df_2021['BS']+df_2021['HLD'])>0]

print("Count of eligible batters: " + str(len(df_2021)))
print("Sum of eligible pa: " + str(int(df_2021['PA'].sum())))
print("Sum of 2021 R by 9/18: " + str(int(df_2021['R'].sum())))
# print("Total R/PA by 9/18: " +  str(df_2021['R'].sum()))
print("Max of 2021 R by 9/18: " + str(int(df_2021['R'].max())))
print(list(df_2021.loc[df_2021['R'] == df_2021['R'].max()]['Name']))
print("Med of 2021 R by 9/18: " + str(int(df_2021['R'].median())))
print("Mean of 2021 R by 9/18: " + str(int(df_2021['R'].mean())))
print(list(df_2021.loc[df_2021['R'] == df_2021['R'].median()]['Name']))
df_2021.hist(column='R')
col1s = ["AVG", 'BABIP', 'Spd', 'SLG', 'OBP', 'PA', 'SB']
col2 = 'R'
top5_2021 = []
for col1 in col1s:
    print(col1)
    corr = df_2021[col1].corr(df_2021[col2])
    print("2021 Correlation between ", col1, " and ", col2, "is: ", round(corr, 2))
    df_2021 = df_2021.sort_values(by=[col1], ascending=False)
    top_5 = list(df_2021['Name'][:5])
    print(top_5)
    top5_2021.extend(top_5)
top5_2021 = list(set(top5_2021))


df_2022_stand = scrape_year(year='2022',cat='bat',verbose=0,date1='2022-03-20',date2='2022-09-18')
df_2022 = scrape_year(year='2022',cat='bat',verbose=0,date1='2022-03-20',date2='2022-09-18', stat_typ = 1)

# df_2022 = df_2022.loc[~df_2022['Name'].isin(['Andrew Vasquez', 'Gerardo Parra'])]

    
stand_cols = ['G','R', 'RBI', 'HR' , 'SB']

stand_cols.extend(['Name', 'Team'])       
df_2022 = df_2022.merge(df_2022_stand[stand_cols], on = ['Name', 'Team'], how = 'left')
df_2022['PA'] = df_2022['PA'].astype(float)
df_2022['R'] = df_2022['R'].astype(float)
print("Sum of 2022 R by 9/18: " + str(int(df_2022['R'].sum())))
df_2022 = df_2022.loc[(df_2022['PA']>100)]

cols = list(df_2022.columns)
cols.remove('Name')
cols.remove('Team')

for col in cols:
    # print(col)
    try:
        df_2022[col] = df_2022[col].astype(float)
    except:
        df_2022[col] = df_2022[col].str[:-1].astype(float)
# # df_2022 = df_2022.loc[(df_2022['SV']+df_2022['BS']+df_2022['HLD'])>0]

print("Count of eligible batters: " + str(len(df_2022)))
print("Sum of eligible pa: " + str(int(df_2022['PA'].sum())))
print("Sum of 2022 R by 9/18: " + str(int(df_2022['R'].sum())))
# print("Total R/PA by 9/18: " +  str(df_2022['R'].sum()))
print("Max of 2022 R by 9/18: " + str(int(df_2022['R'].max())))
print(list(df_2022.loc[df_2022['R'] == df_2022['R'].max()]['Name']))
print("Med of 2022 R by 9/18: " + str(int(df_2022['R'].median())))
print("Mean of 2022 R by 9/18: " + str(int(df_2022['R'].mean())))
print(list(df_2022.loc[df_2022['R'] == df_2022['R'].median()]['Name']))
df_2022.hist(column='R')
col1s = ["AVG", 'BABIP', 'Spd', 'SLG', 'OBP', 'PA', 'SB']
col2 = 'R'
top5_2022 = []
for col1 in col1s:
    print(col1)
    corr = df_2022[col1].corr(df_2022[col2])
    print("2022 Correlation between ", col1, " and ", col2, "is: ", round(corr, 2))
    df_2022 = df_2022.sort_values(by=[col1], ascending=False)
    top_5 = list(df_2022['Name'][:5])
    print(top_5)
    top5_2022.extend(top_5)
top5_2022 = list(set(top5_2022))


df_2023_stand = scrape_year(year='2023',cat='bat',verbose=0,date1='2023-03-20',date2='2023-09-18')
df_2023 = scrape_year(year='2023',cat='bat',verbose=0,date1='2023-03-20',date2='2023-09-18', stat_typ = 1)

# df_2023 = df_2023.loc[~df_2023['Name'].isin(['Andrew Vasquez', 'Gerardo Parra'])]

    
stand_cols = ['G','R', 'RBI', 'HR' , 'SB']

stand_cols.extend(['Name', 'Team'])       
df_2023 = df_2023.merge(df_2023_stand[stand_cols], on = ['Name', 'Team'], how = 'left')
df_2023['PA'] = df_2023['PA'].astype(float)
df_2023['R'] = df_2023['R'].astype(float)
print("Sum of 2023 R by 9/18: " + str(int(df_2023['R'].sum())))
df_2023 = df_2023.loc[(df_2023['PA']>100)]

cols = list(df_2023.columns)
cols.remove('Name')
cols.remove('Team')
cols.remove('UBR')
cols.remove('wGDP')

for col in cols:
    # print(col)
    try:
        df_2023[col] = df_2023[col].astype(float)
    except:
        df_2023[col] = df_2023[col].str[:-1].astype(float)
# # df_2023 = df_2023.loc[(df_2023['SV']+df_2023['BS']+df_2023['HLD'])>0]

print("Count of eligible batters: " + str(len(df_2023)))
print("Sum of eligible pa: " + str(int(df_2023['PA'].sum())))
print("Sum of 2023 eligible R by 9/18: " + str(int(df_2023['R'].sum())))
# print("Total R/PA by 9/18: " +  str(df_2023['R'].sum()))
print("Max of 2023 R by 9/18: " + str(int(df_2023['R'].max())))
print(list(df_2023.loc[df_2023['R'] == df_2023['R'].max()]['Name']))
print("Med of 2023 R by 9/18: " + str(int(df_2023['R'].median())))
print("Mean of 2023 R by 9/18: " + str(int(df_2023['R'].mean())))
print(list(df_2023.loc[df_2023['R'] == df_2023['R'].median()]['Name']))
df_2023.hist(column='R')
col1s = ["AVG", 'BABIP', 'Spd', 'SLG', 'OBP', 'PA', 'SB']
col2 = 'R'
top5_2023 = []
for col1 in col1s:
    print(col1)
    corr = df_2023[col1].corr(df_2023[col2])
    print("2023 Correlation between ", col1, " and ", col2, "is: ", round(corr, 2))
    df_2023 = df_2023.sort_values(by=[col1], ascending=False)
    top_5 = list(df_2023['Name'][:5])
    print(top_5)
    top5_2023.extend(top_5)
top5_2023 = list(set(top5_2023))