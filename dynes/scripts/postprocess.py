# -*- coding: utf-8 -*-

import numpy
import pandas
import fortranformat as ff


def extract_results(folder_path):

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