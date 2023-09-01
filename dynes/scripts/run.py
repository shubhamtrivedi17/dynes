# -*- coding: utf-8 -*-

import os
import dynes

PACKAGE_PATH = os.path.dirname(dynes.__file__)

def dynes(folder_path):

    current_dir = os.getcwd()
    os.chdir(folder_path)
    os.system(f'"{PACKAGE_PATH}\exe\dynes3d.exe" < dynes.dat > dynes.log')
    os.chdir(current_dir)


def pstdynes(folder_path):

    current_dir = os.getcwd()
    os.chdir(folder_path)
    os.system(f'"{PACKAGE_PATH}\exe\pstdynes.exe" < post_acc.dat > post_acc.log')
    os.system(f'"{PACKAGE_PATH}\exe\pstdynes.exe" < post_stress.dat > post_stress.log')
    os.system(f'"{PACKAGE_PATH}\exe\pstdynes.exe" < post_strain.dat > post_strain.log')
    os.system(f'"{PACKAGE_PATH}\exe\pstdynes.exe" < post_spect.dat > post_spect.log')
    os.chdir(current_dir)