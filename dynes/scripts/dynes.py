# -*- coding: utf-8 -*-

import os
import json
from argparse import ArgumentParser
import pandas

import dynes.scripts.build as build
import dynes.scripts.run as run
import dynes.scripts.postprocess as postprocess

def dynes(settings, materials, layers, bedrock, eqdata, path_analysis):

    print("Writing input data files...")
    eqdata = build.write_eq(eqdata, path_analysis)
    build.write_dynes(settings, materials, layers, bedrock, eqdata, path_analysis)
    build.write_post(settings, path_analysis)
    print("\t\tFINISHED!")
    
    print("Running DYNES analysis...")
    run.dynes(path_analysis)
    print("\t\tFINISHED!")
    print("Running DYNES postprocessing...")
    run.pstdynes(path_analysis)
    print("\t\tFINISHED!")

    print("Extracting results...")
    postprocess.extract_results(path_analysis)
    print("\t\tFINISHED!")
    print("Caclulating response spectrum...")
    postprocess.calc_spect(path_analysis)
    print("\t\tFINISHED!")
    print("Plotting results...")
    postprocess.plot_results(path_analysis, layers)
    print("\t\tFINISHED!")


def load_inputs(path_settings, path_materials, path_layers, path_bedrock, path_eqdata):

    settings_df = pandas.read_csv(path_settings, header=None, index_col=0)
    settings = settings_df[1].to_dict()

    materials_df = pandas.read_csv(path_materials, header=0, skiprows=[1])
    materials = materials_df.to_dict(orient='records')

    layers_df = pandas.read_csv(path_layers, header=0, skiprows=[1])
    layers = layers_df.to_dict(orient='records')

    bedrock_df = pandas.read_csv(path_bedrock, header=None, index_col=0)
    bedrock = bedrock_df[1].to_dict()

    eqdata_df = pandas.read_csv(path_eqdata, header=None, index_col=0)
    eqdata = eqdata_df[1].to_dict()

    return settings, materials, layers, bedrock, eqdata


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
    if not os.path.isdir(os.path.join(driver['analysis_folder'], 'output')):
        os.mkdir(os.path.join(os.getcwd(), driver['analysis_folder'], 'output'))

    # Load input files
    settings, materials, layers, bedrock, eqdata = load_inputs(driver['path_settings'], driver['path_materials'], driver['path_layers'], driver['path_bedrock'], driver['path_eqdata'])

    # Call dynes fucntion to run all tasks
    dynes(settings, materials, layers, bedrock, eqdata, driver['analysis_folder'])