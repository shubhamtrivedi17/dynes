# -*- coding: utf-8 -*-

import os

PACKAGE_PATH = ''

def dynes(folder_path):

    current_dir = os.getcwd()
    os.chdir(folder_path)
    os.system(f"{PACKAGE_PATH}//exe//dynes.exe < dynes.bat > dynes.log")
    os.chdir(current_dir)


def pstdynes(folder_path):

    current_dir = os.getcwd()
    os.chdir(folder_path)
    os.system(f"{PACKAGE_PATH}//exe//pstdynes.exe < post_acc.dat > post_acc.log")
    os.system(f"{PACKAGE_PATH}//exe//pstdynes.exe < post_stress.dat > post_stress.log")
    os.system(f"{PACKAGE_PATH}//exe//pstdynes.exe < post_strain.dat > post_strain.log")
    os.system(f"{PACKAGE_PATH}//exe//pstdynes.exe < post_spect.dat > post_spect.log")
    os.chdir(current_dir)