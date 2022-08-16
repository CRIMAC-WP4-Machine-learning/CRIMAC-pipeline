#!/bin/bash
scp -r /localscratch_hdd/nilsolav/2007/S2007205/ACOUSTIC/PREDICTIONS/S2007205_predictions_2.zarr nilsolav@dedun.hi.no:/data/crimac-scratch/2007/S2007205/ACOUSTIC/PREDICTIONS/S2007205_predictions_2.zarr

function move_predictions() {
    echo -------------------------------
    echo This code runs the sand eel survey reports
    echo -------------------------------
    echo scp -r /localscratch_hdd/nilsolav/${YEAR}/${SURVEY}/ACOUSTIC/PREDICTIONS/${SURVEY}_predictions_2.zarr nilsolav@dedun.hi.no:/data/crimac-scratch//${YEAR}/${SURVEY}/ACOUSTIC/PREDICTIONS/${SURVEY}_predictions_2.zarr

YEAR='2007'
SURVEY='S2007205'
move_predictions

YEAR='2008'
SURVEY='S2008205'
move_predictions
