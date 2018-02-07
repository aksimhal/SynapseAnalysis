"""
Run multiple comparisons
"""
import os
import numpy as np
import pandas as pd #also requires xlsxwriter
from at_synapse_detection import dataAccess as da
from at_synapse_detection import antibodyAnalysis as aa


def gephyrin_multipleclones():
    """Gephyrin multiple clone comparisons

    """
    folder_names = ['3-2-1', '4-2', '22-3', '23-1', '73-2', '83-1', '93-1']
    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/L106-Gephyrin/'
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9

    target_filenames = ['3-2-1-cloneA.tif', '4-2-cloneA.tif', '22-3-cloneA.tif',
                        '23-1-cloneA.tif', '73-2-cloneA.tif', '83-1-cloneA.tif',
                        '93-1-cloneA.tif']

    conjugate_filenames = ['3-2-1-GADA.tif', '4-2-GADA.tif', '22-3-GADA.tif',
                           '23-1-GADA.tif',  '73-2-GADA.tif', '83-1GADA.tif',
                           '93-1-GADA.tif']

    query_list = []
    for n in range(0, len(target_filenames)):
        target_name = target_filenames[n]
        conjugate_name = conjugate_filenames[n]
        query = {'preIF': [conjugate_name], 'preIF_z': [2],
                 'postIF': [target_name], 'postIF_z': [2],
                 'punctumSize': 2}
        query_list.append(query)

    measure_list = aa.calculate_measure_lists(query_list, folder_names, base_dir,
                                        thresh, resolution, target_filenames)

    df = aa.create_df(measure_list, folder_names, target_filenames, conjugate_filenames)
    print(df)

    return df





def collybistin_multipleclones():
    """ Collybistin multiple clones
    """

    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/L120-Collybistin/'
    folder_names = aa.getListOfFolders(base_dir)
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9
    conjugate_filename_str = 'GAD'
    target_filename_str = 'L120'
    conjugate_filenames = []
    target_filenames = []
    query_list = []
    for foldername in folder_names:
        target_name = aa.find_filename(target_filename_str, foldername, base_dir)
        conjugate_name = aa.find_filename(conjugate_filename_str, foldername, base_dir)

        conjugate_filenames.append(conjugate_name)
        target_filenames.append(target_name)

        query = {'preIF': [conjugate_name], 'preIF_z': [2],
                'postIF': [target_name], 'postIF_z': [2],
                'punctumSize': 2}

        query_list.append(query)

    measure_list = aa.calculate_measure_lists(query_list, folder_names, base_dir,
                                        thresh, resolution, target_filenames)

    df = aa.create_df(measure_list, folder_names, target_filenames, conjugate_filenames)
    print(df)

    return df

def VGAT_lowicryl_multipleclones():
    """ VGAT_lowicryl_multipleclones
    """

    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/L118-VGAT/Lowicryl/'
    folder_names = aa.getListOfFolders(base_dir)
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9
    conjugate_filename_str = 'GAD'
    target_filename_str = 'VGAT'
    conjugate_filenames = []
    target_filenames = []
    query_list = []
    for foldername in folder_names:
        target_name = aa.find_filename(target_filename_str, foldername, base_dir)
        conjugate_name = aa.find_filename(conjugate_filename_str, foldername, base_dir)

        conjugate_filenames.append(conjugate_name)
        target_filenames.append(target_name)

        query = {'preIF': [target_name, conjugate_name], 'preIF_z': [2, 2],
                'postIF': [], 'postIF_z': [],
                'punctumSize': 2}

        query_list.append(query)

    measure_list = aa.calculate_measure_lists(query_list, folder_names, base_dir,
                                        thresh, resolution, target_filenames)

    df = aa.create_df(measure_list, folder_names, target_filenames, conjugate_filenames)
    print(df)

    return df

def homer_multipleclones():
    """ homer_multipleclones
    """

    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/L113-Homer/'
    folder_names = aa.getListOfFolders(base_dir)
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9
    conjugate_filename_str = 'PSD'
    target_filename_str = 'L113'
    conjugate_filenames = []
    target_filenames = []
    query_list = []
    for foldername in folder_names:
        target_name = aa.find_filename(target_filename_str, foldername, base_dir)
        conjugate_name = aa.find_filename(conjugate_filename_str, foldername, base_dir)

        conjugate_filenames.append(conjugate_name)
        target_filenames.append(target_name)

        query = {'preIF': [], 'preIF_z': [],
                'postIF': [target_name, conjugate_name], 'postIF_z': [2, 2],
                'punctumSize': 2}

        query_list.append(query)

    measure_list = aa.calculate_measure_lists(query_list, folder_names, base_dir,
                                        thresh, resolution, target_filenames)

    df = aa.create_df(measure_list, folder_names, target_filenames, conjugate_filenames)
    print(df)

    return df


