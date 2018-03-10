"""
Run Pairwise Comparisons for multiple queries
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
    list_of_df : dataframe list
    """
    list_of_df = []
    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/pairwise/KDM-RW-120419/'
    resolution = {'res_xy_nm': 100,'res_z_nm': 70}
    thresh = 0.9
    target_antibody_name1 = 'PSD95m_1st.tif'
    target_antibody_name2 = 'PSD95r_2nd.tif'

    # QUERY 1
    query1 = {'preIF': ['synapsin_1st.tif'], 'preIF_z': [1],
            'postIF': ['PSD95m_1st.tif'], 'postIF_z': [1],
            'punctumSize': 2}
    query2 = {'preIF': ['synapsin_1st.tif'], 'preIF_z': [1],
            'postIF': ['PSD95r_2nd.tif'], 'postIF_z': [1],
            'punctumSize': 2}
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('PSD-95 dataframe: ')
    print(df)

    # QUERY 2
    query1['preIF_z'] = [1]
    query1['postIF_z'] = [2]
    query2['preIF_z'] = [1]
    query2['postIF_z'] = [2]
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('PSD-95 dataframe: ')
    print(df)

    # QUERY 3
    query1['preIF_z'] = [2]
    query1['postIF_z'] = [2]
    query2['preIF_z'] = [2]
    query2['postIF_z'] = [2]
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('PSD-95 dataframe: ')
    print(df)

    # QUERY 4
    query1['preIF_z'] = [1]
    query1['postIF_z'] = [3]
    query2['preIF_z'] = [1]
    query2['postIF_z'] = [3]
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('PSD-95 dataframe: ')
    print(df)

    return list_of_df


def synapsin_pairwise():
    """
    Synapsin Pairwise

    Return
    -----------
    list_of_df : dataframe list
    """
    list_of_df = []
    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/pairwise/KDM-SYN-090210/Synapsin/'
    resolution = {'res_xy_nm': 100,'res_z_nm': 70}
    thresh = 0.9
    target_antibody_name1 = 'synapsinGP1stA.tif'
    target_antibody_name2 = 'synapsinR1stA.tif'

    # QUERY 1
    query1 = {'preIF': ['synapsinGP1stA.tif'], 'preIF_z': [1],
              'postIF': ['psd1stA.tif'], 'postIF_z': [1],
              'punctumSize': 2}
    query2 = {'preIF': ['synapsinR1stA.tif'], 'preIF_z': [1],
            'postIF': ['psd1stA.tif'], 'postIF_z': [1],
            'punctumSize': 2}
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('Synapsin dataframe: ')
    print(df)

    # QUERY 2
    query1['preIF_z'] = [2]
    query1['postIF_z'] = [1]
    query2['preIF_z'] = [2]
    query2['postIF_z'] = [1]
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('Synapsin dataframe: ')
    print(df)

    # QUERY 3
    query1['preIF_z'] = [2]
    query1['postIF_z'] = [2]
    query2['preIF_z'] = [2]
    query2['postIF_z'] = [2]
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('Synapsin dataframe: ')
    print(df)

    # QUERY 4
    query1['preIF_z'] = [3]
    query1['postIF_z'] = [1]
    query2['preIF_z'] = [3]
    query2['postIF_z'] = [1]
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('Synapsin dataframe: ')
    print(df)


    return list_of_df


def gephyrin_pairwise():
    """
    Gephyrin Pairwise

    Return
    ---------------
    list_of_df : dataframe list
    """
    list_of_df = []
    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/pairwise/KDM-SYN-161213/gephyrin/'
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9
    target_antibody_name1 = 'GephyrinL106-83.tif'
    target_antibody_name2 = 'GephyrinBD.tif'

    # QUERY 1
    query1 = {'preIF': ['GAD_L106-83.tif'], 'preIF_z': [1],
              'postIF': ['GephyrinL106-83.tif'], 'postIF_z': [1],
              'punctumSize': 2}
    query2 = {'preIF': ['GAD_BD.tif'], 'preIF_z': [1],
            'postIF': ['GephyrinBD.tif'], 'postIF_z': [1],
            'punctumSize': 2}
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('Gephyrin dataframe: ')
    print(df)

    # QUERY 2
    query1['preIF_z'] = [1]
    query1['postIF_z'] = [2]
    query2['preIF_z'] = [1]
    query2['postIF_z'] = [2]
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('Gephyrin dataframe: ')
    print(df)

    # QUERY 3
    query1['preIF_z'] = [2]
    query1['postIF_z'] = [2]
    query2['preIF_z'] = [2]
    query2['postIF_z'] = [2]
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('Gephyrin dataframe: ')
    print(df)

    # QUERY 4
    query1['preIF_z'] = [1]
    query1['postIF_z'] = [3]
    query2['preIF_z'] = [1]
    query2['postIF_z'] = [3]
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('Gephyrin dataframe: ')
    print(df)

    return list_of_df

