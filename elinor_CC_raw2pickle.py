import pickle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import util
import datetime as dt
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os

#this code removes the empty files.  I manually changed the year and months to process in an orderly manner. 
data_dir = '/Users/brandonmcclung/Data/KSC_Weather_Archive/MERLIN_CC/'
yrs = ['2023']
mos = ['02','04','05','06']
# for yr in yrs:
#     for mo in mos:
#         dir = data_dir+yr+'_CC/'+mo+'/'
#         files = os.listdir(dir)
#         for file in files:
#             try:
#                     temp = pd.read_csv(dir+file,sep=' ',header=None,usecols=[0,2,6,8,12,15,20,22,24,26],low_memory=False)
#             except:
#                 print('no data: '+file+' removing')
#                 os.remove(dir+file)

#this code loads the raw data into a pickle file for fast I/O
for yr in yrs:
    for mo in mos:
        print(yr,mo)
        first_file=True
        dir = data_dir+yr+'_CC/'+mo+'/'
        files = os.listdir(dir)
        for file in files:
            if first_file==True:
                print(file)
                first_file=False
                merlin_cc = pd.read_csv(dir+file,sep=' ',header=None,usecols=[0,2,6,8,20,22,24,26],low_memory=False,\
                    on_bad_lines='skip')
                # print(merlin_cc)
            else:
                print(file)
                merlin_cc = pd.concat([merlin_cc,pd.read_csv(dir+file,sep=' ',header=None,usecols=[0,2,6,8,20,22,24,26],\
                    on_bad_lines='skip',low_memory=False)])
        data_stor = '/Users/brandonmcclung/Data/pickles/merlin_cc/'
        file = open(data_stor+yr+'_'+mo+'_merlin_cc_df.p','wb')
        pickle.dump(merlin_cc,file)
        file.close() 