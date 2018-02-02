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

    measure_list = run_multipleclones_comparison(query_list, 
                                                folder_names, base_dir, 
                                                thresh, resolution, 
                                                target_filenames)

    # df = create_concentration_df(measure_list, folder_names, 
    #                              target_filenames, conjugate_filenames) 

    return df

def run_multipleclones_comparison(query_list, folder_names, base_dir, thresh, 
                                 resolution, target_filenames): 
    """multiple clones comparison

    """

    measure_list = []
    for n, foldername in enumerate(folder_names): 
        query = query_list[n]
        data_location = os.path.join(base_dir, foldername)
        target_antibody_name = target_filenames[n]
        synaptic_volumes = da.load_tiff_from_query(query, data_location)
        measure = aa.run_ab_analysis(synaptic_volumes, query, thresh, resolution, target_antibody_name)

        measure_list.append(measure)

    return measure_list    



def main(): 
    """ Run concentration comparisons """ 
    
    # synapsin_df = synapsin_concentrations() 
    # glur1_df = glur3_concentrations()
    # glur2_df = glur2_concentrations()
    # glur3_df = glur3_concentrations()
    # nr1_df = nr1_concentrations()

    # sheet_name = 'Concentration'
    # fn = 'concentration_comparisons.xlsx'
    # df_list = [synapsin_df, glur1_df, glur2_df, glur3_df, nr1_df]
    # aa.write_dfs_to_excel(df_list, sheet_name, fn)


if __name__ == '__main__':
    main()
