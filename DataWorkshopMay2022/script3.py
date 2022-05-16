import xarray as xr
import pandas as pd
import os
import csv
import numpy as np
import matplotlib as mpl
mpl.use('Agg') # Needed for plotting as files if you do not have xwindows
import matplotlib.pyplot as plt

imgsave = '/mnt/d/DATAscratch/crimac-scratch/TMP/'

# Data  files
d = '/mnt/d/DATAscratch/crimac-scratch'
f = '/2019/S2019847_0511/ACOUSTIC/GRIDDED/S2019847_0511'
sv_fname = d + f + '_sv.zarr'
annotations_fname = d + f + '_labels.zarr'
schools_fname = d + f + '_labels.parquet.csv'

# Check if files are available
print(os.path.isdir(sv_fname))
print(os.path.isdir(annotations_fname))
print(os.path.isfile(schools_fname))

# Open the files
zarr_grid = xr.open_zarr(sv_fname)
zarr_pred = xr.open_zarr(annotations_fname)
df = pd.read_csv(schools_fname)

# Try these
zarr_grid
zarr_grid.frequency
zarr_grid.channel_id[0].values

zarr_pred
zarr_pred.category

zarr_pred.coords

# Extract the indices for school k
k = 91
df.iloc[k, :]
extrapixels = 5
x1 = int(df.iloc[k, 7]-extrapixels)
x2 = int(df.iloc[k, 8]+extrapixels)
y1 = int(df.iloc[k, 11]-extrapixels)
y2 = int(df.iloc[k, 12]+extrapixels)

# Plot the sv data for school k


# https://xarray-contrib.github.io/xarray-tutorial/scipy-tutorial/03_computation_with_xarray.html
sv_sub = zarr_grid.sv.isel(ping_time=slice(x1, x2),
                         range=slice(y1, y2))
Sv_sub = 10*np.log10(sv_sub)

# Plot all Sv values
Sv_sub.plot()
plt.savefig(imgsave+'01_allchannels_Sv.png', dpi=300)
plt.close()

# Plot one channel
Sv_sub.isel(frequency=4).T.plot()
plt.savefig(imgsave+'02_channel0_Sv.png', dpi=300)
plt.close()

# Subset the annotation data set
pred_sub = zarr_pred.isel(ping_time=slice(x1, x2),
                          range=slice(y1, y2))

# Select the pixels associated witht the object k
annotmask = pred_sub.object == df.iloc[k,:].object
annotmask.T.plot()
plt.savefig(imgsave+'03_annotmask.png', dpi=300)
plt.close()

# Filter the data based on the annotation mask
masked_Sv = annotmask * Sv_sub
masked_Sv.isel(frequency=4).T.plot()
plt.savefig(imgsave+'04_maskedSv.png', dpi=300)
plt.close()


# Plot as np arrays instead
fig, axs = plt.subplots(nrows=2, ncols=4)
axs[0, 0].imshow(10 * np.log10(zarr_grid.sv.isel(frequency=slice(0, 1), ping_time=slice(x1, x2), range=slice(y1,y2)) )[0].T, cmap='hot')
axs[0, 1].imshow(10 * np.log10(zarr_grid.sv.isel(frequency=slice(1, 2), ping_time=slice(x1, x2), range=slice(y1,y2)) )[0].T, cmap='hot')
axs[0, 2].imshow(10 * np.log10(zarr_grid.sv.isel(frequency=slice(2, 3), ping_time=slice(x1, x2), range=slice(y1,y2)) )[0].T, cmap='hot')
axs[1, 0].imshow(10 * np.log10(zarr_grid.sv.isel(frequency=slice(3, 4), ping_time=slice(x1, x2), range=slice(y1,y2)) )[0].T, cmap='hot')
axs[1, 1].imshow(10 * np.log10(zarr_grid.sv.isel(frequency=slice(4, 5), ping_time=slice(x1, x2), range=slice(y1,y2)) )[0].T, cmap='hot')
axs[1, 2].imshow(10 * np.log10(zarr_grid.sv.isel(frequency=slice(5, 6), ping_time=slice(x1, x2), range=slice(y1,y2)) )[0].T, cmap='hot')

axs[0, 3].imshow(10 * (zarr_pred.annotation.isel(category=slice(3, 4), ping_time=slice(x1, x2), range=slice(y1, y2 )))[0].T,cmap='hot')
axs[1, 3].imshow(10 * (zarr_pred.annotation.isel(category=slice(3, 4), ping_time=slice(x1, x2), range=slice(y1, y2 )))[0].T,cmap='hot')

plt.savefig(imgsave+'sv.png')
plt.close()

