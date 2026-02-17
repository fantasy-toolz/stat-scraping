# -*- coding: utf-8 -*-
"""
Created on Tue Feb 04 10:01:14 2020

@author: Erich Rentz
"""

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import pandas as pd
import datetime
import time
from selenium import webdriver

date_string             =  format(datetime.datetime.now().strftime('%Y%m%d'), "1")

# Outline FanGraphs Url components for scraping
projections = [
        'fangraphsdc', 
        'steamer', 
        'atc', 
        'thebat',
         'zips'
        ]

# Ask for fangraphs creds
try:
    creds.keys()
except:
    
    creds = dict([("email",  input("What is your email? (include quotations in 2)")),
                  ("password", input("What is your password? (include quotations in 2)"))
                    ]
            )

#Google File IDs
pa_ID = '1e9m0MPMU0sg415rKcgpcJOrJDhoDQwtI'
id_ID = '1JPPUenvD7I11Z6n_ndVP2sDbYh6JdHlU'

## subroutines
def create_browser():
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : os.path.join(os.getcwd(), "Data")}
    chrome_options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(options=chrome_options)
    return browser

def UploadFileByID(in_file, in_googsID):
    file6 = drive.CreateFile({'id': in_googsID})
    file6.SetContentFile(in_file)
    file6.Upload() 

def grab_data(browser, player_type):
    proj_dfs = []
    last_time = 0
    # Define urls based on type
    if player_type == 'pitching':
        url         = 'https://www.fangraphs.com/projections.aspx?pos=all&stats=pit&type={0}&team=0&lg=all&players=0'
    elif player_type == 'hitting':
        url         = 'https://www.fangraphs.com/projections.aspx?pos=all&stats=bat&type={0}&team=0&lg=all&players=0'     
    # grab data from fangraphs, return dfs for each projection outlet
    for proj in projections:
        print(url.format(proj))
        proj_csv = 'Data//{} {} {}.csv'.format(player_type, proj, date_string)
        if not os.path.exists(proj_csv):
            browser.get(url.format(proj))
            element = browser.find_element_by_id("ProjectionBoard1_cmdCSV")
            browser.maximize_window()
            browser.execute_script("arguments[0].scrollIntoView();", element)
            browser.execute_script("window.scrollBy(0, -150);")
            time.sleep(2)
            browser.find_element_by_id('ProjectionBoard1_cmdCSV').click()
            time.sleep(2)
#            filename = max([f for f in os.listdir(os.path.join(os.getcwd(), "Data"))], key=os.path.getctime) 
            
#            this doesn't work
            
            for f in os.listdir('Data'):
                print(f)
                if os.path.isfile(os.path.join('Data', f)) and  f.endswith(".csv"):
                    doc_time =  os.path.getctime(os.path.join('Data', f))
                    print(doc_time)
                    if doc_time > last_time:
                        filename = os.path.join(os.getcwd(), 'Data', f)
                        last_time = doc_time
            os.rename(filename, os.path.join(os.getcwd(), proj_csv)) 
        proj_df = pd.read_csv(os.path.join(os.getcwd(), proj_csv))
        proj_dfs.append(proj_df)
    # Aggregate all the projections DFs
    proj_df = proj_dfs[0]
    proj_df['UID'] = proj_df['playerid'].astype(str)
    for i in proj_dfs[1:]:
        i['UID'] = i['playerid'].astype(str) # PlayerIDs are messed, fill new UID field
        proj_df = pd.concat([proj_df, i])
        
    return proj_df

#
## Grab data and analyze
#
# Initiate selenium
browser = create_browser()
browser.get('https://blogs.fangraphs.com/wp-login.php?')
elem = browser.find_element_by_xpath('//*[@id="user_login"]')
elem.send_keys(creds['email'])
elem = browser.find_element_by_xpath('//*[@id="user_pass"]')
elem.send_keys(creds['password'])
elem = browser.find_element_by_xpath('//*[@id="wp-submit"]').click()

# Grab hitting and pitching dfs
pit_df = grab_data(browser, 'pitching')
hit_df = grab_data(browser, 'hitting')

# Summarize IP by player ID and Name by playerID
pit_df['IP'] = pit_df['IP']/1.0
ip_df = pd.DataFrame(pit_df.groupby(['UID'])['IP'].mean())
pit_name_df = pd.DataFrame(pit_df.groupby(['UID'])['﻿"Name"'].first())

# Merge Names over to IP summary, rename columns, and save
ip_df = ip_df.merge(pit_name_df,  right_index = True,  left_index = True)
ip_df.columns = ['IP', 'Name']
ip_df.to_csv('Data//Stolen_IPs_{0}.csv'.format(date_string), index = True)

# Summarize PA by player ID and Name by playerID
pa_df = pd.DataFrame(hit_df.groupby(['UID'])['PA'].mean())
hit_name_df = pd.DataFrame(hit_df.groupby(['UID'])['﻿"Name"'].first())

# Merge Names over to PA summary, rename columns, and save
pa_df = pa_df.merge(hit_name_df,  right_index = True,  left_index = True)
pa_df.columns = ['PA', 'Name']
pa_df.to_csv('Data//Stolen_PAs_{0}.csv'.format(date_string), index = True)

#
## Upload to GoogleDrive
#       
try:
    drive
except:
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

UploadFileByID('Data//Stolen_PAs_{0}.csv'.format(date_string), pa_ID)
UploadFileByID('Data//Stolen_IPs_{0}.csv'.format(date_string), id_ID)
    
