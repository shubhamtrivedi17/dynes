# -*- coding: utf-8 -*-

import glob
import numpy
import pandas
import pyrotd
import fortranformat as ff
import matplotlib.pyplot as pyplot


def extract_results(folder_path):

    ## Extract maximum response profile
    with open(f"{folder_path}\\dynes.max", 'r', encoding="utf-8") as file:
        _ = file.readline()
        n_lay = int(file.readline().split()[0])
        for _ in range(n_lay + 1 + n_lay):
            _ = file.readline()
        maxnoderesp = []
        reader = ff.FortranRecordReader('(I5, 9E15.8)')
        for idx in range(n_lay + 1):
            line = reader.read(file.readline())
            maxnoderesp.append(line)
        maxelemresp = []
        reader = ff.FortranRecordReader('(I5, 8E15.8)')
        for idx in range(n_lay):
            line = reader.read(file.readline())
            maxelemresp.append(line)

    maxnoderesp_df = pandas.DataFrame(maxnoderesp)
    maxnoderesp_df.columns = ['idx', 'acc_x', 'vel_x', 'dis_x', 'acc_y', 'vel_y', 'dis_y', 'acc_z', 'vel_z', 'dis_z']
    maxnoderesp_df.to_csv(f"{folder_path}\\output\\maxnoderesp.csv", index=False, encoding="utf-8")

    maxelemresp_df = pandas.DataFrame(maxelemresp)
    maxelemresp_df.columns = ['idx', 'strs_x', 'strs_y', 'overb', 'epwp', 'strn_x', 'strn_y', 'pres_x', 'pres_y']
    maxelemresp_df.to_csv(f"{folder_path}\\output\\maxelemresp.csv", index=False, encoding="utf-8")

    ## Extract response history data
    for quant in ['acc', 'stress', 'strain']:
        with open(f"{folder_path}\\dynes_{quant}.rsp", 'r', encoding="utf-8") as file:
            reader = ff.FortranRecordReader('(1P8E10.3)')
            _ = file.readline()
            data = []
            header = file.readline()
            layer = header.split("At Layer=")[1].split()[0]
            dt = float(header.split("DT=")[1].split()[0])
            datnum = int(header.split("Data=")[1].split()[0])
            for line in file:
                if "TIM" not in line.split():
                    line_data = reader.read(line)
                    data.extend([x for x in line_data if x is not None])
                else:
                    t_data = numpy.arange(0, datnum * dt, dt)
                    df = pandas.DataFrame({'time': t_data, quant: data})
                    df.to_csv(f"{folder_path}\\output\\{quant}_{layer}.csv", index=False, encoding="utf-8")
                    data = []
                    header = file.readline()
                    layer = header.split("At Layer=")[1].split()[0]
                    dt = float(header.split("DT=")[1].split()[0])
                    datnum = int(header.split("Data=")[1].split()[0])
                    continue
            t_data = numpy.arange(0, datnum * dt, dt)
            df = pandas.DataFrame({'time': t_data, quant: data})
            df.to_csv(f"{folder_path}\\output\\{quant}_{layer}.csv", index=False, encoding="utf-8")


def calc_spect(folder_path):

    ## Degine calculation parameters
    pyrotd.processes = 1
    osc_damping = 0.05
    osc_freqs = numpy.logspace(-1, 2, 501)
    osc_t = 1 / osc_freqs

    ## Calculate spectrum for each acceleration record
    for acc_file in glob.glob(f"{folder_path}\\output\\acc_*.csv"):
        layer = acc_file.split("acc_")[-1].split(".csv")[0]
        acc_data = pandas.read_csv(acc_file, header=0)
        time_step = acc_data.time.iloc[1] - acc_data.time.iloc[0]
        acc = acc_data.acc.to_list()
        spect = pyrotd.calc_spec_accels(time_step, acc, osc_freqs, osc_damping).spec_accel
        spect_df = pandas.DataFrame({'period': osc_t, 'spect': spect})
        spect_df.to_csv(f"{folder_path}\\output\\spect_{layer}.csv", index=False)


def plot_results(folder_path, layers):

    
    pyplot.style.use('seaborn-v0_8-bright')

    ## Process layer data to add depth information
    layers_df = pandas.DataFrame(layers)
    layers_df['depth'] = layers_df.hlay.cumsum()

    ## Plot max response profile
    maxnoderesp = pandas.read_csv(f"{folder_path}\\output\\maxnoderesp.csv")
    maxnoderesp['depth'] = pandas.Series([0] + layers_df.depth.to_list())
    maxelemresp = pandas.read_csv(f"{folder_path}\\output\\maxelemresp.csv")
    maxelemresp['depth'] = layers_df.depth

    fig, (ax1, ax2, ax3) = pyplot.subplots(1, 3, figsize=(10, 7), sharey=True)
    ax1.plot(maxnoderesp.acc_x.abs(), maxnoderesp.depth)
    ax2.plot(maxnoderesp.dis_x.abs(), maxnoderesp.depth)
    ax3.plot(maxelemresp.strn_x.abs() * 100, layers_df.depth, drawstyle='steps-post')
    ax1.set_xlabel('Acceleration (m/s$^2$)')
    ax2.set_xlabel('Relative displacement (m)')
    ax3.set_xlabel('Shear strain (%)')
    for ax in [ax1, ax2, ax3]:
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
        ax.grid(True)
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')
    for ax in [ax1, ax2, ax3]:
        ax.invert_yaxis()
    fig.savefig(f"{folder_path}\\output\\maxresp.svg", bbox_inches="tight")

    ## Plot response spectrum for all layers
    for spect_file in glob.glob(f"{folder_path}\\output\\spect_*.csv"):
        layer = spect_file.split("\\output\\spect_")[-1].split(".csv")[0]
        spect = pandas.read_csv(spect_file)

        fig, ax = pyplot.subplots(figsize=(7, 7))
        ax.plot(spect.period, spect.spect)
        ax.set_xscale('log')
        ax.set_xlabel('Time period (s)')
        ax.set_ylabel('Response acceleration (m/s$^2$)')
        ax.set_xlim(left=0.01, right=10)
        ax.set_ylim(bottom=0)
        ax.grid(True)
        fig.savefig(f"{folder_path}\\output\\spect_{layer}.svg", bbox_inches="tight")
        pyplot.close(fig)

    ## Plot hysteresis curves for all layers
    strain_files = glob.glob(f"{folder_path}\\output\\strain_*.csv")
    stress_files = glob.glob(f"{folder_path}\\output\\stress_*.csv")
    for strain_file, stress_file in zip(strain_files, stress_files):
        layer = strain_file.split("\\output\\strain_")[-1].split(".csv")[0]
        strain = pandas.read_csv(strain_file)
        stress = pandas.read_csv(stress_file)

        fig, ax = pyplot.subplots(figsize=(7, 7))
        ax.plot(strain.strain * 100, stress.stress / 1000)
        ax.set_xlabel('Strain (%)')
        ax.set_ylabel('Shear stress (kPa)')
        ax.grid(True)
        fig.savefig(f"{folder_path}\\output\\strsstrn_{layer}.svg", bbox_inches="tight")
        pyplot.close(fig)