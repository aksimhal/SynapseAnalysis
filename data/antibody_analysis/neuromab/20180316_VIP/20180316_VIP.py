"""
Run antibody characterization tool on the L110-CCK dataset
Output an excel sheet of results
"""
import os
import numpy as np
import pandas as pd #also requires xlsxwriter
from at_synapse_detection import dataAccess as da
from at_synapse_detection import antibodyAnalysis as aa



def VIP():
    """ Run antibody characterization tool on the L110-CCK dataset

    Return
    ----------
    df : dataframe - contains results
    """

    # Location of data
    base_dir = "C:/Users/i3x-MM/DesktopSACT/20180316/Align_Raw_Tiffs" #Location of align tif"
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70} #Resolution of a pixel
    thresh = 0.9 #What qualifies for final probability map
    number_of_datasets = 12 #Number of wells

    #Rb Antibody
    conjugate_fn_str = 'GAD2' #String segment to search in a filename 
    #Ms Antibody project name, no parent or subclone number needed
    target_fn_str = 'L108'
    #Takes base directory string and gives you an array of all the files within
    filenames = aa.getListOfFolders(base_dir)
    #
    conjugate_filenames = []
    target_filenames = []
    query_list = []
    folder_names = []

    for n in range(1, 12):
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
        query = {'preIF': [target_name], 'preIF_z': [1],
                'postIF': [conjugate_name], 'postIF_z': [2],
                'punctumSize': 2}

        query_list.append(query)

    n = 12
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'GAD2' #String segment to search in a filename
    target_fn_str = 'L106'
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

    VIP_df = VIP()
    
    sheet_name = '20180316_AT_VIP'
    fn = '20180316_AT_VIP.xlsx'
    df_list = [VIP_df]
    aa.write_dfs_to_excel(df_list, sheet_name, fn)
    

if __name__ == '__main__':
    main()
