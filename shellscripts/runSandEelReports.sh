#!/bin/bash
echo -------------------------------
echo This code runs the sand eel survey reports
echo -------------------------------
echo
# https://codefather.tech/blog/bash-functions/
HST=$(hostname)
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
    echo
    echo -------------------------------
    VAR1="HI-14667"
    if [ "$VAR1" = "$HST" ]; then
	echo Running survey $SURVEY "HI-14667 setup:"
	DATAIN='/mnt/c/DATAscratch/crimac-scratch/'$YEAR'/'$SURVEY'/'
	DATAOUT='/mnt/c/DATAscratch/crimac-scratch/'$YEAR'/'$SURVEY'/'
    else
	echo Running survey $SURVEY "pallas setup:"
	DATAIN='/localscratch_hdd/crimac/'$YEAR'/'$SURVEY'/'
	DATAOUT='/localscratch_hdd/nilsolav/'$YEAR'/'$SURVEY'/'
    fi
    echo -------------------------------
    PREDICTIONFILE_1=${SURVEY}_labels.zarr
    REPORTFILE_1=${SURVEY}_report_1.zarr
    PREDICTIONFILE_2=${SURVEY}_predictions_2.zarr
    REPORTFILE_2=${SURVEY}_report_2.zarr
    echo 
    echo Files:
    echo LSSS labels:________________: $PREDICTIONFILE_1
    echo Report from LSSS labels_____: $REPORTFILE_1
    echo
    echo -------------------------------
    echo UNET report generation on survey: $SURVEY 
    echo -------------------------------
    echo

    echo Inputdata:
    echo Raw data_________: ${DATAIN}/ACOUSTIC/GRIDDED/
    echo Unet predictions_: ${DATAOUT}/ACOUSTIC/PREDICTIONS/${PREDICTIONFILE_2}
    echo Reports__________: ${DATAOUT}/ACOUSTIC/REPORTS/${REPORTFILE_2}

    echo
    echo Unet reportgeneration:
#    docker run -it --rm --name reportgeneration \
#	   -v "${DATAIN}/ACOUSTIC/GRIDDED":/datain \
#	   -v "${DATAOUT}/ACOUSTIC/PREDICTIONS":/predin \
#	   -v "${DATAOUT}/ACOUSTIC/REPORTS"/:/dataout \
#	   --security-opt label=disable \
#	   --env SURVEY=$SURVEY \
#	   --env PREDICTIONFILE=$PREDICTIONFILE_2 \
#	   --env REPORTFILE=$REPORTFILE_2 \
#	   --env THRESHOLD=$THRESHOLD \
#	   --env CLASSTRHRESHOLD=$CLASSTRHRESHOLD \
#	   --env PING_AXIS_INTERVAL_TYPE=$PING_AXIS_INTERVAL_TYPE \
#	   --env PING_AXIS_INTERVAL_ORIGIN=$PING_AXIS_INTERVAL_ORIGIN \
#	   --env PING_AXIS_INTERVAL_UNIT=$PING_AXIS_INTERVAL_UNIT \
#	   --env PING_AXIS_INTERVAL=$PING_AXIS_INTERVAL \
#	   --env CHANNEL_THICKNESS=$CHANNEL_THICKNESS \
#	   --env CHANNEL_TYPE=$CHANNEL_TYPE \
#	   --env CHANNEL_DEPTH_START=$CHANNEL_DEPTH_START \
#	   --env CHANNEL_DEPTH_END=$CHANNEL_DEPTH_END \
#	   reportgeneration:latest
    echo
    echo -------------------------------
    echo LSSS work file reportgeneration on survey: $SURVEY 
    echo -------------------------------
    echo
    echo Inputdata:
    echo Raw data_________: ${DATAIN}/ACOUSTIC/GRIDDED/
    echo Unet predictions_: ${DATAIN}/ACOUSTIC/PREDICTIONS/${PREDICTIONFILE_1}
    echo Reports__________: ${DATAOUT}/ACOUSTIC/REPORTS/${REPORTFILE_1}

    docker run -it --rm --name reportgeneration \
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
	   reportgeneration:latest
    echo
}

# Run the testsurvey
SURVEY='S2019847_0511'
YEAR='2019'
#run_survey

# Run the sand eel series
YEAR='2007'
SURVEY='S2007205'
#run_survey

YEAR='2008'
SURVEY='S2008205'
#run_survey

YEAR='2009'
SURVEY='S2009107'
run_survey

YEAR='2010'
SURVEY='S2010205'
run_survey

YEAR='2011'
SURVEY='S2011206'
#run_survey

YEAR='2012'
SURVEY='S2012837'
#run_survey

YEAR='2013'
SURVEY='S2013842'
#run_survey

YEAR='2014'
SURVEY='S2014807'
#run_survey

YEAR='2015'
SURVEY='S2015837'
#run_survey

YEAR='2016'
SURVEY='S2016837'
#run_survey

YEAR='2017'
SURVEY='S2017843'
#run_survey

YEAR='2018'
SURVEY='S2018823'
#run_survey

YEAR='2019'
SURVEY='S2019847'
#run_survey

YEAR='2020'
SURVEY='S2020821'
#run_survey

YEAR='2021'
SURVEY='S2021847'
#run_survey

#YEAR='2022'
#SURVEY='2022xxx'
