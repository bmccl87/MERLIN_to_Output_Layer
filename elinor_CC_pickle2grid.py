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
import shutil


def to_netcdf(temp1,mo,yr):
    cape_lats = pd.read_pickle('/Users/brandonmcclung/Data/pickles/grids/LaunchCastLat.p')
    cape_lons = pd.read_pickle('/Users/brandonmcclung/Data/pickles/grids/LaunchCastLon.p')

    xedge = cape_lons[0,:]
    yedge = cape_lats[:,0]

    xmid = [] #Blank array
    ymid = [] #Blank array

    i=0
    while(i < len(xedge)-1):
        xmid.append((xedge[i]+xedge[i+1])/2) #Calculate and append midpoints
        i+=1
    i=0
    while(i < len(yedge)-1):
        ymid.append((yedge[i]+yedge[i+1])/2) #Calculate and append midpoints
        i+=1
    #consider rounding 

    #first time rounded down/backward to the nearest 5 minutes
    first_time = temp1['Date_Time'].iloc[0]
    print(first_time)
    if round(first_time.minute,-1)==60:
        start_time = first_time.replace(minute=55,second=0,microsecond=0,nanosecond=0) #start_slicing with this time
    else:
        start_time = first_time.replace(minute=round(first_time.minute,-1),second=0,microsecond=0,nanosecond=0)
    #last time rounded up to the forward nearest 5 minutes
    last_time = temp1['Date_Time'].iloc[len(temp1)-1]
    end_time = last_time.replace(minute=round(last_time.minute,+1),second=0,microsecond=0,nanosecond=0)
    print(end_time)

    # last_time = temp1['Date_Time'][len(temp1)-1]
    time_sample = dt.timedelta(0, 300)
    temp_array = xr.Dataset()
    tempArrayList = []
    tempArrayTimeList = []
    t=0
    while(start_time<=end_time):
        temp_df = temp1[slice(start_time,start_time+time_sample)]
        if len(temp_df)>0: #deviates from randy's and tobias's code
            C = util.boxbin(temp_df['Lon_Decimal']+360, temp_df['Lat_Decimal'], xedge, yedge, mincnt=0)
            tempArray = xr.Dataset(
                data_vars=dict(strikes=(["x", "y"], C)),
                coords=dict(
                    lon=(["x"], xmid),
                    lat=(["y"], ymid),
                ),
                attrs=dict(description="Lightning data"),
            )  # Create dataset
            tempArrayList.append(tempArray)
            tempArrayTimeList.append(start_time)

        start_time = start_time+time_sample
        t=t+1
    
    tempArray = xr.concat(tempArrayList, data_vars='all', dim='time')
    tempArray = tempArray.assign_coords(time=tempArrayTimeList)
    tempArray = tempArray.fillna(0)
    print(tempArray)
    
    # tempArray.to_netcdf('/Users/brandonmcclung/Data/netcdfs/merlin_cc_16jan24/'+mo+yr+'.nc',mode='w',format="NETCDF4") #Save
     #Print save message
    return tempArray

p_dir = '/Users/brandonmcclung/Data/pickles/merlin_cc/post_qc/'
files = os.listdir(p_dir)
txt_dump = open('/Users/brandonmcclung/Data/txt_dump/merlin_cc_src_subset.txt','w')
txt_dump.write('mo,yr,before,after'+'\n')

err_log = open('/Users/brandonmcclung/Data/txt_dump/merlin_cc_error.txt','w')

cape_lats = pd.read_pickle('/Users/brandonmcclung/Data/pickles/grids/LaunchCastLat.p')
cape_lons = pd.read_pickle('/Users/brandonmcclung/Data/pickles/grids/LaunchCastLon.p')

xedge = cape_lons[0,:]
yedge = cape_lats[:,0]

print(xedge[0])
print(xedge[len(xedge)-1])

print(yedge[0])
print(yedge[len(yedge)-1])

i=0
for file in files:
    
    if i==1:        
        mo = file[9:11]
        yr = file[6:8]
        print(file)
        try:
            merlin_cc = pd.read_pickle(p_dir+file)
            merlin_cc['Lon_Decimal_360'] = merlin_cc['Lon_Decimal']+360
            merlin_cc_subset = merlin_cc.loc[merlin_cc['Lon_Decimal_360']>=xedge[0]]
            merlin_cc_subset = merlin_cc_subset.loc[merlin_cc_subset['Lon_Decimal_360']<=xedge[len(xedge)-1]]
            merlin_cc_subset = merlin_cc_subset.loc[merlin_cc_subset['Lat_Decimal']>=yedge[len(yedge)-1]]
            merlin_cc_subset = merlin_cc_subset.loc[merlin_cc_subset['Lat_Decimal']<=yedge[0]]
            # txt_dump.write(mo+','+yr+','+str(len(merlin_cc))+','+str(len(merlin_cc_subset))+'\n')
            cc_xarray = to_netcdf(merlin_cc_subset,mo,yr)
            f = open('/Users/brandonmcclung/Data/pickles/merlin_cc/xr_binned_cc/'+mo+yr+'.p','wb')
            pickle.dump(cc_xarray,f)
            print('Saved: ' + mo+yr+'.p')
            shutil.move(p_dir+file,'/Users/brandonmcclung/Data/pickles/merlin_cc/ran2grid/'+file)
        except ValueError:
            print('minute valueError')
            err_log.write('minute must be in 0..59 '+file+' \n')
        except:
            print('something went wrong')
            err_log.write('something else went wrong '+file+' \n')
    i=i+1
txt_dump.close()
err_log.close()