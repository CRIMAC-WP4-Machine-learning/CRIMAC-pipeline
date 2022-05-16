import xarray as xr
import pandas as pd
import os

# Data  files
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
zarr_grid = xr.open_zarr(sv_fname)
zarr_pred = xr.open_zarr(annotations_fname)
df = pd.read_csv(schools_fname)

