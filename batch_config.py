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
PREDICTOR_IMAGE = 'crimac/predictor'
PREPROCESSOR_IMAGE = 'crimac/preprocessor'
