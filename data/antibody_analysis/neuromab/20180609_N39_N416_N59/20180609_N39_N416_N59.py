"""
Run antibody characterization tool on the L110-CCK dataset
Output an excel sheet of results
"""
import os
import numpy as np
import pandas as pd #also requires xlsxwriter
from at_synapse_detection import dataAccess as da
from at_synapse_detection import antibodyAnalysis as aa



def N39B():
    """ Run antibody characterization tool on the L110-CCK dataset

    Return
    ----------
    df : dataframe - contains results
    """

    # Location of data
    base_dir = "C:/Users/stjst/Desktop/Work/Image_Processing/20180609/align_tiffs" #Location of align tif"
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70} #Resolution of a pixel
    thresh = 0.9 #What qualifies for final probability map
    number_of_datasets = 22 #Number of wells

    #Rb Antibody
    conjugate_fn_str = 'PSD' #String segment to search in a filename 
    #Ms Antibody project name, no parent or subclone number needed
    target_fn_str = 'N39B'
    #Takes base directory string and gives you an array of all the files within
    filenames = aa.getListOfFolders(base_dir)
    #
    conjugate_filenames = []
    target_filenames = []
    query_list = []
    folder_names = []

    for n in range(3, 19):
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
        query = {'preIF': [], 'preIF_z': [],
                'postIF': [target_name,conjugate_name], 'postIF_z': [1,2],
                'punctumSize': 2}

        query_list.append(query)



    n = 1
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'PSD' #String segment to search in a filename
    target_fn_str = 'N416'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [], 'preIF_z': [], 'postIF': [target_name,conjugate_name], 'postIF_z': [1,2], 'punctumSize': 2}
    query_list.append(query)

    n = 2
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'PSD' #String segment to search in a filename
    target_fn_str = 'N59'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [], 'preIF_z': [], 'postIF': [target_name,conjugate_name], 'postIF_z': [1,2], 'punctumSize': 2}
    query_list.append(query)


    n = 19
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'PSD' #String segment to search in a filename
    target_fn_str = 'K28'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [target_name,conjugate_name], 'preIF_z': [1,2], 'postIF': [], 'postIF_z': [], 'punctumSize': 2}
    query_list.append(query)

    n = 20
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'PSD' #String segment to search in a filename
    target_fn_str = 'SP2'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [target_name,conjugate_name], 'preIF_z': [1,2], 'postIF': [], 'postIF_z': [], 'punctumSize': 2}
    query_list.append(query)

    n = 21
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'NP-RB' #String segment to search in a filename
    target_fn_str = 'NP-MS'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [], 'preIF_z': [], 'postIF': [target_name,conjugate_name], 'postIF_z': [1,2], 'punctumSize': 2}
    query_list.append(query)

    n = 22
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'NPNS-RB' #String segment to search in a filename
    target_fn_str = 'NPNS-MS'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [], 'preIF_z': [], 'postIF': [target_name,conjugate_name], 'postIF_z': [1,2], 'punctumSize': 2}
    query_list.append(query)


    # Run all the queries
    measure_list = aa.calculate_measure_lists(query_list, None, base_dir,
                                        thresh, resolution, target_filenames)

    df = aa.create_df(measure_list, folder_names, target_filenames, conjugate_filenames)
    print(df)

    return df
    

def main():
    """ Run comparisons """

    N39B_df = N39B()
    
    sheet_name = '20180609_N39_N416_N59'
    fn = '220180609_N39_N416_N59.xlsx'
    df_list = [N39B_df]
    aa.write_dfs_to_excel(df_list, sheet_name, fn)
    

if __name__ == '__main__':
    main()
