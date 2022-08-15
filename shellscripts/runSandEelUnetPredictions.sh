#!/bin/bash
echo -------------------------------
echo This code runs the sand eel survey Unet predictions
echo -------------------------------
echo
# https://codefather.tech/blog/bash-functions/
HST=$(hostname)
MODELFILE='regriddingPaper_v1_baseline.pt'
echo MODELFILE: $MODELFILE
echo

function run_survey() {
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

    PREDICTIONFILE_2=${SURVEY}_predictions_2.zarr
    echo 
    echo Files:
    echo Unet preditions:____________: $PREDICTIONFILE_2
    echo
    echo Unet predictions:
    docker run  -it --rm --gpus all --name unet \
	       -v "${DATAIN}":/datain \
	       -v "${MODEL}":/model -v "${DATAOUT}/ACOUSTIC/PREDICTIONS/":/dataout \
	       --security-opt label=disable \
	       --env MODEL=$MODELFILE \
	       --env SURVEY=$SURVEY \
	       --env ZARRFILE=$PREDICTIONFILE_2 \
	       unet:latest
}

# Run the testsurvey
SURVEY='S2019847_0511'
YEAR='2019'
#run_survey

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
run_survey

YEAR='2012'
SURVEY='S2012837'
run_survey

YEAR='2013'
SURVEY='S2013842'
run_survey
YEAR='2014'
SURVEY='S2014807'
run_survey

YEAR='2015'
SURVEY='S2015837'
run_survey

YEAR='2016'
SURVEY='S2016837'
run_survey

YEAR='2017'
SURVEY='S2017843'
run_survey

YEAR='2018'
SURVEY='S2018823'
run_survey

YEAR='2019'
SURVEY='S2019847'
run_survey

YEAR='2020'
SURVEY='S2020821'
run_survey

YEAR='2021'
SURVEY='S2021847'
run_survey

#YEAR='2022'
#SURVEY='2022xxx'
