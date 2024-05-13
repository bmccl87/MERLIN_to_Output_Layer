import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import os
import shutil
import numpy as np

nc_dir = '/Users/brandonmcclung/Data/netcdfs/merlin_cg/'
img_dir = '/Users/brandonmcclung/Desktop/merlin_cg/'
files = os.listdir(nc_dir)
idx = 2
test = xr.open_dataset(nc_dir+files[idx],engine='netcdf4')
print(files[idx])

# print(test['lon'].values)
# print(len(test['time']))

for i in range(len(test['time'])):
    if i<9999999999999999:
        fig = plt.figure(figsize=(16,10))
        ax = fig.add_subplot(1,1,1, projection=ccrs.PlateCarree())
        ax.set_extent([-81.25,-80,28,29],crs=ccrs.PlateCarree())
        temp = test['strikes'][i,:,:].values
        bool1 = np.where(temp==0)
        temp[bool1]=np.nan
        plt.pcolormesh(test['lon']-360, test['lat'],temp.transpose(),transform=ccrs.PlateCarree())
        ax.add_feature(cfeature.LAND, edgecolor="black")
        ax.add_feature(cfeature.OCEAN, edgecolor="black")
        cbar = plt.colorbar()
        plt.clim(0, 10)
        cbar.ax.tick_params(labelsize=24)
        cbar.set_label(label='# MERLIN C-G - Sources', size=24)
        plt.savefig(img_dir+'cg_neg_'+str(i)+'.png')
        plt.close()