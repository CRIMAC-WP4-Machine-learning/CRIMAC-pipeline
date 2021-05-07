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
import batch_core

# Get the configuration
import batch_config


# Get All sandeel survey (code series 13)
client = init_docker()
cruise_list = extract_cruise_series("cruiseseries.xml", 13)
do_batch(cruise_list)


# This script is the starting point for a working CRIMAC pipeline. The different steps can 

# Read cruise series
#cs=extract_cruise_series?

# Choose cruise series to process
#cruiseseries = cs[1]

# Preprocess data
#for cruise in cruiseseries
#   preprocess_data(cruise)

# Bottom classification
#for cruise in cruiseseries
#   preprocess_data(cruise)

# Bottom classification
#for cruise in cruiseseries
#   preprocess_data(cruise)

# Integration step
#for cruise in cruiseseries
#   integrate(cruise)

