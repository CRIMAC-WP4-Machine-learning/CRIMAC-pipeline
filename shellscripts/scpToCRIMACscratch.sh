#!/bin/bash

function move_predictions() {
    echo -------------------------------
    echo Moves predicitons from ${SURVEY} 
    echo -------------------------------
    scp -r /localscratch_hdd/nilsolav/${YEAR}/${SURVEY}/ACOUSTIC/PREDICTIONS/${SURVEY}_predictions_2.zarr \
            nilsolav@dedun.hi.no:/data/crimac-scratch//${YEAR}/${SURVEY}/ACOUSTIC/PREDICTIONS/${SURVEY}_predictions_2.zarr
}

function move_reports() {
    echo -------------------------------
    echo Moves reports from ${SURVEY} 
    echo -------------------------------
    scp -r /localscratch_hdd/nilsolav/${YEAR}/${SURVEY}/ACOUSTIC/REPORTS/${SURVEY}report_2.zarr \
        nilsolav@dedun.hi.no:/data/crimac-scratch//${YEAR}/${SURVEY}/ACOUSTIC/REPORTS/${SURVEY}_report_2.zarr
    scp -r /localscratch_hdd/nilsolav/${YEAR}/${SURVEY}/ACOUSTIC/REPORTS/${SURVEY}report_1.zarr \
        nilsolav@dedun.hi.no:/data/crimac-scratch//${YEAR}/${SURVEY}/ACOUSTIC/REPORTS/${SURVEY}_report_1.zarr

    scp /localscratch_hdd/nilsolav/${YEAR}/${SURVEY}/ACOUSTIC/REPORTS/${SURVEY}report_2.zarr.csv \
        nilsolav@dedun.hi.no:/data/crimac-scratch//${YEAR}/${SURVEY}/ACOUSTIC/REPORTS/${SURVEY}_report_2.zarr.csv
    scp /localscratch_hdd/nilsolav/${YEAR}/${SURVEY}/ACOUSTIC/REPORTS/${SURVEY}report_1.zarr.csv \
        nilsolav@dedun.hi.no:/data/crimac-scratch//${YEAR}/${SURVEY}/ACOUSTIC/REPORTS/${SURVEY}_report_1.zarr.csv


}

SURVEY='S2019847_0511'
YEAR='2019'
move_predictions
#move_reports

YEAR='2007'
SURVEY='S2007205'
move_predictions
#move_reports

YEAR='2008'
SURVEY='S2008205'
move_predictions
#move_reports
