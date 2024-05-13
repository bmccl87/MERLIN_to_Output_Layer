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
import time
import shutil 

def convert_lat_lon(merlin_cc):
    
    temp_merlin = merlin_cc
    temp_merlin[['Lat_Deg','Lat_Min','Lat_Seconds']] =  temp_merlin['Lat'].str.split(':',expand=True)
    temp_merlin['Lat_Deg'] = temp_merlin['Lat_Deg'].astype('float')
    temp_merlin['Lat_Min'] = temp_merlin['Lat_Min'].astype('float')/60. 
    temp_merlin['Lat_Seconds'] = temp_merlin['Lat_Seconds'].astype('float')/3600.
    temp_merlin['Lat_Decimal'] = temp_merlin['Lat_Deg']+temp_merlin['Lat_Min']+temp_merlin['Lat_Seconds']
    
    temp_merlin[['Lon_Deg','Lon_Min','Lon_Seconds']] = temp_merlin['Lon'].str.split(':',expand=True)
    temp_merlin['Lon_Deg'] = temp_merlin['Lon_Deg'].astype('float')
    temp_merlin['Lon_Min'] = temp_merlin['Lon_Min'].astype('float')/60.
    temp_merlin['Lon_Seconds'] = temp_merlin['Lon_Min'].astype('float')/3600. 
    temp_merlin['Lon_Decimal'] = temp_merlin['Lon_Deg']-temp_merlin['Lon_Min']-temp_merlin['Lat_Seconds']

    return temp_merlin

# merlin_cc.rename({0:'Date',2:'Time',6:'Lat',8:'Lon',20:'SemiMajor',22:'SemiMinor',24:'Ellipse_Angle',26:'Sensors'},inplace=True,axis=1)
# merlin_cc.dropna(inplace=True,axis=0)
# merlin_cc = convert_lat_lon(merlin_cc)
# merlin_cc['Date_Time'] = pd.to_datetime(merlin_cc['Date']+' '+merlin_cc['Time'],errors='coerce')
# merlin_cc.set_index(merlin_cc['Date_Time'],inplace=True)
# merlin_cc.sort_index(axis=0,inplace=True)
# merlin_cc.dropna(axis=0,inplace=True)
# merlin_cc = merlin_cc[merlin_cc.index.month==6]

pickle_dir = '/Users/brandonmcclung/Data/pickles/merlin_cc/pre_QC/'

qc_dir = '/Users/brandonmcclung/Data/pickles/merlin_cc/post_QC/'
files = os.listdir(pickle_dir)
files2 = os.listdir(qc_dir)
i=0

for file in files:
    print(file)
    t=time.time() 
    mo_int = int(file[5:7])
    merlin_cc = pd.read_pickle(pickle_dir+file)
    merlin_cc.rename({0:'Date',2:'Time',6:'Lat',8:'Lon',20:'SemiMajor',22:'SemiMinor',24:'Ellipse_Angle',26:'Sensors'},inplace=True,axis=1)
    merlin_cc.dropna(inplace=True,axis=0)
    merlin_cc = convert_lat_lon(merlin_cc)
    merlin_cc['Date_Time'] = pd.to_datetime(merlin_cc['Date']+' '+merlin_cc['Time'],errors='coerce')
    merlin_cc.set_index(merlin_cc['Date_Time'],inplace=True)
    merlin_cc.sort_index(axis=0,inplace=True)
    merlin_cc.dropna(axis=0,inplace=True)
    merlin_cc = merlin_cc[merlin_cc.index.month==mo_int]
    merlin_cc.to_pickle(qc_dir+'qcd_'+file)
    elapsed = time.time()-t
    shutil.move(pickle_dir+file,'/Users/brandonmcclung/Data/pickles/merlin_cc/ran_qc/'+file)
    print(file,elapsed)  
    i=i+1


