"""
Run Concentration Comparisons
"""
import os
import numpy as np
import pandas as pd #also requires xlsxwriter
from at_synapse_detection import dataAccess as da
from at_synapse_detection import antibodyAnalysis as aa


def glur1_concentrations(): 
    """GLUR1 concentration comparisons """
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9
    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/Dilutions/KDM-SYN-120314/'
    folder_names = ['GluR1_25', 'GluR1_125', 'GluR1_625', 'GluR1_3125']
    
    target_filenames = ['GluR1_25_1st_A.tif', 'GluR1_125_1st_A.tif', 'GluR1_625_1st_A.tif', 'GluR1_3125_1st_A.tif']
    conjugate_antibody_name = 'synph_1st_A.tif'
    
    conjugate_filenames = []
    query_list = [] 
    for target_antibody_name in target_filenames: 
        query = {'preIF': [conjugate_antibody_name], 'preIF_z': [2],
                'postIF': [target_antibody_name], 'postIF_z': [2],
                'punctumSize': 2}
        query_list.append(query)
        conjugate_filenames.append(conjugate_antibody_name)

    measure_list = aa.calculate_measure_lists(query_list, folder_names, base_dir, 
                                        thresh, resolution, target_filenames)

    df = aa.create_df(measure_list, folder_names, target_filenames, conjugate_filenames) 
    print(df)

    return df



def glur2_concentrations(): 
    """GLUR2 concentration comparisons """
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9
    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/Dilutions/KDM-SYN-120320/'
    folder_names = ['GluR2_25', 'GluR2_125', 'GluR2_625', 'GluR2_3125']
    
    target_antibody_name = 'GluR2A.tif'
    conjugate_antibody_name = 'SynapsinA.tif'

    conjugate_filenames = [] 
    target_filenames = [] 
    query_list = [] 
    for fn in folder_names: 
        query = {'preIF': [conjugate_antibody_name], 'preIF_z': [2],
                'postIF': [target_antibody_name], 'postIF_z': [2],
                'punctumSize': 2}
        query_list.append(query)
        target_filenames.append(target_antibody_name)
        conjugate_filenames.append(conjugate_antibody_name)

    measure_list = aa.calculate_measure_lists(query_list, folder_names, base_dir, 
                                        thresh, resolution, target_filenames)

    df = aa.create_df(measure_list, folder_names, target_filenames, conjugate_filenames) 
    print(df)
    
    return df


def glur3_concentrations(): 
    """GLUR3 concentration comparisons """
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9
    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/Dilutions/KDM-SYN-120322/'
    folder_names = ['GluR3_25', 'GluR3_125', 'GluR3_625', 'GluR3_3125']
    
    target_antibody_name = 'GluR3_1stA.tif'
    conjugate_antibody_name = 'VGluT1A.tif'
    
    conjugate_filenames = [] 
    target_filenames = []
    query_list = [] 
    for fn in folder_names: 
        query = {'preIF': [conjugate_antibody_name], 'preIF_z': [2],
                'postIF': [target_antibody_name], 'postIF_z': [2],
                'punctumSize': 2}
        query_list.append(query)
        target_filenames.append(target_antibody_name)
        conjugate_filenames.append(conjugate_antibody_name)

    measure_list = aa.calculate_measure_lists(query_list, folder_names, base_dir, 
                                        thresh, resolution, target_filenames)

    df = aa.create_df(measure_list, folder_names, target_filenames, conjugate_filenames)
    print(df)

    return df

def synapsin_concentrations(): 
    """ Synapsin concentration comparisons """ 
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9
    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/Dilutions/KDM-SYN-110228/'
    folder_names = ['Stacks SynCS 100', 'Stacks SynCS 1000']
    
    target_antibody_name = 'ASynCS_1st.tif'
    conjugate_antibody_name = 'AVGluT1_3rd.tif'
    
    conjugate_filenames = []
    target_filenames = [] 
    query_list = [] 
    for fn in folder_names: 
        query = {'preIF': [target_antibody_name, conjugate_antibody_name], 'preIF_z': [2, 2],
                'postIF': [], 'postIF_z': [],
                'punctumSize': 2}
        query_list.append(query)
        target_filenames.append(target_antibody_name)
        conjugate_filenames.append(conjugate_antibody_name)

    measure_list = aa.calculate_measure_lists(query_list, folder_names, base_dir, 
                                        thresh, resolution, target_filenames)

    df = aa.create_df(measure_list, folder_names, target_filenames, conjugate_filenames)

    print(df)
    return df

def nr1_concentrations(): 
    """NR1 Concentration comparison"""
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9

    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/Dilutions/KDM-SYN-120404/'
    folder_names = ['NR1_25', 'NR1_125', 'NR1_625', 'NR1_3125']

    target_antibody_name = 'NR1_1stA.tif'
    conjugate_antibody_name = 'VGluT1A.tif'
    
    query = {'preIF': [conjugate_antibody_name], 'preIF_z': [1],
             'postIF': [target_antibody_name], 'postIF_z': [1],
             'punctumSize': 2}

    conjugate_filenames = []
    target_filenames = [] 
    query_list = [] 
    for fn in folder_names: 
        query_list.append(query)
        target_filenames.append(target_antibody_name)
        conjugate_filenames.append(conjugate_antibody_name)

    measure_list = aa.calculate_measure_lists_rayleigh(query_list, folder_names, base_dir, 
                                        thresh, resolution, target_filenames)

    df = aa.create_df(measure_list, folder_names, target_filenames, conjugate_filenames)

    print(df)
    return df


def main(): 
    """ Run concentration comparisons """ 
    
    synapsin_df = synapsin_concentrations() 
    glur1_df = glur1_concentrations()
    glur2_df = glur2_concentrations()
    glur3_df = glur3_concentrations()
    nr1_df = nr1_concentrations()

    sheet_name = 'Concentration'
    fn = 'concentration_comparisons.xlsx'
    df_list = [synapsin_df, glur1_df, glur2_df, glur3_df, nr1_df]
    #df_list = [nr1_df]
    aa.write_dfs_to_excel(df_list, sheet_name, fn)


if __name__ == '__main__':
    main()
