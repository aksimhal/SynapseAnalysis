"""
Compare puncta distribution in a channel with synapse distribution. 
"""
import os
import copy
import socket

import numpy as np
import pandas as pd
from skimage import measure
from at_synapse_detection import SynapseDetection as syn
from at_synapse_detection import dataAccess as da
from at_synapse_detection import antibodyAnalysis as aa


def run_SACT_FXS(synaptic_volumes, query, thresh, resolution, target_antibody_name, result_location):
    """
    Run SACT. 

    MEASURES
    - Puncta Density
    - Average punctum size
    - Standard deviation of the size
    - Synapse density
    - Target Specificity Ratio (tsr)
    - Raw data mean/std

    Parameters
    -----------
    synaptic_volumes : dict - has two keys, 'postsynaptic' and 'presynaptic.' Each key contains a list of volumes. 
    query : dict
    thresh : float
    resolution : dict

    Returns
    -----------
    antibody_measure : AntibodyAnalysis()
    """

    antibody_measure = aa.AntibodyAnalysis(query)

    # Get data volume
    antibody_measure.volume_um3 = aa.getdatavolume(
        synaptic_volumes, resolution)
    print('data volume: ', antibody_measure.volume_um3, 'um3')

    # Check to see if user supplied blobsize
    if 'punctumSize' in query.keys():
        blobsize = query['punctumSize']
        edge_win = int(np.ceil(blobsize * 1.5))

    # Data
    presynaptic_volumes = synaptic_volumes['presynaptic']
    postsynaptic_volumes = synaptic_volumes['postsynaptic']

    # Number of slices each blob should span
    preIF_z = query['preIF_z']
    postIF_z = query['postIF_z']

    # Compute raw mean and standard deviation
    antibody_measure = aa.compute_raw_measures(
        presynaptic_volumes, antibody_measure, 'presynaptic')

    # SNR test
    raw_presynaptic_volumes = []
    for vol in presynaptic_volumes:
        raw_presynaptic_volumes.append(np.copy(vol))

    for n in range(0, len(presynaptic_volumes)):
        presynaptic_volumes[n] = syn.getProbMap(
            presynaptic_volumes[n])  # Step 1
        presynaptic_volumes[n] = syn.convolveVolume(
            presynaptic_volumes[n], blobsize)  # Step 2
        if preIF_z[n] > 1:
            factor_vol = syn.computeFactor(
                presynaptic_volumes[n], int(preIF_z[n]))  # Step 3
            presynaptic_volumes[n] = presynaptic_volumes[n] * factor_vol

    # Compute single channel measurements
    antibody_measure = aa.compute_single_channel_measurements(
        presynaptic_volumes, antibody_measure, thresh, 'presynaptic')

    # SNR test
    antibody_measure = aa.compute_SNR_synapticside(raw_presynaptic_volumes,
                                                   presynaptic_volumes, thresh,
                                                   antibody_measure, 'presynaptic')

    print('Computed presynaptic single channel measurements')

    # Compute raw mean and standard deviation
    antibody_measure = aa.compute_raw_measures(
        postsynaptic_volumes, antibody_measure, 'postsynaptic')

    # SNR test
    raw_postsynaptic_volumes = []
    for vol in postsynaptic_volumes:
        raw_postsynaptic_volumes.append(np.copy(vol))

    for n in range(0, len(postsynaptic_volumes)):
        postsynaptic_volumes[n] = syn.getProbMap(
            postsynaptic_volumes[n])  # Step 1
        postsynaptic_volumes[n] = syn.convolveVolume(
            postsynaptic_volumes[n], blobsize)  # Step 2
        if postIF_z[n] > 1:
            factor_vol = syn.computeFactor(
                postsynaptic_volumes[n], int(postIF_z[n]))  # Step 3
            postsynaptic_volumes[n] = postsynaptic_volumes[n] * factor_vol

    # Compute single channel measurements
    antibody_measure = aa.compute_single_channel_measurements(
        postsynaptic_volumes, antibody_measure, thresh, 'postsynaptic')

    # SNR test
    antibody_measure = aa.compute_SNR_synapticside(raw_postsynaptic_volumes,
                                                   postsynaptic_volumes, thresh,
                                                   antibody_measure, 'postsynaptic')
    print('Computed postsynaptic single channel measurements')

    # Load result volume
    resultVol = np.load(result_location)

    # Compute whole statistics
    label_vol = measure.label(resultVol > thresh)
    stats = measure.regionprops(label_vol)
    antibody_measure.synapse_density = len(stats) / antibody_measure.volume_um3
    antibody_measure.synapse_count = len(stats)

    antibody_measure = aa.calculuate_target_ratio(
        antibody_measure, target_antibody_name)

    return antibody_measure


def run_blob_synapse(mouse_number, mouse_project_str, base_query_num, channel_name):
    """
    Blob Synapse Ratio.  Run SACT for FXS data
    Only runs on Galicia
    """

    query_fn = 'queries/' + mouse_project_str + '_queries.json'

    hostname = socket.gethostname()
    if hostname == 'Galicia':
        data_location = '/data5TB/yi_mice/' + str(mouse_number) + 'ss_stacks'
    listOfQueries = syn.loadQueriesJSON(query_fn)

    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    region_name_base = 'F00'
    thresh = 0.9

    mask_location_str = -1  # no mask specified
    foldernames = []
    measure_list = []
    target_filenames = []
    conjugate_filenames = []

    for region_num in range(0, 4):
        region_name = region_name_base + str(region_num)
        data_region_location = os.path.join(data_location, region_name)

        query = listOfQueries[base_query_num]
        nQuery = base_query_num
        foldername = region_name + '-Q' + str(nQuery)
        foldernames.append(foldername)
        conjugate_filenames.append('Query' + str(base_query_num))
        # Load the data
        synaptic_volumes = da.load_tiff_from_query(
            query, data_region_location)

        target_antibody_name = str(mouse_number) + channel_name
        target_filenames.append(target_antibody_name)
        query_number = nQuery + 12 * region_num
        result_location = os.path.join(data_location, str(
            mouse_number) + 'ss_fragX', region_name, 'query_' + str(query_number) + '.npy')

        antibody_measure = run_SACT_FXS(
            synaptic_volumes, query, thresh, resolution, target_antibody_name, result_location)

        measure_list.append(antibody_measure)

    mouse_df = aa.create_df(measure_list, foldernames,
                            target_filenames, conjugate_filenames)

    return mouse_df


def iterate_over_mice(query_number, channel_name):
    mouse_list = [1, 2, 3, 4, 5, 6, 7, 22]

    df_list = []
    for num in mouse_list:
        mouse_df = run_blob_synapse(
            num, str(num) + 'ss', query_number, channel_name)
        df_list.append(mouse_df)

    return df_list


def iterate_over_queries():
    channel_name = 'ss_PSD.tif'
    df_list = iterate_over_mice(0, channel_name)
    aa.write_dfs_to_excel(df_list, 'blob_synapse', 'blob_synapse.xlsx')


def main():
    iterate_over_queries()


if __name__ == '__main__':
    main()
