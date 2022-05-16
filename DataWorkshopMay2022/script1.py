# This tests if you have all the ncessary libabries
import xarray as xr
import pandas as pd
import os
import zarr as zr
import matplotlib as mp
import matplotlib.pyplot as plt
import holoviews as hv
import holoviews.operation.datashader as hd
import bokeh as bk
import torch
import dask
import numcodecs
import PyYAML
import sklearn
import scipy
import pyarrow

# This test if you can access the data  files
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

