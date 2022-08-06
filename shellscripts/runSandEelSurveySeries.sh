#!/bin/bash
# This code runs the sand eel survey predictions
# 

# https://codefather.tech/blog/bash-functions/


HST=$(hostname)
MODELFILE='regriddingPaper_v1_baseline.pt'

echo
echo -------------------------------
echo Static variables for report genertor
echo -------------------------------
echo
PING_AXIS_INTERVAL_TYPE="distance"  # see http://vocab.ices.dk/?ref=1455
echo PING_AXIS_INTERVAL_TYPE__: $PING_AXIS_INTERVAL_TYPE
PING_AXIS_INTERVAL_ORIGIN="start"  # see http://vocab.ices.dk/?ref=1457
echo PING_AXIS_INTERVAL_ORIGIN: $PING_AXIS_INTERVAL_ORIGIN
PING_AXIS_INTERVAL_UNIT="nmi"  # see http://vocab.ices.dk/?ref=1456
echo PING_AXIS_INTERVAL_UNIT__: $PING_AXIS_INTERVAL_UNIT
PING_AXIS_INTERVAL=0.1
echo PING_AXIS_INTERVAL_______: $PING_AXIS_INTERVAL
CHANNEL_DEPTH_START=0
echo CHANNEL_DEPTH_START______: $CHANNEL_DEPTH_START
CHANNEL_DEPTH_END=500
echo CHANNEL_DEPTH_END________: $CHANNEL_DEPTH_END
CHANNEL_THICKNESS=5
echo CHANNEL_THICKNESS________: $CHANNEL_THICKNESS
CHANNEL_TYPE='depth'
echo CHANNEL_TYPE_____________: $CHANNEL_TYPE
CLASSTRHRESHOLD=0.8
echo CLASSTRHRESHOLD__________: $CLASSTRHRESHOLD
SV_THRESHOLD=-100
echo SV_THRESHOLD_____________: $SV_THRESHOLD
TYPE="C"  # C = sA, Nautical area scattering coefficient
echo TYPE_____________________: $TYPE
UNIT="m2nmi-2"  # see http://vocab.ices.dk/?ref=1460 |
echo UNIT_____________________: $UNIT
MAIN_FREQ=38000  # The frequency to integrate (could be a list in the future)
echo MAIN_FREQ________________: $MAIN_FREQ
OUTPUT_TYPE='zarr'
echo OUTPUT_TYPE______________: $OUTPUT_TYPE


function run_survey() {
    #HST=$1
    #MODELFILE=$2
    #SURVEY=$3
    #YEAR=$4
    echo
    echo -------------------------------
    VAR1="HI-14667"
    if [ "$VAR1" = "$HST" ]; then
	echo Running survey $SURVEY "HI-14667 setup:"
	DATAIN='/mnt/c/DATAscratch/crimac-scratch/'$YEAR'/'$SURVEY'/'
	DATAOUT='/mnt/c/DATAscratch/crimac-scratch/'$YEAR'/'$SURVEY'/'
	MODEL='/mnt/c/DATAscratch/crimac-scratch/NR_Unet/'
	
    else
	echo Running survey $SURVEY "pallas setup:"
	DATAIN='/localscratch_hdd/crimac/'$YEAR'/'$SURVEY'/'
	DATAOUT='/localscratch_hdd/nilsolav/'$YEAR'/'$SURVEY'/'
	MODEL='/localscratch_hdd/nilsolav/modelweights/'
    fi
    echo -------------------------------
    echo
    echo Folders:
    echo Datain__: $DATAIN
    echo Dataout_: $DATAOUT
    echo Model___: $MODEL

    PREDICTIONFILE_1=${SURVEY}_labels.zarr
    REPORTFILE_1=${SURVEY}_report_1.zarr
    PREDICTIONFILE_2=${SURVEY}_predictions_2.zarr
    REPORTFILE_2=${SURVEY}_report_2.zarr
    echo 
    echo Files:
    echo LSSS labels:________________: $PREDICTIONFILE_1
    echo Report from LSSS labels_____: $REPORTFILE_1
    echo Unet preditions:____________: $PREDICTIONFILE_2
    echo Report from Unet predictions: $REPORTFILE_2
    echo
    echo Unet predictions:
    docker run  -it --rm --name unet \
	       -v "${DATAIN}":/datain \
	       -v "${MODEL}":/model -v "${DATAOUT}/ACOUSTIC/PREDICTIONS/":/dataout \
	       --security-opt label=disable \
	       --env MODEL=$MODELFILE \
	       --env SURVEY=$SURVEY \
	       --env ZARRFILE=$PREDICTIONFILE_2 \
	       unet:latest
    echo
    echo LSSS work file reportgenerator:
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
    echo
    echo Unet reportgenerator:
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
}

# Run the testsurvey
SURVEY='S2019847_0511'
YEAR='2019'
run_survey

# Run the sand eel series
SURVEY='S2019847'
YEAR='2019'
run_survey

YEAR='2005'
SURVEY='2005205'
run_survey

YEAR='2006'
SURVEY='2006207'
run_survey

YEAR='2007'
SURVEY='2007205'
run_survey

YEAR='2008'
SURVEY='2008205'
run_survey

YEAR='2009'
SURVEY='2009107'
run_survey

YEAR='2010'
SURVEY='2010205'
run_survey

YEAR='2011'
SURVEY='2011206'
run_survey

YEAR='2012'
SURVEY='2012837'
run_survey

YEAR='2013'
SURVEY='2013842'
run_survey
YEAR='2014'
SURVEY='2014807'
run_survey

YEAR='2015'
SURVEY='2015837'
run_survey

YEAR='2016'
SURVEY='2016837'
run_survey

YEAR='2017'
SURVEY='2017843'
run_survey

YEAR='2018'
SURVEY='2018823'
run_survey

YEAR='2019'
SURVEY='2019847'
run_survey

YEAR='2020'
SURVEY='2020821'

run_survey
YEAR='2021'
SURVEY='2021847'

run_survey
#YEAR='2022'
#SURVEY='2021847'



