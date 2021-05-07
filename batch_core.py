"""
CRIMAC Pipeline Script

Copyright (C) 2021, Ibrahim Umar and The Institute of Marine
Research, Norway.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""


from pathlib import Path, PurePath
import xml.etree.ElementTree as ET
import itertools
import shutil
import docker

def extract_cruise_series(xmlfile, cruise_series_code = 13):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    # Set the namespace
    ns = {'ns1': 'http://www.imr.no/formats/nmdreference/v2.1'}
    # Placeholder for the cruises
    target_cruises = []
    # Get the cruises for a series
    for elem in root.findall('.//ns1:row/[ns1:code="'+ str(cruise_series_code) + '"]/ns1:samples/ns1:sample', ns):
        # Get the year information
        for subelem in elem.findall(".//ns1:sampleTime", ns):
            year = subelem.text
        # Get the cruise number and ship name information
        for subelem in elem.findall(".//ns1:cruises", ns):
            for cruise_el in subelem.getchildren():
                for subsubelem in cruise_el.iter():
                    _, _, tag = subsubelem.tag.rpartition('}')
                    if tag == "cruisenr":
                        cruise_no = subsubelem.text
                    if tag == "shipName":
                        ship_name = subsubelem.text
                # Append to list
                target_cruises.append([year, cruise_no, ship_name])
    return(target_cruises)

def check_create_dir(target_dir):
    target = Path(target_dir)
    if not target.exists():
        print("Creating output directory: " + str(target))
        target.mkdir()
    else:
        print("Using an existing output directory: " + str(target))

def check_overwrite_file(target_file, overwrite):
    target = Path(target_file)
    #print(target)
    if target.exists():
        if overwrite:
            print("Removing existing target: " + str(target))
            if target.is_file():
                target.unlink()
            else:
                shutil.rmtree(target)
            return True
        else:
            print("Not overwriting target: " + str(target))
            return False
    else:
        return True


def check_raw_data(target_dir):
    path = None
    raw_type = None
    parent = Path(target_dir)
    # Get the raw data directory
    raws = list(parent.glob("*/*/*_RAWDATA"))
    for raw in raws:
        raw_loc = PurePath(raw)
        # Get the relative path
        path = raw_loc.relative_to(PurePath(parent))
        # Now check the type
        ## Get the first file
        tmp_raw = next(raw.glob("*.raw"), None)
        if tmp_raw is not None:
            break

    if tmp_raw is not None:
        ## Read the first 4 bytes
        with open(tmp_raw, 'rb') as f:
            header = f.read(7)[-3:]
            if header == b'CON':
                raw_type = 'ek60'
            elif header == b'XML':
                raw_type = 'ek80'
    return {'path': str(path), 'raw_type': raw_type}

def gen_path_list(cruise_list):
    paths = []
    for year, cruise_no, ship_name in cruise_list:
        paths.append(Path(root_dir + "/" + year).glob("*" + cruise_no.upper() + "*" + ship_name.upper() + "*"))
    return(paths)

def get_ext_data_type(data_type):
    if data_type == "zarr":
        return("zarr")
    elif data_type == "netcdf4":
        return("nc")
    else:
        return(None)

def launch_bottom_classifier(datain, dataout, algorithm, in_name, out_name):
    '''
    Launch bottom classifier image

    Parameters:
        datain (str)         : Directory path of the RAW files.
        dataout (str)        : Output directory.
        algorithm (str)      : Bottom classifier algorithm.
        prefix (str)         : Name of the output data.
        grid_data_type (str) : Output type, can be either 'zarr' or 'netcdf4'.

    '''

    mount_list = {
        datain: {'bind': '/in_dir', 'mode': 'rw'},
        dataout: {'bind': '/out_dir', 'mode': 'rw'}
    }
    environments = [
        "INPUT_NAME=" + in_name,
        "OUTPUT_NAME=" + out_name,
        "ALGORITHM=" + algorithm
    ]
    print(environments)
    print(mount_list)
    container = client.containers.run('crimac/bottomdetection',
            detach = True,
            auto_remove = True,
            volumes=mount_list,
            environment=environments,
    )
    process = container.logs(stream=True, follow=True)
    print('Stream logging the container..')
    for line in process:
        print(line)

def launch_unet_classifier(datain, dataout, model, prefix, grid_data_type):
    '''
    Launch unet classifier image to do preprocessing

    Parameters:
        datain (str)         : Directory path of the RAW files.
        dataout (str)        : Output directory.
        model (str)          : Directory path of the model files.
        prefix (str)         : Name of the output data.
        grid_data_type (str) : Output type, can be either 'zarr' or 'netcdf4'.

    '''

    mount_list = {
        datain: {'bind': '/datain', 'mode': 'rw'},
        model: {'bind': '/model', 'mode': 'rw'},
        dataout: {'bind': '/dataout', 'mode': 'rw'}
    }
    environments = [
        "OUTPUT_NAME=" + prefix,
    ]    
    print(environments)
    print(mount_list)
    container = client.containers.run('crimac/predictor',
            detach = True,
            auto_remove = True,
            volumes=mount_list,
            environment=environments,
            runtime="nvidia"
    )
    process = container.logs(stream=True, follow=True)
    print('Stream logging the container..')
    for line in process:
        print(line)

def launch_preprocessing(datain, datawork, dataout, prefix, grid_data_type):
    '''
    Launch docker preprocessor image to do preprocessing

    Parameters:
        datain (str)         : Directory path of the RAW files.
        datawork (str)       : Directory path of the LSSS WORK files.
        dataout (str)        : Output directory.
        prefix (str)         : Name of the output data.
        grid_data_type (str) : Output type, can be either 'zarr' or 'netcdf4'.

    '''

    mount_list = {
        datain: {'bind': '/datain', 'mode': 'rw'},
        datawork: {'bind': '/workin', 'mode': 'rw'},
        dataout: {'bind': '/dataout', 'mode': 'rw'}
    }
    environments = [
        "OUTPUT_TYPE=" + grid_data_type,
        "MAIN_FREQ=38000", 
        "MAX_RANGE_SRC=500",
        "OUTPUT_NAME=" + prefix,
        "WRITE_PNG=0",
    ]
    print(environments)
    print(mount_list)
    container = client.containers.run('crimac/preprocessor',
            detach = True,
            auto_remove = True,
            volumes=mount_list,
            environment=environments,
    )
    process = container.logs(stream=True, follow=True)
    print('Stream logging the container..')
    for line in process:
        print(line)

def do_preprocessing(target, prefix, grid_data_type, process_ek80, overwrite):
    print("\n\nTrying to do pre-processing (gridding) for " + str(target))
    raw_data = check_raw_data(target)
    # Check data sanity
    if raw_data['raw_type'] is None or raw_data['path'] is None:
        print("ERROR: Invalid RAW data found!")
        return(False)
    # Check EK80 data
    if raw_data['raw_type'] == "ek80" and not process_ek80:
        print("Not processing EK80 data.")
        return(False)
    #print(target / raw_data['path'])
    if (target / raw_data['path']).exists():
        # Get extension
        ext = get_ext_data_type(grid_data_type)
        datain = target / raw_data['path']
        dataout = target / first_level / gridded_data
        datawork = target / first_level / "LSSS" / "WORK"
        target_file = dataout / str(prefix + "." + ext)
        target_file_work = dataout / str(prefix + "_work.parquet")
        # Make necessary directory and whether to overwrite files
        check_create_dir(dataout)
        proceed = check_overwrite_file(target_file, overwrite)
        check_overwrite_file(target_file_work, overwrite)
        if proceed:
            launch_preprocessing(str(datain), str(datawork), str(dataout), prefix, grid_data_type)
            return True
        else:
            return False
    else:
        print("ERROR: RAW data not found!")
        return False

def do_prediction(target, prefix, grid_data_type, overwrite = False):
    print("\n\nTrying to do prediction for " + str(target))
    if (target / first_level / gridded_data).exists():
        # Get extension
        ext = get_ext_data_type(grid_data_type)
        datain = target / first_level / gridded_data
        dataout = target / first_level / prediction
        target_file_pred = dataout / str(prefix + "_pred.zarr")
        check_create_dir(dataout)
        proceed = check_overwrite_file(target_file_pred, overwrite)
        if proceed:
            launch_unet_classifier(str(datain), str(dataout), model =  "/scratch/disk2/AzureMirror/models/NR_Unet", prefix = prefix, grid_data_type = grid_data_type)
            return True
        else:
            return False
    else:
        print("ERROR: Gridded data not found! Please do preprocessing first.")
        return False

def do_bottom_detection(target, prefix, algorithm, grid_data_type, overwrite = False):
    print("\n\nTrying to do bottom detection for " + str(target))
    if (target / first_level / gridded_data).exists():
        # Get extension
        ext = get_ext_data_type(grid_data_type)
        datain = target / first_level / gridded_data
        dataout = target / first_level / bottom_detection
        in_name = prefix + "." + ext
        out_name = str(prefix + "_pred_bottom.parquet")
        target_file = dataout / out_name
        check_create_dir(dataout)
        proceed = check_overwrite_file(target_file, overwrite)
        if proceed:
            launch_bottom_classifier(str(datain), str(dataout), algorithm, in_name, out_name)
            return True
        else:
            return False
    else:
        print("ERROR: Gridded data not found! Please do preprocessing first.")
        return False

def do_batch(cruise_list, output_prefix = None, grid_data_type = 'zarr', bottom_detection_algorithm = "simple", process_ek80 = False, overwrite = False):
    paths = gen_path_list(cruise_list)
    for p in itertools.chain(*paths):
        # Check if prefix none or "" get the cruise number as the output_prefix
        if output_prefix is None or output_prefix == "":
            prefix, _, _ = p.name.partition('_')
        else:
            prefix = output_prefix
        print("Starting batch processing of cruise " + prefix)
        do_preprocessing(p, prefix, grid_data_type, process_ek80, overwrite)
        do_prediction(p, prefix, overwrite)
        do_bottom_detection(p, prefix, bottom_detection_algorithm, grid_data_type, overwrite)
        print("\n")

def init_docker_client():
    # Setup docker
    client = docker.from_env()
    return client

