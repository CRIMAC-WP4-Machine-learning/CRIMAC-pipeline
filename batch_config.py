# CRIMAC PIPELINE CONFIG FILE #

#
# First, select the operation mode as either standalone processing
# or HI cruise series processing
#

# For standalone processing, fill the below with another value than 'None'
SINGLE_DATA_DIR = None # or raw data dir such as: /cruise_data/2019/S2019847_PEROS_3317/ACOUSTIC/EK60/EK60_RAWDATA"
SINGLE_WORK_DIR = None # or work dir such as: "/cruise_data/2019/S2019847_PEROS_3317/ACOUSTIC/LSSS/WORK"

# ...or HI's CRUISE SERIES:

# Cruise series selector (e.g., 13 for Sandeel, as in cruiseseries.xml file)
CRUISE_SERIES_NUMBER = 13

# Root directory for the cruise data
ROOT_DIR = "/scratch/disk2/AzureMirror/cruise_data"

#
# Below values will apply to either standalone and cruise series processing #
#

# Important directories. Please note that we need to
# define different directories for different output types
FIRST_LEVEL_DIR = "ACOUSTIC"
GRIDDED_DATA_DIR = "GRIDDED_EK_DATA"
PREDICTOR_DATA_DIR = "PREDICTION_DATA"
BOTTOM_DATA_DIR = "BOTTOM_DATA"
INTEGRATOR_DATA_DIR = "INTEGRATION_DATA"

# Docker images
BOTTOMDETECTION_IMAGE = 'crimac/bottomdetection'
PREDICTOR_IMAGE = 'crimac/unet'
PREPROCESSOR_IMAGE = 'crimac/preprocessor'
INTEGRATOR_IMAGE = 'crimac/reportgeneration'

# Global settings
GLOBAL_PREFIX = None        # Specify prefix for the output names
                            # None means we use the cruise number
                            # or OUT for single cruise processing

# Per-step Settings

## Preprocessor
PREPROCESSOR_OVERWRITE     = 'yes'      # or resume or no
PREPROCESSOR_OUT_TYPE      = 'zarr'     # or netcdf4
PREPROCESSOR_MAIN_FREQ     = 38000
PREPROCESSOR_MAX_RANGE_SRC = 500
PREPROCESSOR_WRITE_PNG     = 'no'       # or yes
PREPROCESSOR_PROCESS_EK80  = True       # or False

## Predictor
PREDICTOR_OVERWRITE      = 'yes'        # or no
PREDICTOR_OUT_TYPE       = 'zarr'
PREDICTOR_MODEL_PATH     = "/scratch/disk2/AzureMirror/models/NR_Unet"
PREDICTOR_USE_CUDA       = True

## Bottom detector
BOTTOMDETECTION_OVERWRITE                  = 'yes'        # or no
BOTTOMDETECTION_ALGORITHM                  = 'simple'
BOTTOMDETECTION_OUT_TYPE                   = 'zarr'       # or parquet
BOTTOMDETECTION_PARAMETER_MINIMUM_RANGE    = 10.0
BOTTOMDETECTION_PARAMETER_OFFSET           = 0.5
BOTTOMDETECTION_PARAMETER_THRESHOLD_LOG_SV = -31.0

# Report generator / integrator
INTEGRATOR_OVERWRITE             = 'yes'    # or resume or no
INTEGRATOR_OUT_TYPE              = 'zarr'
INTEGRATOR_THRESHOLD             = 0.8
INTEGRATOR_MAIN_FREQ             = 38000
INTEGRATOR_MAX_RANGE_SRC         = 500
INTEGRATOR_HOR_INTEGRATION_TYPE  = 'ping'
INTEGRATOR_HOR_INTEGRATION_STEP  = 100
INTEGRATOR_VERT_INTEGRATION_TYPE ='range'
INTEGRATOR_VERT_INTEGRATION_STEP = 10
