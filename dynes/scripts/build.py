# -*- coding: utf-8 -*-

import pandas
import fortranformat as ff


def write_dynes(settings, materials, layers, bedrock, eqdata, folder_path):
    """Write dynes.dat input file with all analysis settings and material data

    Args:
        settings (dict): _description_
        materials (dict): _description_
        layers (dict): _description_
        bedrock (dict): _description_
        eqdata (dict): _description_
        folder_path (str): Path to analysis folder
    """

    ## Add some default material data parameters
    for mat in materials:
        mat['ncon'] = '104'
        mat['uwei'] *= 1E3
        mat['ak'] = mat['vs'] ** 2 * mat['uwei'] / 9.80665
        mat['ifdsp'] = '1'
        mat['itp'] = '5'
        mat['nrev'] = 100
        mat['alpha'] = ''
        mat['beta'] = ''

        ## Add nonlin data
        nonlin_df = pandas.read_csv(mat['nonlin'], header=0, skiprows=[1])
        mat['par1'] = len(nonlin_df)
        mat['strn'] = nonlin_df.strn.to_list()
        mat['gg0'] = nonlin_df.gg0.to_list()
        mat['damp'] = nonlin_df.damp.to_list()

    ## Define settings from layers and materials data
    settings['nlay'] = len(layers)
    settings['nmat'] = len(materials)

    ## Write dynes inpur file
    with open(f"{folder_path}\\dynes.dat", 'w', encoding='utf-8') as file:

        ## Write analysis settings
        file.write(f"{settings['title']:<80}")
        file.write("\n")
        
        file.write(" ")
        file.write(f"{settings['mtflg']:>1}")
        file.write(f"{settings['nlay']:>3}")
        file.write(f"{settings['nmat']:>5}")
        file.write(f"{settings['nwtb']:>5}")
        file.write(f"{settings['nfix']:>5}")
        file.write(f"{settings['nbase']:>5}")
        file.write(f"{settings['neffe']:>5}")
        file.write(f"{settings['ninteg']:>5}")
        file.write(f"{settings['itermax']:>5}")
        file.write(f"{settings['filmax']:<20}")
        file.write("\n")
        
        file.write(f"{float(settings['gacc']):<10.7G}")
        file.write(f"{float(settings['gamaw']):<10.7G}")
        file.write(f"{float(settings['atm']):<10.7G}")
        file.write(f"{float(settings['buwat']):<10.7G}")
        file.write(f"{settings['btanmk']:<10}")
        file.write(f"{settings['gamnmk']:<10}")
        file.write(f"{float(settings['dmpalp']):<10.7G}")
        file.write(f"{float(settings['dmpbta']):<10.7G}")
        file.write("\n")

        ## Write material data
        for idx, mat in enumerate(materials):
            file.write(f"{idx + 1:>5}")
            file.write(f"{mat['ncon']:>5}")
            file.write("\n")
            
            file.write(f"{mat['uwei']:<10.5G}")
            file.write(f"{mat['ak']:<10.5G}")
            file.write(f"{mat['alpha']:<10}")
            file.write(f"{mat['beta']:<10}")
            file.write(f"{mat['ifdsp']:>5}")
            file.write("\n")
            
            file.write(f"{mat['itp']:>5}")
            file.write(f"{mat['nrev']:>5}")
            file.write(f"{mat['par1']:>5}")
            file.write("\n")

            writer = ff.FortranRecordWriter('(8F10.6)')
            file.write(writer.write(mat['strn']))
            file.write("\n")
            file.write(writer.write(mat['gg0']))
            file.write("\n")
            file.write(writer.write(mat['damp']))
            file.write("\n")
        
        ## Write soil layers data
        for idx, layer in enumerate(layers):
            file.write(f"{idx + 1:>5}")
            file.write(f"{layer['imat']:>5}")
            file.write(f"{float(layer['hlay']):<10.5G}")
            file.write("\n")
        
        ## Write bedrock data
        file.write(f"{bedrock['ro']:<10.5G}")
        file.write(f"{bedrock['vs']:<10.5G}")
        file.write(f"{bedrock['vp']:<10.5G}")
        file.write("\n")
        
        ## Write earthquake data
        file.write(f"{eqdata['ndata']:>5}")
        file.write(f"{eqdata['nintvl']:>5}")
        file.write(f"{eqdata['ivelot']:>5}")
        file.write(f"{eqdata['motion']:>5}")
        file.write(f"{eqdata['nprt']:>5}")
        file.write(f"{eqdata['mxprt']:>5}")
        file.write(f"{eqdata['dt']:<10}")
        file.write(f"{eqdata['filout']:<20}")
        file.write("\n")

        file.write(f"{eqdata['eqfmt']:<40}")
        file.write(f"{eqdata['eqnam']:<20}")
        file.write("\n")

        file.write(f"{eqdata['eqmult']:<10}")
        file.write(f"{eqdata['nskip']:>5}")
        file.write(f"{'':>5}")
        file.write(f"{eqdata['eqfil']:<20}")
        file.write("\n")


