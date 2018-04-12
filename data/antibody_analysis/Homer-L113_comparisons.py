"""
Run antibody characterization tool on the L113-Homer dataset
Output an excel sheet of results
"""
import os
import numpy as np
import pandas as pd  # also requires xlsxwriter
from at_synapse_detection import dataAccess as da
from at_synapse_detection import antibodyAnalysis as aa


def homer():
    """ Run antibody characterization tool on the L113-Homer dataset

    Return
    ----------
    df : dataframe - contains results
    """

    # Location of data
    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/neuromab_L113/'
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9
    number_of_datasets = 146

    conjugate_fn_str = 'psd'  # String segment to search in a filename
    target_fn_str = 'L113'

    filenames = aa.getListOfFolders(base_dir)

    conjugate_filenames = []
    target_filenames = []
    query_list = []
    folder_names = []

    for n in range(1, number_of_datasets + 1):
        # for n in range(1, 3):
        if n == 21:  # Dataset 21 does not exist
            continue

        print('Set: ', str(n))
        # Collate 'dataset' names for excel sheet
        folder_names.append('L113-' + str(n))
        # filename to search for
        conjugate_str = str(n) + '-' + conjugate_fn_str
        target_str = str(n) + '-' + target_fn_str

        # Search for file associated with the specific dataset number
        indices = [i for i, s in enumerate(
            filenames) if conjugate_str == s[0:len(conjugate_str)]]
        conjugate_name = filenames[indices[0]]
        print(conjugate_name)
        indices = [i for i, s in enumerate(
            filenames) if target_str == s[0:len(target_str)]]
        target_name = filenames[indices[0]]
        print(target_name)

        conjugate_filenames.append(conjugate_name)
        target_filenames.append(target_name)

        # Create query
        query = {'preIF': [target_name], 'preIF_z': [2],
                 'postIF': [conjugate_name], 'postIF_z': [2],
                 'punctumSize': 2}

        query_list.append(query)

    # Run all the queries
    measure_list = aa.calculate_measure_lists(query_list, None, base_dir,
                                              thresh, resolution, target_filenames)

    df = aa.create_df(measure_list, folder_names,
                      target_filenames, conjugate_filenames)
    print(df)

    return df


def main():
    """ Run homer comparisons """

    homer_df = homer()

    sheet_name = 'Homer-L113'
    fn = 'Homer-L113.xlsx'
    df_list = [homer_df]
    aa.write_dfs_to_excel(df_list, sheet_name, fn)


if __name__ == '__main__':
    main()
