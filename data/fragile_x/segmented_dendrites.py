"""
Quantify the amount of YFP signal in each volume
"""
import os
import subprocess
import numpy as np
import pandas as pd
import skimage.morphology as morph
from skimage import measure
from at_synapse_detection import SynapseDetection as syn
from at_synapse_detection import dataAccess as da
from at_synapse_detection import antibodyAnalysis as aa


def segment_dendrites(vol, thresh, num_of_dendrites, output_dir):
    """ segment dendrites

    Parameters
    ------------
    vol - 3d numpy array 
    thresh - float threshold
    Return
    -----------
    result - int 
    """
    probvol = syn.getProbMap(vol)
    bw_vol = probvol > thresh
    SE = morph.ball(5)
    bw_vol = morph.closing(bw_vol, SE)
    label_vol = measure.label(bw_vol, connectivity=2)
    stats = measure.regionprops(label_vol)
    # sort by size
    size_list = []
    for stat in stats:
        size_list.append(stat.area)

    ind_list = np.flip(np.argsort(size_list), 0)

    for n in range(0, num_of_dendrites):
        dendrite = stats[ind_list[n]]
        list_of_coords = dendrite.coords
        list_of_coords = np.array(list_of_coords)
        filename = 'dendrite' + str(n) + '.off'
        output_filename = os.path.join(output_dir, filename)
        write_off_file(list_of_coords, output_filename)
        stl_filename = os.path.join(output_dir, 'dendrite' + str(n) + '.stl')
        print('number of points: ', str(len(list_of_coords)))

        if len(list_of_coords) < 40000:
            print('starting meshlab', output_filename)
            subprocess.call(["meshlabserver", "-i", output_filename,
                             "-o", stl_filename, "-s", "ballpivot.mlx"])
        else:
            print('starting meshlab subsampling', output_filename)
            subprocess.call(["meshlabserver", "-i", output_filename,
                             "-o", stl_filename, "-s", "ballpivot2.mlx"])

        print('stl created', stl_filename)

    return stl_filename


def write_off_file(list_of_coords, filename):
    """ Write .off file

    Parameters
    ---------------
    list_of_coords
    filename 
    """

    # fid = fopen('cs08_v3_r15.off','w');
    f = open(filename, "w")
    f.write('OFF\n')
    f.write(str(len(list_of_coords)) + ' 0 0\n')
    for n in range(len(list_of_coords)):
        f.write(str(list_of_coords[n, 0]) + ' ' + str(
            list_of_coords[n, 1]) + ' ' + str(list_of_coords[n, 2]) + '\n')


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
    num_of_dendrites = 10
    output_basedir = '/data5TB/yi_mice/segmented-dendrites'

    for mouse_num in mouse_num_list:
        for region_name in region_list:
            vol_dir = os.path.join(data_dir, str(
                mouse_num) + mouse_base_fn, region_name, str(mouse_num) + filebase)
            vol_name = str(mouse_num) + mouse_base_fn + '-' + region_name
            vol_name_list.append(vol_name)
            vol = da.imreadtiff(vol_dir)
            off_output_dir = os.path.join(output_basedir, str(
                mouse_num) + mouse_base_fn, region_name)

            dir_result = os.path.isdir(off_output_dir)
            if (dir_result == False):
                os.makedirs(off_output_dir)

            result = segment_dendrites(
                vol, thresh, num_of_dendrites, off_output_dir)
            print(vol_dir)


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
    iterate_yfp_volumes()


if __name__ == '__main__':
    main()
