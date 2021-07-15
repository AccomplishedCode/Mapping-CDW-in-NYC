# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 13:13:11 2021

@author: Parth
"""

import pandas as pd
import numpy as np
import json

df= pd.read_csv('C:/Users/Parth/Documents/Work/Study/Spring21/Capstone/main_cdw_app/trips_v2.csv')

df= df.fillna({'Destiny':'Not Applicable', 'Tonnage':0})


df.to_csv('C:/Users/Parth/Documents/Work/Study/Spring21/Capstone/main_cdw_app/cleaned_transfers.csv')

