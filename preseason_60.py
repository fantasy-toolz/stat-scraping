# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 11:38:30 2022

@author: rentz
"""

import stat_scraping 
from datetime import datetime

print("Start =",  datetime.now())

date_string = format(datetime.now().strftime('%Y%m%d'), "1")

hit_df = stat_scraping.get_fantasy_pros_stats('hitters')
pit_df = stat_scraping.get_fantasy_pros_stats('pitchers')