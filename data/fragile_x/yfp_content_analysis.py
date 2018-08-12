"""
Quantify the amount of YFP signal in each volume
"""
import os
import numpy as np
import pandas as pd
from at_synapse_detection import SynapseDetection as syn
from at_synapse_detection import dataAccess as da
from at_synapse_detection import antibodyAnalysis as aa


def measure_yfp(vol, thresh):
    """ measure the number of yfp voxels in a volume

    Parameters
    ------------
    vol - 3d numpy array 
    thresh - float threshold
    Return
    -----------
    result - int 
    """
    probvol = syn.getProbMap(vol)
    probvol = probvol > thresh
    result = np.sum(probvol)
    return result


def iterate_yfp_volumes():
    """Iterate through all the YFP volumes 
    Returns
    -----------
    vol_name_list
    signal_list
    """

    mouse_num_list = [2, 3, 4, 5, 6, 7]
    mouse_base_fn = 'ss_stacks'
    region_list = ['F000', 'F001', 'F002', 'F003']
    data_dir = '/data5TB/yi_mice/'
    filebase = 'ss_YFP.tif'
    vol_name_list = []
    signal_list = []
    thresh = 0.9

    for mouse_num in mouse_num_list:
        for region_name in region_list:
            vol_dir = os.path.join(data_dir, str(
                mouse_num) + mouse_base_fn, region_name, str(mouse_num) + filebase)
            vol_name = str(mouse_num) + mouse_base_fn + '-' + region_name
            vol_name_list.append(vol_name)
            vol = da.imreadtiff(vol_dir)
            result = measure_yfp(vol, thresh)
            signal_list.append(result)
            print(vol_dir, result)

    return vol_name_list, signal_list


def write_df(vol_name_list, signal_list, output_fn):
    """Save signal measurement results as a df

    Paramters
    ---------------
    vol_name_list : list of strs 
    signal_list : list of floats 
    output_fn : str - output filename

    Return
    ----------------
    df : dataframe
    """

    column_labels = ['YFP Size']
    df = pd.DataFrame(np.nan, index=vol_name_list, columns=column_labels)

    df.iloc[:, 0] = signal_list
    sheet_name = 'YFP Size'
    df_list = [df]

    aa.write_dfs_to_excel(df_list, sheet_name, output_fn)

    return df


def main():
    vol_name_list, signal_list = iterate_yfp_volumes()
    output_fn = 'yfpsize.xlsx'

    write_df(vol_name_list, signal_list, output_fn)


if __name__ == '__main__':
    main()
