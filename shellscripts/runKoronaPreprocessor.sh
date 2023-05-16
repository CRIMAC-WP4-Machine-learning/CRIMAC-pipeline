#!/bin/bash
echo -------------------------------
echo This code runs the Korona preprocessor
echo -------------------------------
echo
# https://codefather.tech/blog/bash-functions/

#The ping time is '2016-05-09T12:52:48.782571000' from 2016 sandeel survey (survey number= 2016837).

DATAIN='/gpfs/gpfs0/cruise_data/2009/S2009206_PJOHANHJORT_1019/ACOUSTIC_DATA/EK60/EK60_RAWDATA/'
DATAOUT='/gpfs/gpfs0/crimac-scratch/2009/S2009206/ACOUSTIC/GRIDDED/'
SURVEY='S2009206'

docker run -it --rm \
  -v "${DATAIN}":/datain \
  -v "${DATAOUT}":/dataout \
  --security-opt label=disable \
  --env STEP=1 \
  --env TYPE=cw_sv \
  --env OUTPUT_NAME=$SURVEY \
  crimac-preprocessor-korona
  
docker run -it --rm \
  -v "${DATAIN}":/datain \
  -v "${DATAOUT}":/dataout \
  --security-opt label=disable \
  --env STEP=2 \
  --env TYPE=cw_sv \
  --env OUTPUT_NAME=$SURVEY \
  crimac-preprocessor-korona
