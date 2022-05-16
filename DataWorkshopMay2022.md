CRIMAC data workshop
====================
May 18th 2022 09:00 at meeting room Pynten, Nordnes, Bergen.

https://goo.gl/maps/yoD4gRDQ5pktXNbx7

# Preparations

## Software

### git

Install ‘git’ and learn the operations ‘git clone’ and ‘git pull’. If you plan on working with the CRIMAC repositories you also need to learn ‘git add’, ‘git commit’ and ‘git push’. This is a useful resource:
https://education.github.com/git-cheat-sheet-education.pdf

### Github

You need a user on github. Most of the code is hosted under:
https://github.com/CRIMAC-WP4-Machine-learning/ 

You need to request access to these private repositories:
https://github.com/CRIMAC-WP4-Machine-learning/CRIMAC-Visualization
https://github.com/CRIMAC-WP4-Machine-learning/CRIMAC-data-organisation

### Python

Install python on your local computer.

Install these packages:
conda install -c plotly pandas ipywidgets xarray zarr datashader pyarrow fastparquet matplotlib pytorch

conda install -c pyviz holoviews bokeh

### Docker

The different processing steps are included in docker images. This can be used for deploying the software. We will not focus on docker during the workshop and we aim to run the code directly in python. But for the more nerdily inclined you may try it out by installing docker.
https://www.docker.com/ 

## Download test data

Download these test data sets:
https://marineseq.hi.no/crimac/

•	Testdata set (Sand eel, school boxes)
https://marineseq.hi.no/crimac/files/data/S2019847_0511.zip

•	Herring data (layers)
https://marineseq.hi.no/crimac/files/data/S2019842.zip

•	Sand eel data (school boxes)
https://marineseq.hi.no/crimac/files/data/S2019847.zip

The data should be organized according to the naming convention here:
https://github.com/CRIMAC-WP4-Machine-learning/CRIMAC-data-organisation 

If you would like to use own data (LSSS interpretations +  EK60/80 raw files) you need to run the preprocessor on the data:
https://github.com/CRIMAC-WP4-Machine-learning/CRIMAC-preprocessing 

## Reading list

### Xarray

You need an understanding of xarray: https://docs.xarray.dev/en/stable/
This video seems basic and good (but feel free to suggest another):
https://www.youtube.com/watch?v=xdrcMi_FB8Q 

### Holoviz

Holoviz is a suite of nice plotting tools that we can use directly on top of xarray: https://holoviz.org/
I made a simple example that you can use as a starting point:
https://github.com/CRIMAC-WP4-Machine-learning/CRIMAC-Visualization 

### Papers to read
We will use this network in the 2nd part of the WK:
Brautaset, O., Waldeland, A. U., Johnsen, E., Malde, K., Eikvil, L., Salberg, A.-B., and Handegard, N. O. 2020. Acoustic classification in multifrequency echosounder data using deep convolutional neural networks. ICES Journal of Marine Science, 77: 1391–1400. https://academic.oup.com/icesjms/advance-article/doi/10.1093/icesjms/fsz235/5712978 (Accessed 29 January 2020).


# Program

## Part 1 - Reading data and exploring xarray

-Reading and accessing the data

-Short presentation of manual data annotations to layers and school boxes

-Subsetting data based on annotations using xarray

## Part 2 - Setting up the u-net and train on test data

### Short presentation of the U-net algorithm

### Get the U-net code

`git clone https://github.com/CRIMAC-WP4-Machine-learning/CRIMAC-classifiers-unet`

The code is stored under the `NR_UNet` branch

`git checkout NR_UNet`

Now we should have a local copy of the code.

## Part 3 - Integration (probably for next workshop)
