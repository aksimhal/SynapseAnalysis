"""
Run antibody characterization tool on the L110-CCK dataset
Output an excel sheet of results
"""
import os
import numpy as np
import pandas as pd #also requires xlsxwriter
from at_synapse_detection import dataAccess as da
from at_synapse_detection import antibodyAnalysis as aa



def VGLUT3():
    """ Run antibody characterization tool on the L110-CCK dataset

    Return
    ----------
    df : dataframe - contains results
    """

    # Location of data
    base_dir = "C:/Users/stjst/Desktop/Work/Image_Processing/20180228N_34_and_L114_Pure/Align_Tiffs" #Location of align tif"
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70} #Resolution of a pixel
    thresh = 0.9 #What qualifies for final probability map
    number_of_datasets = 18 #Number of wells

    #Rb Antibody
    conjugate_fn_str = 'SYNAPSIN' #String segment to search in a filename 
    #Ms Antibody project name, no parent or subclone number needed
    target_fn_str = 'N34'
    #Takes base directory string and gives you an array of all the files within
    filenames = aa.getListOfFolders(base_dir)
    #
    conjugate_filenames = []
    target_filenames = []
    query_list = []
    folder_names = []

    for n in range(1, 11):
        #Use if dataset missing
        #if n == 21: # Dataset 21 does not exist
            #continue

        print('Well: ', str(n))
        folder_names.append('Test-' + str(n)) # Collate 'dataset' names for excel sheet
        conjugate_str = str(n) + '-' + conjugate_fn_str #creates filename to search for #Creates n-conjugatename
        target_str = str(n) + '-' + target_fn_str

        # Search for file associated with the specific dataset number
        indices = [i for i, s in enumerate(filenames) if conjugate_str == s[0:len(conjugate_str)]]
        conjugate_name = filenames[indices[0]]
        print(conjugate_name)
        indices = [i for i, s in enumerate(filenames) if target_str == s[0:len(target_str)]]
        target_name = filenames[indices[0]]
        print(target_name)
        
        conjugate_filenames.append(conjugate_name)
        target_filenames.append(target_name)

        # Create query
        #
        query = {'preIF': [target_name,conjugate_name], 'preIF_z': [1,2],
                'postIF': [], 'postIF_z': [],
                'punctumSize': 2}

        query_list.append(query)

    n = 11
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'SYNAPSIN' #String segment to search in a filename
    target_fn_str = 'N28'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [target_name,conjugate_name], 'preIF_z': [1,2], 'postIF': [], 'postIF_z': [], 'punctumSize': 2}
    query_list.append(query)

    n = 12
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'SYNAPSIN' #String segment to search in a filename
    target_fn_str = 'L114'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [conjugate_name], 'preIF_z': [2], 'postIF': [target_name], 'postIF_z': [1], 'punctumSize': 2}
    query_list.append(query)

    n = 13
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'SYNAPSIN' #String segment to search in a filename
    target_fn_str = 'L114'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [conjugate_name], 'preIF_z': [2], 'postIF': [target_name], 'postIF_z': [1], 'punctumSize': 2}
    query_list.append(query)

    n = 14
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'SYNAPSIN' #String segment to search in a filename
    target_fn_str = 'L114'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [conjugate_name], 'preIF_z': [2], 'postIF': [target_name], 'postIF_z': [1], 'punctumSize': 2}
    query_list.append(query)

    n = 15
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'SYNAPSIN' #String segment to search in a filename
    target_fn_str = 'K28'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [conjugate_name], 'preIF_z': [2], 'postIF': [target_name], 'postIF_z': [1], 'punctumSize': 2}
    query_list.append(query)

    


    # Run all the queries
    measure_list = aa.calculate_measure_lists(query_list, None, base_dir,
                                        thresh, resolution, target_filenames)

    df = aa.create_df(measure_list, folder_names, target_filenames, conjugate_filenames)
    print(df)

    return df
    

def main():
    """ Run comparisons """

    VGLUT3_df = VGLUT3()
    
    sheet_name = '20180424_AT_VGLUT3'
    fn = '20180424_AT_VGLUT3.xlsx'
    df_list = [VGLUT3_df]
    aa.write_dfs_to_excel(df_list, sheet_name, fn)
    

if __name__ == '__main__':
    main()
