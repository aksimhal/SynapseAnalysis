"""
Run antibody characterization tool on the Mitochrondria-170906.py
Output an excel sheet of results
"""
import os
import numpy as np
import pandas as pd #also requires xlsxwriter
from at_synapse_detection import dataAccess as da
from at_synapse_detection import antibodyAnalysis as aa



def mitochrondia_170906():
    """ Run antibody characterization tool on the L113-Homer dataset

    Return
    ----------
    df : dataframe - contains results
    """

    # Location of data
    base_dir = '/Users/anish/Dropbox/KDM-SYN-170906/'
    folder_names = aa.getListOfFolders(base_dir)
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9

    conjugate_filename_str = 'VDAC'
    target_filename_str = 'N152'

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


def main():
    """ Run homer comparisons """

    mitochrondia_170906_df = mitochrondia_170906()

    sheet_name = 'mitochrondia_170906'
    fn = 'mitochrondia_170906.xlsx'
    df_list = [mitochrondia_170906_df]
    aa.write_dfs_to_excel(df_list, sheet_name, fn)

if __name__ == '__main__':
    main()
