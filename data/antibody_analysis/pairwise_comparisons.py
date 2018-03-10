"""
Run Pairwise Comparisons
"""
import numpy as np
import pandas as pd #also requires xlsxwriter
from at_synapse_detection import dataAccess as da
from at_synapse_detection import antibodyAnalysis as aa


def psd95_pairwise():
    """
    PSD95 pairwise comparisons

    Parameters
    -------------
    None 

    Return
    -------------
    df : dataframe
    """

    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/pairwise/KDM-RW-120419/'
    query1 = {'preIF': ['synapsin_1st.tif'], 'preIF_z': [2],
            'postIF': ['PSD95m_1st.tif'], 'postIF_z': [2],
            'punctumSize': 2}
    resolution = {'res_xy_nm': 100,'res_z_nm': 70}
    thresh = 0.9
    target_antibody_name1 = 'PSD95m_1st.tif'

    target_antibody_name2 = 'PSD95r_2nd.tif'
    query2 = {'preIF': ['synapsin_1st.tif'], 'preIF_z': [2],
            'postIF': ['PSD95r_2nd.tif'], 'postIF_z': [2],
            'punctumSize': 2}

    measure_list = run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)

    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    
    print('PSD-95 dataframe: ')
    print(df)
    

    return df

def run_pairwise(query1, query2, target_antibody_name1, target_antibody_name2,
                 base_dir, thresh, resolution):
    """
    Run pairwise

    Parameters
    -------------
    query1 : dict
    query2 : dict
    target_antibody_name1 : str
    target_antibody_name2 : str
    base_dir : str
    thresh : float
    resultion : dict 

    Return
    -------------
    [measure1, measure2] : list of AntibodyAnalysis objects
    """

    synaptic_volumes1 = da.load_tiff_from_query(query1, base_dir)
    measure1 = aa.run_ab_analysis(synaptic_volumes1, query1, thresh, resolution, target_antibody_name1)

    synaptic_volumes2 = da.load_tiff_from_query(query2, base_dir)
    measure2 = aa.run_ab_analysis(synaptic_volumes2, query2, thresh, resolution, target_antibody_name2)

    return [measure1, measure2]



# Function to look at pairwise comparisons
def synapsin_pairwise():
    """
    Synapsin Pairwise

    Return
    -----------
    df : dataframe
    """
    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/pairwise/KDM-SYN-090210/Synapsin/'
    resolution = {'res_xy_nm': 100,'res_z_nm': 70}
    thresh = 0.9

    query1 = {'preIF': ['synapsinGP1stA.tif'], 'preIF_z': [2],
              'postIF': ['psd1stA.tif'], 'postIF_z': [2],
              'punctumSize': 2}

    target_antibody_name1 = 'synapsinGP1stA.tif'
    target_antibody_name2 = 'synapsinR1stA.tif'

    query2 = {'preIF': ['synapsinR1stA.tif'], 'preIF_z': [2],
            'postIF': ['psd1stA.tif'], 'postIF_z': [2],
            'punctumSize': 2}

    measure_list = run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)

    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    
    print('Synapsin dataframe: ')
    print(df)

    return df
   

def gephyrin_pairwise():
    """
    Gephyrin Pairwise
    
    Return
    ---------------
    df : dataframe
    """
    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/pairwise/KDM-SYN-161213/gephyrin/'

    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9
    
    target_antibody_name1 = 'GephyrinL106-83.tif'
    query1 = {'preIF': ['GAD_L106-83.tif'], 'preIF_z': [2],
              'postIF': ['GephyrinL106-83.tif'], 'postIF_z': [2],
              'punctumSize': 2}

    target_antibody_name2 = 'GephyrinBD.tif'
    query2 = {'preIF': ['GAD_BD.tif'], 'preIF_z': [2],
            'postIF': ['GephyrinBD.tif'], 'postIF_z': [2],
            'punctumSize': 2}

    measure_list = run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)

    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    
    print('Gephyrin dataframe: ')
    print(df)

    return df

def vglut1_pairwise():
    """
    VGLUT1 pairwise comparison 

    Return
    ----------
    df : dataframe

    """

    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/pairwise/KDM-SYN-090210/VGluT1/';

    resolution = {'res_xy_nm': 100,'res_z_nm': 70}
    thresh = 0.9

    query1 = {'preIF': ['VGlut1GP1stA.tif', 'synapsin1stA.tif'], 'preIF_z': [2, 2],
              'postIF': [], 'postIF_z': [],
              'punctumSize': 2}

    target_antibody_name1 = 'VGlut1GP1stA.tif'
    target_antibody_name2 = 'VGlut1M1stA.tif'

    query2 = {'preIF': ['VGlut1M1stA.tif', 'synapsin1stA.tif'], 'preIF_z': [2, 2],
            'postIF': [], 'postIF_z': [],
            'punctumSize': 2}

    measure_list = run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)

    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    
    print('VGLUT1 dataframe: ')
    print(df)

    return df



def cav31_pairwise():
    """
    CAV31 pairwise comparison

    Return
    ---------
    df : dataframe
    """

    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/pairwise/KDM-MH-131023/Cav3.1/'

    resolution = {'res_xy_nm': 100,'res_z_nm': 70}
    thresh = 0.9

    query1 = {'preIF': ['VGluT1_1st_A.tif'], 'preIF_z': [2],
              'postIF': ['Cav31M_1st_A.tif'], 'postIF_z': [2],
              'punctumSize': 2}

    target_antibody_name1 = 'Cav31M_1st_A.tif'
    target_antibody_name2 = 'Cav31R_1st_A.tif'

    query2 = {'preIF': ['VGluT1_1st_A.tif'], 'preIF_z': [2],
            'postIF': ['Cav31R_1st_A.tif'], 'postIF_z': [2],
            'punctumSize': 2}

    measure_list = run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)

    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    
    print('CAV31 dataframe: ')
    print(df)

    return df


def main():
    """Run pairwise comparisons and save to an excel file"""

    gephyrin_df = gephyrin_pairwise()
    cav31_df = cav31_pairwise()
    synapsin_df = synapsin_pairwise()
    psd_df = psd95_pairwise()
    vglut1_df = vglut1_pairwise()


    sheet_name = 'Pairwise'
    fn = 'pairwise_comparisons.xlsx'
    df_list = [synapsin_df, vglut1_df, psd_df, gephyrin_df, cav31_df]
    aa.write_dfs_to_excel(df_list, sheet_name, fn)



if __name__ == '__main__':
    main()

