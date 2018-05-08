"""
Run antibody characterization tool on the L110-CCK dataset
Output an excel sheet of results
"""
import os
import numpy as np
import pandas as pd #also requires xlsxwriter
from at_synapse_detection import dataAccess as da
from at_synapse_detection import antibodyAnalysis as aa



def validation():
    """ Run antibody characterization tool on the L110-CCK dataset

    Return
    ----------
    df : dataframe - contains results
    """

    # Location of data
    base_dir = "S:/AIBS_Stanford_for_AT/AT_Plans_and_NM_AT_Images/20180409_JAT_Cortex_#6_Validation/raw_align_tiff" #Location of align tif
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70} #Resolution of a pixel
    thresh = 0.9 #What qualifies for final probability map
    number_of_datasets = 20 #Number of wells

    #Rb Antibody
    conjugate_fn_str = 'GAD2' #String segment to search in a filename 
    #Ms Antibody project name, no parent or subclone number needed
    target_fn_str = 'L110'
    #Takes base directory string and gives you an array of all the files within
    filenames = aa.getListOfFolders(base_dir)
    #
    conjugate_filenames = []
    target_filenames = []
    query_list = []
    folder_names = []



    n = 1
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'SYNAPSIN' #String segment to search in a filename
    target_fn_str = 'K28'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [conjugate_name], 'preIF_z': [2], 'postIF': [target_name], 'postIF_z': [1], 'punctumSize': 2}
    query_list.append(query)

    n = 2
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'SYNAPSIN' #String segment to search in a filename
    target_fn_str = 'L124'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [target_name, conjugate_name], 'preIF_z': [1,2], 'postIF': [], 'postIF_z': [], 'punctumSize': 2}
    query_list.append(query)

    n = 3
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'GAD2' #String segment to search in a filename
    target_fn_str = 'L106'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [target_name, conjugate_name], 'preIF_z': [1,2], 'postIF': [], 'postIF_z': [], 'punctumSize': 2}
    query_list.append(query)

    n = 4
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'PSD' #String segment to search in a filename
    target_fn_str = 'K28'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [], 'preIF_z': [], 'postIF': [target_name, conjugate_name], 'postIF_z': [1,2], 'punctumSize': 2}
    query_list.append(query)

    n = 10
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'SYNAPSIN' #String segment to search in a filename
    target_fn_str = 'K28'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [conjugate_name], 'preIF_z': [2], 'postIF': [target_name], 'postIF_z': [1], 'punctumSize': 2}
    query_list.append(query)

    n = 11
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'SYNAPSIN' #String segment to search in a filename
    target_fn_str = 'L124'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [target_name, conjugate_name], 'preIF_z': [1,2], 'postIF': [], 'postIF_z': [], 'punctumSize': 2}
    query_list.append(query)

    n = 12
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'GAD2' #String segment to search in a filename
    target_fn_str = 'L106'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [target_name, conjugate_name], 'preIF_z': [1,2], 'postIF': [], 'postIF_z': [], 'punctumSize': 2}
    query_list.append(query)

    n = 13
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'PSD' #String segment to search in a filename
    target_fn_str = 'K28'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [], 'preIF_z': [], 'postIF': [target_name, conjugate_name], 'postIF_z': [1,2], 'punctumSize': 2}
    query_list.append(query)



    # Run all the queries
    measure_list = aa.calculate_measure_lists(query_list, None, base_dir,
                                        thresh, resolution, target_filenames)

    df = aa.create_df(measure_list, folder_names, target_filenames, conjugate_filenames)
    print(df)

    return df
    

def main():
    """ Run comparisons """

    validation_df = validation()
    
    sheet_name = 'validation-cortex-6'
    fn = 'validation-cortex-6.xlsx'
    df_list = [validation_df]
    aa.write_dfs_to_excel(df_list, sheet_name, fn)
    

if __name__ == '__main__':
    main()
