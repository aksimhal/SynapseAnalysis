import os
import numpy as np
import pandas as pd
from skimage import measure
from at_synapse_detection import antibodyAnalysis as aa


def run_combos(queryID1, queryID2):
    """
    """
    mouse_num_list = [1, 2, 3, 4, 5, 6, 7, 22]
    mouse_base_fn = 'ss_stacks'
    region_list = ['F000', 'F001', 'F002', 'F003']
    data_dir = '/data5TB/yi_mice/'

    vol_name_list = []
    signal_list = []

    for mouse_num in mouse_num_list:
        print(mouse_num)
        queryoffset = 12
        for region_ind, region_name in enumerate(region_list):
            vol_dir_base = os.path.join(data_dir, str(
                mouse_num) + mouse_base_fn, 'results_' + str(mouse_num) + 'ss_fragX', region_name)

            vol_name = str(mouse_num) + 'ss_' + region_name
            vol_name_list.append(vol_name)

            fn1 = os.path.join(vol_dir_base, 'query_' +
                               str(queryID1 + region_ind * queryoffset) + '.npy')
            fn2 = os.path.join(vol_dir_base, 'query_' +
                               str(queryID2 + region_ind * queryoffset) + '.npy')
            print("fn1: ", fn1)
            print("fn2: ", fn2)

            vol1 = np.load(fn1)
            vol2 = np.load(fn2)
            thresh = 0.9
            lvol1 = measure.label(vol1 > thresh)
            stats1 = measure.regionprops(lvol1)
            lvol2 = measure.label(vol2 > thresh)
            stats2 = measure.regionprops(lvol2)

            centroid_list = np.zeros((len(stats2), 3))
            for n, stat in enumerate(stats2):
                centroid_list[n, :] = stat.centroid

            close_synapse_list = np.zeros((len(stats1), 1))
            for n, stat1 in enumerate(stats1):
                cpt = stat1.centroid
                cpt_tile = np.tile(cpt, (len(stats2), 1))

                distance_list = np.sqrt(
                    0.1 * np.power(cpt_tile[:, 0] - centroid_list[:, 0], 2) +
                    0.1 * np.power(cpt_tile[:, 1] - centroid_list[:, 1], 2) +
                    0.07 * np.power(cpt_tile[:, 2] - centroid_list[:, 2], 2))

                close_synapses = distance_list < 1.1
                close_synapse_list[n] = np.sum(close_synapses)

            percent = np.count_nonzero(
                close_synapse_list) / len(close_synapse_list)
            print(percent)
            signal_list.append(percent)

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

    column_labels = ['Percentage']
    df = pd.DataFrame(np.nan, index=vol_name_list, columns=column_labels)

    df.iloc[:, 0] = signal_list
    sheet_name = 'Synapses'
    df_list = [df]

    aa.write_dfs_to_excel(df_list, sheet_name, output_fn)

    return df


def main():

    vol_name_list, signal_list = run_combos(queryID1=5, queryID2=7)
    write_df(vol_name_list, signal_list, 'vglut1_vs_inhibitory.xlsx')

    vol_name_list, signal_list = run_combos(queryID1=6, queryID2=7)
    write_df(vol_name_list, signal_list, 'vglut2_vs_inhibitory.xlsx')


if __name__ == '__main__':
    main()
