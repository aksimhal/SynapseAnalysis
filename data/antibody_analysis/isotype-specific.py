"""
Run antibody characterization tool on the Isotype-Specific-Ab-Data dataset 
Output an excel sheet of results
"""
import os
import numpy as np
import pandas as pd #also requires xlsxwriter
from at_synapse_detection import dataAccess as da
from at_synapse_detection import antibodyAnalysis as aa


def isotype_specific():
    """ Run antibody characterization tool
    L106 is Gephyrin, L120 is Collybistin, L124 is Bassoon and K28 is PSD-95.

    1:3 - L106 (Gephyrin) / GAD2
    4   - L120 (Collybistin) / GAD2
    5   - K28 (PSD95) / PSD95
    6   - L124 (Bassoon) / PSD95
    7:9 - L106 (Gephyrin) / GAD2
    10  - L120 (Collybistin) / GAD2
    11  - K28 (PSD95) / PSD95
    12  - L124 (Bassoon) / PSD95 

    Return
    ----------
    df : dataframe - contains results
    """

    # Location of data
    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/Isotype-Specific-Ab-Data/'
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9
    number_of_datasets = 12

    filenames = aa.getListOfFolders(base_dir)


    conjugate_filenames = []
    target_filenames = []
    query_list = []
    folder_names = []

    for n in range(1, 4):
        folder_names.append(str(n)) # Collate 'dataset' names for excel sheet
        reference_fn_str = 'GAD2' #String segment to search in a filename
        target_fn_str = 'L106'
        conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
        
        conjugate_filenames.append(conjugate_name)
        target_filenames.append(target_name)

        # Create query
        query = {'preIF': [target_name], 'preIF_z': [1],
                'postIF': [conjugate_name], 'postIF_z': [1],
                'punctumSize': 2}
        query_list.append(query)

    # Dataset 4
    n = 4
    folder_names.append(str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'GAD2' #String segment to search in a filename
    target_fn_str = 'L120'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [target_name], 'preIF_z': [1], 'postIF': [conjugate_name], 'postIF_z': [1], 'punctumSize': 2}
    query_list.append(query)

    # Dataset 5
    n = 5
    folder_names.append(str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'PSD' #String segment to search in a filename
    target_fn_str = 'K28'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [], 'preIF_z': [], 'postIF': [conjugate_name, target_name], 'postIF_z': [1, 1], 'punctumSize': 2}
    query_list.append(query)

    # Dataset 6
    n = 6
    folder_names.append(str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'PSD' #String segment to search in a filename
    target_fn_str = 'L124'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [], 'preIF_z': [], 'postIF': [conjugate_name, target_name], 'postIF_z': [1, 1], 'punctumSize': 2}
    query_list.append(query)

    # Datasets 7:9
    for n in range(7, 10):
        folder_names.append(str(n)) # Collate 'dataset' names for excel sheet
        reference_fn_str = 'GAD2' #String segment to search in a filename
        target_fn_str = 'L106'
        conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
        
        conjugate_filenames.append(conjugate_name)
        target_filenames.append(target_name)

        # Create query
        query = {'preIF': [target_name], 'preIF_z': [1],
                'postIF': [conjugate_name], 'postIF_z': [1],
                'punctumSize': 2}
        query_list.append(query)

    # Dataset 10
    n = 10
    folder_names.append(str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'GAD2' #String segment to search in a filename
    target_fn_str = 'L120'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [target_name], 'preIF_z': [1], 'postIF': [conjugate_name], 'postIF_z': [1], 'punctumSize': 2}
    query_list.append(query)

    # Dataset 11
    n = 11
    folder_names.append(str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'PSD' #String segment to search in a filename
    target_fn_str = 'K28'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [], 'preIF_z': [], 'postIF': [conjugate_name, target_name], 'postIF_z': [1, 1], 'punctumSize': 2}
    query_list.append(query)

    # Dataset 12
    n = 12
    folder_names.append(str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'PSD' #String segment to search in a filename
    target_fn_str = 'L124'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [], 'preIF_z': [], 'postIF': [conjugate_name, target_name], 'postIF_z': [1, 1], 'punctumSize': 2}
    query_list.append(query)

    # Run all the queries
    measure_list = aa.calculate_measure_lists(query_list, None, base_dir,
                                        thresh, resolution, target_filenames)

    df = aa.create_df(measure_list, folder_names, target_filenames, conjugate_filenames)
    print(df)

    return df


def main():
    """ Run homer comparisons """

    isotype_specific_df = isotype_specific()

    # sheet_name = 'isotype_specific'
    # fn = 'isotype_specific.xlsx'
    # df_list = [isotype_specific_df]
    # aa.write_dfs_to_excel(df_list, sheet_name, fn)


if __name__ == '__main__':
    main()
