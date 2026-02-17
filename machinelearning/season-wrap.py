# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 06:28:52 2022

@author: rentz
"""

import stat_scraping as ss

df_hit = ss.get_fantasy_pros_stats(player_type = 'hitters')
df_pre_hit = ss.get_fantasy_pros_proj(player_type = 'hitters', preseason = True)