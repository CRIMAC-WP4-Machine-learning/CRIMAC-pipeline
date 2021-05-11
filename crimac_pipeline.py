"""
CRIMAC Pipeline Script

Copyright (C) 2021, Ibrahim Umar and The Institute of Marine
Research, Norway.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

# Get the core functions
from batch_core import Pipeline

# Get All sandeel surveys (code series 13)
pipeline = Pipeline()

cruise_list = Pipeline.extract_cruise_series("cruiseseries.xml", 13)
print(cruise_list)

# Select a cruise
selected_cruise = [cruise_list['2019']]

# Select all cruises
#selected_cruise = cruise_list.values()

print(selected_cruise)

# Preprocess data
for _, _, p in selected_cruise:
    pipeline.do_preprocessing(p, prefix = None, grid_data_type = 'zarr', process_ek80 = True)

# U-net prediction
for _, _, p in selected_cruise:
    pipeline.do_prediction(p, prefix = None, grid_data_type = 'zarr')

# Bottom classification
for _, _, p in selected_cruise:
    pipeline.do_bottom_detection(p, prefix = None, algorithm = 'simple', grid_data_type = 'zarr')

# Integration
#for _, _, p in selected_cruise:
#    pipeline.do_integration(
