"""
Run L113-Homer
"""
import os
import numpy as np
import pandas as pd #also requires xlsxwriter
from at_synapse_detection import dataAccess as da
from at_synapse_detection import antibodyAnalysis as aa



def homer():
    """ bassoon_L170921_multipleclones
    """

    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/neuromab_L113/'
    filenames = aa.getListOfFolders(base_dir)

    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9
    
    number_of_datasets = 146

    conjugate_fn_str = 'psd'
    target_fn_str = 'L113'

    conjugate_filenames = [] 
    target_filenames = []
    query_list = [] 
    folder_names = [] 

    for n in range(1, number_of_datasets + 1):
        if n == 21: 
            continue 
            
        folder_names.append('L113-'+str(n))
        conjugate_str = str(n) + '-' + conjugate_fn_str
        
        target_str = str(n) + '-' + target_fn_str
        
        indices = [i for i, s in enumerate(filenames) if conjugate_str == s[0:len(conjugate_str)]]
        conjugate_name = filenames[indices[0]]
        print(conjugate_name)
        indices = [i for i, s in enumerate(filenames) if target_str == s[0:len(target_str)]]
        target_name = filenames[indices[0]]
        print(target_name)

        conjugate_filenames.append(conjugate_name)
        target_filenames.append(target_name)
        
        query = {'preIF': [target_name], 'preIF_z': [2],
                'postIF': [conjugate_name], 'postIF_z': [2],
                'punctumSize': 2}

        query_list.append(query)

    measure_list = aa.calculate_measure_lists(query_list, None, base_dir, 
                                        thresh, resolution, target_filenames)

    folder_names = list(range(1, 1+number_of_datasets))
    df = aa.create_df(measure_list, folder_names, target_filenames, conjugate_filenames)
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
