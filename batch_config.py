# Root directory for the cruises
#ROOT_DIR = "/scratch/disk3/ibrahim-subset-2019/cruise_data"
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
INTEGRATOR_IMAGE = 'crimac/reportgeneration'

# Report generator configuration
INT_THRESHOLD=0.8
INT_MAIN_FREQ = 38000
INT_MAX_RANGE_SRC = 500
HOR_INTEGRATION_TYPE = ping
HOR_INTEGRATION_STEP = 100
VERT_INTEGRATION_TYPE=range
VERT_INTEGRATION_STEP=10