def vglut1_pairwise():
    """
    VGLUT1 pairwise comparison

    Return
    ----------
    list_of_df : dataframe list

    """
    list_of_df = []
    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/pairwise/KDM-SYN-090210/VGluT1/'
    resolution = {'res_xy_nm': 100,'res_z_nm': 70}
    thresh = 0.9
    target_antibody_name1 = 'VGlut1GP1stA.tif'
    target_antibody_name2 = 'VGlut1M1stA.tif'

    query1 = {'preIF': ['VGlut1GP1stA.tif', 'synapsin1stA.tif'], 'preIF_z': [1, 1],
              'postIF': [], 'postIF_z': [],
              'punctumSize': 2}
    query2 = {'preIF': ['VGlut1M1stA.tif', 'synapsin1stA.tif'], 'preIF_z': [1, 1],
            'postIF': [], 'postIF_z': [],
            'punctumSize': 2}
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('VGLUT1 dataframe: ')
    print(df)

    # QUERY 2
    query1['preIF_z'] = [2, 1]
    query2['preIF_z'] = [2, 1]
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('VGLUT1 dataframe: ')
    print(df)

    # QUERY 3
    query1['preIF_z'] = [2, 2]
    query2['preIF_z'] = [2, 2]
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('VGLUT1 dataframe: ')
    print(df)

    # QUERY 4
    query1['preIF_z'] = [3, 1]
    query2['preIF_z'] = [3, 1]
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('VGLUT1 dataframe: ')
    print(df)

    return list_of_df



def cav31_pairwise():
    """
    CAV31 pairwise comparison

    Return
    ---------
    list_of_df : dataframe list
    """
    list_of_df = []
    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/pairwise/KDM-MH-131023/Cav3.1/'
    resolution = {'res_xy_nm': 100,'res_z_nm': 70}
    thresh = 0.9
    target_antibody_name1 = 'Cav31M_1st_A.tif'
    target_antibody_name2 = 'Cav31R_1st_A.tif'

    # QUERY 1
    query1 = {'preIF': ['VGluT1_1st_A.tif'], 'preIF_z': [1],
              'postIF': ['Cav31M_1st_A.tif'], 'postIF_z': [1],
              'punctumSize': 2}
    query2 = {'preIF': ['VGluT1_1st_A.tif'], 'preIF_z': [1],
            'postIF': ['Cav31R_1st_A.tif'], 'postIF_z': [1],
            'punctumSize': 2}
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('CAV31 dataframe: ')
    print(df)

    # QUERY 2
    query1['preIF_z'] = [1]
    query1['postIF_z'] = [2]
    query2['preIF_z'] = [1]
    query2['postIF_z'] = [2]
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('CAV31 dataframe: ')
    print(df)

    # QUERY 3
    query1['preIF_z'] = [2]
    query1['postIF_z'] = [2]
    query2['preIF_z'] = [2]
    query2['postIF_z'] = [2]
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('CAV31 dataframe: ')
    print(df)

    # QUERY 4
    query1['preIF_z'] = [1]
    query1['postIF_z'] = [3]
    query2['preIF_z'] = [1]
    query2['postIF_z'] = [3]
    measure_list = aa.run_pairwise(query1, query2, target_antibody_name1,
                                target_antibody_name2, base_dir, thresh, resolution)
    df = aa.create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    list_of_df.append(df)
    print('CAV31 dataframe: ')
    print(df)

    return list_of_df

def main():
    """Run pairwise comparisons and save to an excel file"""

    cav31_dflist = cav31_pairwise()
    gephyrin_dflist = gephyrin_pairwise()
    synapsin_dflist = synapsin_pairwise()
    psd_dflist = psd95_pairwise()
    vglut1_dflist = vglut1_pairwise()

    sheet_name = 'Pairwise'
    fn = 'pairwise_comparisons2.xlsx'
    df_list = synapsin_dflist + vglut1_dflist + psd_dflist + gephyrin_dflist + cav31_dflist
    aa.write_dfs_to_excel(df_list, sheet_name, fn)

if __name__ == '__main__':
    main()

