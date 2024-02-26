# -*- coding: utf-8 -*-
"""
Created on Thu May 19 21:15:17 2022

@author: rentz
"""

import stat_scraping 
import fantasy_pros as fp
from datetime import datetime

print("Start =",  datetime.now())

date_string = format(datetime.now().strftime('%Y%m%d'), "1")

hit_df = stat_scraping.get_fantasy_pros_proj('hitters', True)
pit_df = stat_scraping.get_fantasy_pros_proj('pitchers', True)

hit_df.to_csv('data/fp_proj_hit_{}.csv'.format(date_string), index = False)
pit_df.to_csv('data/fp_proj_pit_{}.csv'.format(date_string), index = False)

overall_ranks_df = fp.get_fantasy_pros_rank()


print("End =",  datetime.now())
