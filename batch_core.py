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
import shutil
import docker

import batch_config as config

class Pipeline:
    @classmethod
    def extract_cruise_series(cls, xmlfile, cruise_series_code = 13):
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        # Set the namespace
        ns = {'ns1': 'http://www.imr.no/formats/nmdreference/v2.1'}
        # Placeholder for the cruises
        target_cruises = []
        # Get the cruises for a series
        target_cruises = {}
        for elem in root.findall('.//ns1:row/[ns1:code="'+ str(cruise_series_code)
                    + '"]/ns1:samples/ns1:sample', ns):
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
                            ship_name = ''.join([i for i in subsubelem.text if i.isalpha()])
                    # Append to list
                    cruise_path = list(Path(config.ROOT_DIR + "/" + year)
                                    .glob("*" + cruise_no.upper() + "*" + ship_name.upper() + "*"))
                    if len(cruise_path) > 0:
                        print(cruise_path)
                        target_cruises[year] = [cruise_no, ship_name, cruise_path[0]]
        return target_cruises

    @classmethod
    def check_create_dir(cls, target_dir):
        target = Path(target_dir)
        if not target.exists():
            print("Creating output directory: " + str(target))
            target.mkdir()
        else:
            print("Using an existing output directory: " + str(target))

    @classmethod
    def check_overwrite_file(cls, target_file, overwrite_string):
        if overwrite_string.lower() == "yes":
            overwrite = True
        else:
            overwrite = False
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
            print("Not overwriting target: " + str(target))
            return False
        return True

    @classmethod
    def check_raw_data(cls, target_dir):
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

    @classmethod
    def get_ext_data_type(cls, data_type):
        if data_type == "zarr":
            return "zarr"
        if data_type == "netcdf4":
            return "nc"
        return None

    def launch_docker(self, image_tag, mount_list, environments, use_nvidia = False):
        '''
        Launch docker

        Parameters:
            image_tag (str)    : Image name to run.
            mount_list (str)   : Mount list.
            environments (str) : Environment list.
        '''

        print(environments)
        print(mount_list)

        if use_nvidia:
            container = self.client.containers.run(image_tag,
                detach = True,
                auto_remove = True,
                volumes=mount_list,
                environment=environments,
                runtime = "nvidia",
            )
        else:
            container = self.client.containers.run(image_tag,
                detach = True,
                auto_remove = True,
                volumes=mount_list,
                environment=environments
            )

        process = container.logs(stream=True, follow=True)
        print('Stream logging the container..')
        for line in process:
            print(line)

    @classmethod
    def gen_prefix(cls, output_prefix, p):
        # Check if prefix none or "" get the cruise number as the output_prefix
        if output_prefix is None or output_prefix == "":
            prefix, _, _ = p.name.partition('_')
        else:
            prefix = output_prefix
        return prefix

    def do_preprocessing(self, target):
        print("\n\nTrying to do pre-processing (gridding) for " + str(target))
        raw_data = self.check_raw_data(target)
        # Check data sanity
        if raw_data['raw_type'] is None or raw_data['path'] is None:
            print("ERROR: Invalid RAW data found!")
            return False
        # Check EK80 data
        if raw_data['raw_type'] == "ek80" and not config.PREPROCESSOR_PROCESS_EK80:
            print("Not processing EK80 data.")
            return False
        #print(target / raw_data['path'])
        if (target / raw_data['path']).exists():
            # Data input
            datain = target / raw_data['path']
            datawork = target / config.FIRST_LEVEL_DIR / "LSSS" / "WORK"

            # Make necessary directory and whether to overwrite files
            self.check_create_dir(self.preprocessor_out_dir)
            proceed = self.check_overwrite_file(self.preprocessor_out_path, config.PREPROCESSOR_OVERWRITE)
            self.check_overwrite_file(self.preprocessor_work_path, config.PREPROCESSOR_OVERWRITE)

            # Prepare docker
            image_tag = config.PREPROCESSOR_IMAGE
            mount_list = {
                datain: {'bind': '/datain', 'mode': 'ro'},
                datawork: {'bind': '/workin', 'mode': 'ro'},
                self.preprocessor_out_dir: {'bind': '/dataout', 'mode': 'rw'}
            }
            environments = [
                "OUTPUT_NAME=" + self.preprocessor_out_name,
                "OUTPUT_TYPE=" + config.PREPROCESSOR_OUT_TYPE,
                "MAIN_FREQ=" + str(config.PREPROCESSOR_MAIN_FREQ),
                "MAX_RANGE_SRC=" + str(config.PREPROCESSOR_MAX_RANGE_SRC),
                "WRITE_PNG=" + config.PREPROCESSOR_WRITE_PNG
            ]
            if proceed:
                self.launch_docker(image_tag, mount_list, environments)
                return True
            return False
        print("ERROR: RAW data not found!")
        return False

    def do_prediction(self, target):
        print("\n\nTrying to do prediction for " + str(target))
        if (self.preprocessor_out_path).exists():
            self.check_create_dir(self.predictor_out_dir)
            proceed = self.check_overwrite_file(self.predictor_out_path, config.PREDICTOR_OVERWRITE)

            # Prepare docker
            image_tag = config.PREDICTOR_IMAGE
            # If input is netcdf
            if self.preprocessor_out_ext != "zarr":
                print("ERROR for now!")

            mount_list = {
                self.preprocessor_out_dir: {'bind': '/datain', 'mode': 'ro'},
                self.predictor_out_dir: {'bind': '/dataout', 'mode': 'rw'},
                self.predictor_model_path: {'bind': '/model', 'mode': 'ro'}
            }
            environments = [
                "OUTPUT_NAME=" + self.predictor_out_name,
            ]
            if proceed:
                self.launch_docker(image_tag, mount_list, environments, config.PREDICTOR_USE_CUDA)
                return True
            return False
        print("ERROR: Gridded data not found! Please do preprocessing first.")
        return False

    def do_bottom_detection(self, target):
        print("\n\nTrying to do bottom detection for " + str(target))
        if (self.preprocessor_out_path).exists():
            # Get extension
            self.check_create_dir(self.bottomdetection_out_dir)
            proceed = self.check_overwrite_file(self.bottomdetection_out_path, config.BOTTOMDETECTION_OVERWRITE)

            # Prepare docker
            image_tag = config.BOTTOMDETECTION_IMAGE

            mount_list = {
                self.preprocessor_out_dir: {'bind': '/in_dir', 'mode': 'rw'},
                self.bottomdetection_out_dir: {'bind': '/out_dir', 'mode': 'rw'}
            }

            environments = [
                "INPUT_NAME=" + self.preprocessor_out_name,
                "OUTPUT_NAME=" + self.bottomdetection_out_name,
                "ALGORITHM=" + config.BOTTOMDETECTION_ALGORITHM,
                "PARAMETER_minimum_range=" + str(config.BOTTOMDETECTION_PARAMETER_MINIMUM_RANGE),
                "PARAMETER_offset=" + str(config.BOTTOMDETECTION_PARAMETER_OFFSET),
                "PARAMETER_threshold_log_sv=" + str(config.BOTTOMDETECTION_PARAMETER_THRESHOLD_LOG_SV)
            ]

            if proceed:
                self.launch_docker(image_tag, mount_list, environments)
                return True
            return False
        print("ERROR: Gridded data not found! Please do preprocessing first.")
        return False

    def do_integration(self, target):
        print("\n\nTrying to do integration for " + str(target))
        if (self.preprocessor_out_path).exists() and (self.bottomdetection_out_path).exists() and (self.predictor_out_path).exists():

            # Prepare output
            self.check_create_dir(self.integrator_out_dir)
            proceed = self.check_overwrite_file(self.integrator_out_path, config.INTEGRATOR_OVERWRITE)
            self.check_overwrite_file(self.integrator_png_path, config.INTEGRATOR_OVERWRITE)

            # Prepare docker
            image_tag = config.INTEGRATOR_IMAGE

            mount_list = {
                self.preprocessor_out_dir: {'bind': '/datain', 'mode': 'ro'},
                self.predictor_out_dir: {'bind': '/predin', 'mode': 'ro'},
                self.bottomdetection_out_dir: {'bind': '/botin', 'mode': 'ro'},
                self.integrator_out_dir: {'bind': '/dataout', 'mode': 'rw'}
            }

            environments = [
                "DATA_INPUT_NAME=" + self.preprocessor_out_name,
                "PRED_INPUT_NAME=" + self.predictor_out_name,
                "BOT_INPUT_NAME=" + self.bottomdetection_out_name,
                "OUTPUT_NAME=" + self.integrator_out_name,
                "WRITE_PNG=" + self.integrator_png_name,
                "THRESHOLD=" + str(config.INTEGRATOR_THRESHOLD),
                "MAIN_FREQ=" + str(config.INTEGRATOR_MAIN_FREQ),
                "MAX_RANGE_SRC=" + str(config.INTEGRATOR_MAX_RANGE_SRC),
                "HOR_INTEGRATION_TYPE=" + config.INTEGRATOR_HOR_INTEGRATION_TYPE,
                "HOR_INTEGRATION_STEP=" + str(config.INTEGRATOR_HOR_INTEGRATION_STEP),
                "VERT_INTEGRATION_TYPE=" + config.INTEGRATOR_VERT_INTEGRATION_TYPE,
                "VERT_INTEGRATION_STEP=" + str(config.INTEGRATOR_VERT_INTEGRATION_STEP)
            ]

            if proceed:
                self.launch_docker(image_tag, mount_list, environments)
                return True
            return False
        print("ERROR: Either gridded data / bottom detection / u-net prediction data not found!")
        return False

    def populate_paths(self, target, prefix):
        # Init directories and output files

        # Preprocessor
        self.preprocessor_out_dir = target / config.FIRST_LEVEL_DIR / config.GRIDDED_DATA_DIR
        self.preprocessor_out_ext = self.get_ext_data_type(config.PREPROCESSOR_OUT_TYPE)
        self.preprocessor_out_name = prefix
        self.preprocessor_out_path = self.preprocessor_out_dir / str(self.preprocessor_out_name + "." + self.preprocessor_out_ext)

        self.preprocessor_work_name = str(prefix + "_work.parquet")
        self.preprocessor_work_path = self.preprocessor_out_dir / self.preprocessor_work_name

        # Bottom detection
        self.bottomdetection_out_dir = target / config.FIRST_LEVEL_DIR / config.BOTTOM_DATA_DIR
        self.bottomdetection_out_ext = self.get_ext_data_type(config.BOTTOMDETECTION_OUT_TYPE)
        self.bottomdetection_out_name = str(prefix + "_pred_bottom" + "." + self.bottomdetection_out_ext)
        self.bottomdetection_out_path = self.bottomdetection_out_dir / self.bottomdetection_out_name

        # Predictor
        self.predictor_model_path = config.PREDICTOR_MODEL_PATH

        self.predictor_out_dir = target / config.FIRST_LEVEL_DIR / config.PREDICTOR_DATA_DIR
        self.predictor_out_ext = self.get_ext_data_type(config.PREDICTOR_OUT_TYPE)
        self.predictor_out_name = str(prefix + "_pred" + "." + self.predictor_out_ext)
        self.predictor_out_path = self.predictor_out_dir / self.predictor_out_name

        # Integrator
        self.integrator_out_dir = target / config.FIRST_LEVEL_DIR / config.INTEGRATOR_DATA_DIR
        self.integrator_out_ext = self.get_ext_data_type(config.INTEGRATOR_OUT_TYPE)
        self.integrator_out_name = str(prefix + "_report" + "." + self.integrator_out_ext)
        self.integrator_out_path = self.integrator_out_dir / self.integrator_out_name

        self.integrator_png_name = str(prefix + "_report.png")
        self.integrator_png_path = self.integrator_out_dir / self.integrator_png_name

    def do_batch(self, cruise_list):
        for _, _, _, p in cruise_list:
            print("Starting batch processing of cruise " + p)
            prefix = self.gen_prefix(config.GLOBAL_PREFIX, p)
            self.populate_paths(p, prefix)
            self.do_preprocessing(p)
            self.do_prediction(p)
            self.do_bottom_detection(p)
            print("\n")

    def __init__(self):
        # Init Docker
        self.client = docker.from_env()

        # Download images
        image_list = [config.PREPROCESSOR_IMAGE, config.PREDICTOR_IMAGE, config.BOTTOMDETECTION_IMAGE, config.INTEGRATOR_IMAGE]
        for img in image_list:
            print("Pulling the latest " + img + " image from docker hub...")
            self.client.images.pull(img)

        # Init Paths

        # Preprocessor
        self.preprocessor_out_dir = None
        self.preprocessor_out_ext = None
        self.preprocessor_out_name = None
        self.preprocessor_out_path = None

        self.preprocessor_work_name = None
        self.preprocessor_work_path = None

        # Bottom detection
        self.bottomdetection_out_dir = None
        self.bottomdetection_out_ext = None
        self.bottomdetection_out_name = None
        self.bottomdetection_out_path = None

        # Predictor
        self.predictor_model_path = None

        self.predictor_out_dir = None
        self.predictor_out_ext = None
        self.predictor_out_name = None
        self.predictor_out_path = None

        # Integrator
        self.integrator_out_dir = None
        self.integrator_out_ext = None
        self.integrator_out_name = None
        self.integrator_out_path = None

        self.integrator_png_name = None
        self.integrator_png_path = None