def irsp53_lowicryl_multipleclones():
    """ irsp53_lowicryl_multipleclones
    """

    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/L117-IRSP53/Lowicryl/'
    folder_names = aa.getListOfFolders(base_dir)
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9
    conjugate_filename_str = 'PSD'
    target_filename_str = 'L117'
    conjugate_filenames = []
    target_filenames = []
    query_list = []
    for foldername in folder_names:
        target_name = aa.find_filename(target_filename_str, foldername, base_dir)
        conjugate_name = aa.find_filename(conjugate_filename_str, foldername, base_dir)

        conjugate_filenames.append(conjugate_name)
        target_filenames.append(target_name)

        query = {'preIF': [], 'preIF_z': [],
                'postIF': [target_name, conjugate_name], 'postIF_z': [2, 2],
                'punctumSize': 2}

        query_list.append(query)

    measure_list = aa.calculate_measure_lists(query_list, folder_names, base_dir,
                                        thresh, resolution, target_filenames)

    df = aa.create_df(measure_list, folder_names, target_filenames, conjugate_filenames)
    print(df)

    return df

def bassoon_L170920_multipleclones():
    """ bassoon_L170920_multipleclones
    """

    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/L170920-Bassoon/'
    folder_names = aa.getListOfFolders(base_dir)
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9
    conjugate_filename_str = 'Synapsin'
    target_filename_str = 'L124'
    conjugate_filenames = []
    target_filenames = []
    query_list = []
    for foldername in folder_names:
        target_name = aa.find_filename(target_filename_str, foldername, base_dir)
        conjugate_name = aa.find_filename(conjugate_filename_str, foldername, base_dir)

        conjugate_filenames.append(conjugate_name)
        target_filenames.append(target_name)

        query = {'preIF': [target_name, conjugate_name], 'preIF_z': [2, 2],
                'postIF': [], 'postIF_z': [],
                'punctumSize': 2}

        query_list.append(query)

    measure_list = aa.calculate_measure_lists(query_list, folder_names, base_dir,
                                        thresh, resolution, target_filenames)

    df = aa.create_df(measure_list, folder_names, target_filenames, conjugate_filenames)
    print(df)

    return df

def bassoon_L170921_multipleclones():
    """ bassoon_L170921_multipleclones
    """

    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/L170921-Bassoon/'
    folder_names = aa.getListOfFolders(base_dir)
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9
    conjugate_filename_str = 'PSD'
    target_filename_str = 'L124'
    conjugate_filenames = []
    target_filenames = []
    query_list = []
    for foldername in folder_names:
        target_name = aa.find_filename(target_filename_str, foldername, base_dir)
        conjugate_name = aa.find_filename(conjugate_filename_str, foldername, base_dir)

        conjugate_filenames.append(conjugate_name)
        target_filenames.append(target_name)

        query = {'preIF': [target_name], 'preIF_z': [2],
                'postIF': [conjugate_name], 'postIF_z': [2],
                'punctumSize': 2}

        query_list.append(query)

    measure_list = aa.calculate_measure_lists(query_list, folder_names, base_dir,
                                        thresh, resolution, target_filenames)

    df = aa.create_df(measure_list, folder_names, target_filenames, conjugate_filenames)
    print(df)

    return df


def main():
    """ Run concentration comparisons """

    bassoon_21 = bassoon_L170921_multipleclones()
    bassoon_20 = bassoon_L170920_multipleclones()
    irsp53_df = irsp53_lowicryl_multipleclones()
    homer_df = homer_multipleclones()
    vgat_df = VGAT_lowicryl_multipleclones()
    collybistin_df = collybistin_multipleclones()
    gephyrin_df = gephyrin_multipleclones()

    sheet_name = 'Multipleclones'
    fn = 'multipleclones.xlsx'
    df_list = [gephyrin_df, collybistin_df, vgat_df, homer_df, irsp53_df, bassoon_20, bassoon_21]
    aa.write_dfs_to_excel(df_list, sheet_name, fn)


if __name__ == '__main__':
    main()
