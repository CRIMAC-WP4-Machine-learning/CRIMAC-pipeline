#!/bin/zsh
echo Hi
# Sand eel survey
docker run -it --rm --name unet -v "/mnt/c/DATAscratch/crimac-scratch/2019/S2019847_0511/":/datain -v "/mnt/c/DATAscratch/crimac-scratch/NR_Unet":/model -v "/mnt/c/DATAscratch/crimac-scratch/2019/S2019847_0511/ACOUSTIC/PREDICTIONS/":/dataout --security-opt label=disable --env MODEL="paper_v2_heave_2.pt" --env SURVEY=S2019847_0511 --env ZARRFILE=S2019847_0511_predictions_2.zarr unet:latest

