# Import packages
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import xarray as xr

# Data file
d = '/DATAscratch/crimac-scratch'
f = '/S2019847_0511/2019/S2019847_0511/ACOUSTIC/GRIDDED/S2019847_0511'
sv_fname = d+f+'_sv.zarr'
annotations_fname = d+f+'_labels.zarr'
schools_fname = d+f+'_labels.parquet.csv'

# Check if files are available
print(os.path.isdir(sv_fname))
print(os.path.isdir(annotations_fname))
print(os.path.isfile(schools_fname))

# Open the files
sv = xr.open_zarr(sv_fname)
annot = xr.open_zarr(annotations_fname)
df = pd.read_csv(schools_fname)

# The df is a list of LSSS objects
df

# Take a look at a few annotations
for i, row in df[90:93].iterrows():
    annotationtype = row['ID'].split("__", 1)[1].split("-", 1)[0]
    category = str(int(row['category']))
    print('annotationtype:' + annotationtype + ' category:' + category)
    print(' ')
    print(row)
    print(' ')
    print(' ')

# Extract the indices for school k
k = 91
df.iloc[k, :]
extrapixels = 10
x1 = int(df.iloc[k, 7]-extrapixels)
x2 = int(df.iloc[k, 8]+extrapixels)
y1 = int(df.iloc[k, 11]-extrapixels)
y2 = int(df.iloc[k, 12]+extrapixels)

# Plot the sv data for school k

# https://xarray-contrib.github.io/xarray-tutorial/scipy-tutorial/03_computation_with_xarray.html
nils = sv.sv.isel(frequency=slice(0, 1),
                  ping_time=slice(x1, x2),
                  range=slice(y1, y2))

nils

sv_sub = sv.sv.isel(frequency=1,
                    ping_time=slice(x1, x2),
                    range=slice(y1, y2))
Sv_sub = 10*np.log10()
sv_sub.T.plot()
plt.show()

