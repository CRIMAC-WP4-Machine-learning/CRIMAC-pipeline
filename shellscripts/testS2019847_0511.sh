#!/bin/bash
# This code runs the testing of the pipeline on the S2019847_0511 data set on Pallas
# 

VAR1="HI-14667"
VAR2=$(hostname)

if [ "$VAR1" = "$VAR2" ]; then
    echo "HI-14667 setup"
    export DATAIN='/mnt/c/DATAscratch/crimac-scratch/2019/S2019847_0511/'
    export DATAOUT='/mnt/c/DATAscratch/crimac-scratch/2019/S2019847_0511/'
    export MODEL='/mnt/c/DATAscratch/crimac-scratch/NR_Unet/'

else
    echo "pallas setup"
    export DATAIN='/localscratch_hdd/crimac/2019/S2019847_0511/'
    export DATAOUT='/localscratch_hdd/nilsolav/2019/S2019847_0511/'
    export MODEL='/localscratch_hdd/nilsolav/modelweights/'
fi

export SURVEY='S2019847_0511' # Assume that ${SURVEY}_sv file exit
export MODELFILE='regriddingPaper_v1_baseline.pt'

export PREDICTIONFILE_1=${SURVEY}_labels.zarr
export REPORTFILE_1=${SURVEY}_report_1.zarr
export PREDICTIONFILE_2=${SURVEY}_predictions_2.zarr
export REPORTFILE_2=${SURVEY}_report_2.zarr

# Static variables for report genertor
export PING_AXIS_INTERVAL_TYPE="distance"  # see http://vocab.ices.dk/?ref=1455
export PING_AXIS_INTERVAL_ORIGIN="start"  # see http://vocab.ices.dk/?ref=1457
export PING_AXIS_INTERVAL_UNIT="nmi"  # see http://vocab.ices.dk/?ref=1456
export PING_AXIS_INTERVAL=0.1
export CHANNEL_DEPTH_START=0
export CHANNEL_DEPTH_END=500
export CHANNEL_THICKNESS=5
export CHANNEL_TYPE='depth'
export CLASSTRHRESHOLD=0.8
export SV_THRESHOLD=-100
export TYPE="C"  # C = sA, Nautical area scattering coefficient
export UNIT="m2nmi-2"  # see http://vocab.ices.dk/?ref=1460 |
export MAIN_FREQ=38000  # The frequency to integrate (could be a list in the future)
export OUTPUT_TYPE='zarr'

# Sand eel test set Unet prediction
docker run  -it --rm --name unet \
       -v "${DATAIN}":/datain \
       -v "${MODEL}":/model -v "${DATAOUT}/ACOUSTIC/PREDICTIONS/":/dataout \
       --security-opt label=disable \
       --env MODEL=$MODELFILE \
       --env SURVEY=$SURVEY \
       --env ZARRFILE=$PREDICTIONFILE_2 \
       unet:latest

# Sand eel test set work file reportgenerator
docker run -it --rm --name reportgenerator \
       -v "${DATAIN}ACOUSTIC/GRIDDED":/datain \
       -v "${DATAIN}ACOUSTIC/GRIDDED":/predin \
       -v "${DATAOUT}ACOUSTIC/REPORTS"/:/dataout \
       --security-opt label=disable \
       --env SURVEY=$SURVEY \
       --env PREDICTIONFILE=$PREDICTIONFILE_1 \
       --env REPORTFILE=$REPORTFILE_1 \
       --env THRESHOLD=$THRESHOLD \
       --env PING_AXIS_INTERVAL_TYPE=$PING_AXIS_INTERVAL_TYPE \
       --env PING_AXIS_INTERVAL_ORIGIN=$PING_AXIS_INTERVAL_ORIGIN \
       --env PING_AXIS_INTERVAL_UNIT=$PING_AXIS_INTERVAL_UNIT \
       --env PING_AXIS_INTERVAL=$PING_AXIS_INTERVAL \
       --env CHANNEL_THICKNESS=$CHANNEL_THICKNESS \
       --env CHANNEL_TYPE=$CHANNEL_TYPE \
       --env CHANNEL_DEPTH_START=$CHANNEL_DEPTH_START \
       --env CHANNEL_DEPTH_END=$CHANNEL_DEPTH_END \
       --env OUTPUT_TYPE=$OUTPUT_TYPE\
       crimac/reportgeneration:latest

# Sand eel test set Unet reportgenerator
docker run -it --rm --name reportgenerator \
       -v "${DATAIN}/ACOUSTIC/GRIDDED":/datain \
       -v "${DATAIN}/ACOUSTIC/PREDICTIONS":/predin \
       -v "${DATAOUT}/ACOUSTIC/REPORTS"/:/dataout \
       --security-opt label=disable \
       --env SURVEY=$SURVEY \
       --env PREDICTIONFILE=$PREDICTIONFILE_2 \
       --env REPORTFILE=$REPORTFILE_2 \
       --env THRESHOLD=$THRESHOLD \
       --env CLASSTRHRESHOLD=$CLASSTRHRESHOLD \
       --env PING_AXIS_INTERVAL_TYPE=$PING_AXIS_INTERVAL_TYPE \
       --env PING_AXIS_INTERVAL_ORIGIN=$PING_AXIS_INTERVAL_ORIGIN \
       --env PING_AXIS_INTERVAL_UNIT=$PING_AXIS_INTERVAL_UNIT \
       --env PING_AXIS_INTERVAL=$PING_AXIS_INTERVAL \
       --env CHANNEL_THICKNESS=$CHANNEL_THICKNESS \
       --env CHANNEL_TYPE=$CHANNEL_TYPE \
       --env CHANNEL_DEPTH_START=$CHANNEL_DEPTH_START \
       --env CHANNEL_DEPTH_END=$CHANNEL_DEPTH_END \
       crimac/reportgeneration:latest
