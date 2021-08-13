# Root directory for the cruises
ROOT_DIR = "/scratch/disk2/AzureMirror/cruise_data"

# Important directories. Please note that we need to
# define different directories for different output types
FIRST_LEVEL_DIR = "ACOUSTIC"
GRIDDED_DATA_DIR = "GRIDDED_EK_DATA"
PREDICTION_DATA_DIR = "PREDICTION_DATA"
BOTTOM_DATA_DIR = "BOTTOM_DATA"

# Docker images
BOTTOMDETECTION_IMAGE = 'crimac/bottomdetection'
PREDICTOR_IMAGE = 'crimac/unet'
PREPROCESSOR_IMAGE = 'crimac/preprocessor'

# Global settings

##
PREPROCESSOR_OVERWRITE = 'resume'       # or yes or no
PREPROCESSOR_OUT_TYPE = 'zarr'          # or netcdf4
PREPROCESSOR_MAIN_FREQ = 38000
PREPROCESSOR_MAX_RANGE_SRC = 500
PREPROCESSOR_WRITE_PNG = 'no'           # or yes

##
PREDICTOR_OVERWRITE = 'yes'             # or no
PREDICTOR_GRID_DATA_TYPE = PREPROCESSOR_OUT_TYPE

##
BOTTOMDETECTION_OVERWRITE = 'yes'       # or no
BOTTOMDETECTION_ALGORITHM = 'simple'
BOTTOMDETECTION_GRID_DATA_TYPE = PREPROCESSOR_OUT_TYPE
BOTTOMDETECTION_OUT_TYPE = 'zarr'       # or parquet

