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

from pathlib import Path

# Get the core functions
from batch_core import Pipeline
import batch_config as config


pipeline = Pipeline()

if config.SINGLE_DATA_DIR is None:
    # This means we process HI's data
    config.PROCESS_HI_DATA = True

    # Get All cruise series (by default using code 13 or Sandeel cruise, see config file)
    cruise_list = Pipeline.extract_cruise_series("./cruiseseries.xml", config.CRUISE_SERIES_NUMBER)
    print(cruise_list)

    # Select a cruise
    #selected_cruise = [cruise_list['2019']]

    # Select all cruises
    selected_cruise = cruise_list.values()
else:
    # Not processing HI's data (single input)
    config.PROCESS_HI_DATA = False

    # Use single cruise
    selected_cruise = dict({'OUT': ['OUT', 'OUT', Path(config.SINGLE_DATA_DIR)]}).values()


print(selected_cruise)

# Preprocess data
for _, _, p in selected_cruise:
    prefix = pipeline.gen_prefix(config.GLOBAL_PREFIX, p)
    pipeline.populate_paths(p, prefix)
    pipeline.do_preprocessing(p)

# U-net prediction
for _, _, p in selected_cruise:
    prefix = pipeline.gen_prefix(config.GLOBAL_PREFIX, p)
    pipeline.populate_paths(p, prefix)
    pipeline.do_prediction(p)

# Bottom classification
for _, _, p in selected_cruise:
    prefix = pipeline.gen_prefix(config.GLOBAL_PREFIX, p)
    pipeline.populate_paths(p, prefix)
    pipeline.do_bottom_detection(p)

# Integration
for _, _, p in selected_cruise:
    prefix = pipeline.gen_prefix(config.GLOBAL_PREFIX, p)
    pipeline.populate_paths(p, prefix)
    pipeline.do_integration(p)
