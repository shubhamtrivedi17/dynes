# -*- coding: utf-8 -*-

import os
import json
from argparse import ArgumentParser

import dynes.scripts.build as build
import dynes.scripts.run as run
import dynes.scripts.postprocess as postprocess

def dynes(driver):

    build.write_dynes(
        settings=driver['path_settings'],
        materials=driver['path_materials'],
        layers=driver['path_layers'],
        bedrock=driver['path_bedrock'],
        eqdata=driver['path_eqdata'],
        folder_path=driver['path_folder'])
    build.write_post(
        settings=driver['path_settings'],
        folder_path=driver['path_folder']
    )
    
    run.dynes(driver['path_folder'])
    run.pstdynes(driver['path_folder'])

    postprocess.extract_results(driver['path_folder'])


def main():

    # Parse command line arguments
    parser = ArgumentParser()
    required = parser.add_argument_group('required named arguments')
    required.add_argument("-d", "--driver-file", dest="driver_file", help="Driver input file")
    args = parser.parse_args()

    # Load driver file
    driver_file = args.driver_file
    with open(driver_file, "r") as f:
        driver = json.load(f)

    # Create analysis folder
    os.pa

    # Call dynes fucntion to run all tasks
    dynes(driver)