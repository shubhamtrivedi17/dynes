# -*- coding: utf-8 -*-

import os
import json
from argparse import ArgumentParser
import pandas

import dynes.scripts.build as build
import dynes.scripts.run as run
import dynes.scripts.postprocess as postprocess

def dynes(settings, bedrock, eqdata, layers, materials, path_analysis):

    build.write_dynes(settings, bedrock, eqdata, layers, materials, path_analysis)
    build.write_post(settings, path_analysis)
    
    run.dynes(path_analysis)
    run.pstdynes(path_analysis)

    postprocess.extract_results(path_analysis)


def load_inputs(path_settings, path_materials, path_layers, path_bedrock, path_eqdata):

    settings_df = pandas.read_csv("input_settings.csv", header=None, index_col=0)
    settings = settings_df[1].to_dict()

    bedrock_df = pandas.read_csv("input_bedrock.csv", header=None, index_col=0)
    bedrock = bedrock_df[1].to_dict()

    eqdata_df = pandas.read_csv("input_eqdata.csv", header=None, index_col=0)
    eqdata = eqdata_df[1].to_dict()

    layers_df = pandas.read_csv("input_layers.csv", header=0, skiprows=[1])
    layers = layers_df.to_dict(orient='records')

    materials_df = pandas.read_csv("input_materials.csv", header=0, skiprows=[1])
    materials = materials_df.to_dict(orient='records')

    return settings, bedrock, eqdata, layers, materials


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
    if not os.path.isdir(driver['analysis_folder']):
        os.mkdir(os.path.join(os.getcwd(), driver['analysis_folder']))

    # Load input files
    settings, bedrock, eqdata, layers, materials = load_inputs(driver['path_settings'], driver['path_materials'], driver['path_layers'], driver['path_bedrock'], driver['path_eqdata'])

    # Call dynes fucntion to run all tasks
    dynes(settings, bedrock, eqdata, layers, materials, driver['analysis_folder'])