def write_post(settings, folder_path):
    """_summary_

    Args:
        settings (dict): _description_
        folder_path (str): Path to analysis folder
    """

    settings_post_acc = {
        'nform': 0,
        'ndata': settings['nlay'],
        'nt0': 1000,
        'filin': 'dynes.tim',
        'filout': 'dynes_acc.rsp',
        'ltyp1': 1,
        'ltyp2': 1,
        'lflg1': '',
        'lflg2': '',
        'cutfq': 0,
        'dd': [''],
        'file_save': 'post_acc.dat'
    }

    settings_post_spect = {
        'nform': 0,
        'ndata': settings['nlay'],
        'nt0': 1000,
        'filin': 'dynes.tim',
        'filout': 'dynes_spect.rsp',
        'ltyp1': 1,
        'ltyp2': 4,
        'lflg1': 1,
        'lflg2': 1,
        'cutfq': 0,
        'dd': [5.],
        'file_save': 'post_spect.dat'
    }

    settings_post_strs = {
        'nform': 0,
        'ndata': settings['nlay'],
        'nt0': 1000,
        'filin': 'dynes.tim',
        'filout': 'dynes_stress.rsp',
        'ltyp1': 13,
        'ltyp2': 1,
        'lflg1': '',
        'lflg2': '',
        'cutfq': 0,
        'dd': [''],
        'file_save': 'post_stress.dat'
    }

    settings_post_strn = {
        'nform': 0,
        'ndata': settings['nlay'],
        'nt0': 1000,
        'filin': 'dynes.tim',
        'filout': 'dynes_strain.rsp',
        'ltyp1': 15,
        'ltyp2': 1,
        'lflg1': '',
        'lflg2': '',
        'cutfq': 0,
        'dd': [''],
        'file_save': 'post_strain.dat'
    }

    settings_post_all = [settings_post_acc, settings_post_spect, settings_post_strs, settings_post_strn]

    for settings_post_i in settings_post_all:
        with open(f"{folder_path}\\{settings_post_i['file_save']}", 'w', encoding='utf-8') as file:
            file.write(f"{settings_post_i['nform']:>}")
            file.write(f"{settings_post_i['ndata']:>4}")
            file.write(f"{settings_post_i['nt0']:>5}")
            file.write(f"{settings_post_i['filin']:<20}")
            file.write(f"{settings_post_i['filout']:<20}")
            file.write("\n")
            
            for idx in range(settings['nlay']):
                file.write(f"{settings_post_i['ltyp1']:>5}")
                file.write(f"{settings_post_i['ltyp2']:>5}")
                file.write(f"{idx + 1:>5}")
                file.write(f"{settings_post_i['lflg1']:>5}")
                file.write(f"{settings_post_i['lflg2']:>5}")
                file.write(f"{settings_post_i['cutfq']:<5}")
                for dd_i in settings_post_i['dd']:
                    file.write(f"{dd_i:<5}")
                    file.write("\n")