"""
Run Pairwise Comparisons
"""
import numpy as np
import pandas as pd #also requires xlsxwriter
from at_synapse_detection import dataAccess as da
from at_synapse_detection import antibodyAnalysis as aa



def write_dfs_to_excel(df_list, sheets, file_name, spaces=1):
    """
    Write multiple dataframes to an excel file
    source:https://stackoverflow.com/questions/32957441/\
                   putting-many-python-pandas-dataframes-to-one-excel-worksheet

    Parameters 
    --------------
    df_list : list of dataframes 
    sheets : str - name of sheet in excel 
    file_name : str
    spaces : int - number of rows to skip, default = 1

    """

    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    row = 0
    for dataframe in df_list:
        dataframe.to_excel(writer, sheet_name=sheets, startrow=row, startcol=0)
        row = row + len(dataframe.index) + spaces + 1
    writer.save()


def find_target_measure(measure, target_ab_name):
    """Find target antibody measurement object

    Paramters 
    -----------
    measure : AntibodyAnalysis
    target_ab_name : str

    Return
    ------------
    target_measure : ABMeasures
    """
    for n in measure.postsynaptic_list:
        if n.name == target_ab_name:
            target_measure = n

    for n in measure.presynaptic_list:
        if n.name == target_ab_name:
            target_measure = n

    return target_measure

def find_conjugate_name(measure, target_ab_name):
    """Find conjugate antibody name

    Paramters 
    -----------
    measure : AntibodyAnalysis
    target_ab_name : str

    Return
    ------------
    conjugate_name : str
    """
    for n in measure.postsynaptic_list:
        if n.name != target_ab_name:
            conjugate_name = n.name

    for n in measure.presynaptic_list:
        if n.name != target_ab_name:
            conjugate_name = n.name

    return conjugate_name


def create_pairwise_df(measure1, measure2, target_antibody_name1, target_antibody_name2):
    """Create a dataframe for pairwise comparisons

    Paramters
    ------------
    measure1 : AntibodyAnalysis
    measure2 : AntibodyAnalysis
    target_antibody_name1 : str
    target_antibody_name2 : str

    Return
    ------------
    df : dataframe
    """

    columnlabels = ['Target AB', 'Conjugate AB', 'Puncta Density',
                    'Puncta Volume', 'Puncta STD', 'Synapse Density', 'TSR']
    df = pd.DataFrame(np.nan, index=['AB1','AB2'], columns=columnlabels)

    df.iloc[0, 0] = target_antibody_name1
    df.iloc[1, 0] = target_antibody_name2

    conjugate_ab_name = find_conjugate_name(measure1, target_antibody_name1)
    df.iloc[0, 1] = conjugate_ab_name
    target_measure = find_target_measure(measure1, target_antibody_name1)
    df.iloc[0, 2] = target_measure.puncta_density
    df.iloc[0, 3] = target_measure.puncta_size
    df.iloc[0, 4] = target_measure.puncta_std
    df.iloc[0, 5] = measure1.synapse_density
    df.iloc[0, 6] = measure1.specificity_ratio

    target_measure = find_target_measure(measure2, target_antibody_name2)
    conjugate_ab_name = find_conjugate_name(measure2, target_antibody_name2)
    df.iloc[1, 1] = conjugate_ab_name
    df.iloc[1, 2] = target_measure.puncta_density
    df.iloc[1, 3] = target_measure.puncta_size
    df.iloc[1, 4] = target_measure.puncta_std
    df.iloc[1, 5] = measure2.synapse_density
    df.iloc[1, 6] = measure2.specificity_ratio

    return df


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

    df = create_pairwise_df(measure_list[0], measure_list[1],
                            target_antibody_name1, target_antibody_name2)
    
    print('PSD--95 dataframe: ')
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

    df = create_pairwise_df(measure_list[0], measure_list[1],
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

    df = create_pairwise_df(measure_list[0], measure_list[1],
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

    df = create_pairwise_df(measure_list[0], measure_list[1],
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

    df = create_pairwise_df(measure_list[0], measure_list[1],
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
    write_dfs_to_excel(df_list, sheet_name, fn)



if __name__ == '__main__':
    main()

