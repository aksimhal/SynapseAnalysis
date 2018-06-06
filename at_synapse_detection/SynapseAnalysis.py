"""Synapse Analysis"""
import os
import numpy as np
import pandas as pd
from skimage import measure
from at_synapse_detection import SynapseDetection as syn
from at_synapse_detection import dataAccess as da
from at_synapse_detection import antibodyAnalysis as aa
from PIL import Image


class SynapseAnalysis:
    """
    Measurements necessary for comparing synapse populations 
    """

    def __init__(self, query):
        """
        """
        self.synapse_density = 0.0
        self.num_synapses = 0
        self.volume_um3 = 0.0
        self.query = query


def compute_measurements(resultvol, query, volume_um3, thresh):
    """
    """
    queryresult = SynapseAnalysis(query)
    queryresult.volume_um3 = volume_um3

    label_vol = measure.label(resultvol > thresh)
    stats = measure.regionprops(label_vol)
    queryresult.synapse_density = len(stats) / queryresult.volume_um3
    queryresult.num_synapses = len(stats)

    return queryresult


def create_synapse_df(result_list, row_labels):
    """

    Paramters
    ------------

    Return
    -------------
    df : dataframe
    """
    column_labels = ['Synapse Density', 'Synapse Count']

    df = pd.DataFrame(np.nan, index=row_labels, columns=column_labels)

    for n, queryresult in enumerate(result_list):
        df.iloc[n, 0] = queryresult.synapse_density
        df.iloc[n, 1] = queryresult.num_synapses

    return df


def run_synapse_detection(atet_input):
    """
    Run synapse detection and result evalution.  The parameters need to be rethought 

    Parameters
    -------------------
    atet_input : dict 

    Returns
    -------------------
    output_dict : dict 

    """

    query = atet_input['query']
    queryID = atet_input['queryID']
    nQuery = atet_input['nQuery']
    resolution = atet_input['resolution']
    data_location = atet_input['data_location']
    data_region_location = atet_input['data_region_location']
    output_foldername = atet_input['output_foldername']
    region_name = atet_input['region_name']
    mask_str = atet_input['mask_str']

    # Load the data
    synaptic_volumes = da.load_tiff_from_query(query, data_region_location)

    # Load mask
    mask = Image.open(mask_str)
    mask = np.array(mask)
    # Mask data
    synaptic_volumes = mask_synaptic_volumes(synaptic_volumes, mask)

    volume_um3 = get_masked_volume(synaptic_volumes, mask, resolution)
    print(volume_um3)

    # Run Synapse Detection
    print('running synapse detection')
    resultvol = syn.getSynapseDetections(synaptic_volumes, query)

    # Save the probability map to file, if you want
    # outputNPYlocation = os.path.join(
    #     data_location, output_foldername, region_name)
    # syn.saveresultvol(resultvol, outputNPYlocation, 'query_', queryID)

    thresh = 0.9
    queryresult = compute_measurements(
        resultvol, query, volume_um3, thresh)

    output_dict = {'queryID': queryID,
                   'query': query, 'queryresult': queryresult}
    return output_dict


def run_synapse_detection_astro(atet_input):
    """
    Run synapse detection and result evalution.  The parameters need to be rethought 

    Parameters
    -------------------
    atet_input : dict 

    Returns
    -------------------
    output_dict : dict 

    """

    query = atet_input['query']
    queryID = atet_input['queryID']
    nQuery = atet_input['nQuery']
    resolution = atet_input['resolution']
    data_location = atet_input['data_location']
    data_region_location = atet_input['data_region_location']
    output_foldername = atet_input['output_foldername']
    region_name = atet_input['region_name']
    mask_str = atet_input['mask_str']

    # Load the data
    synaptic_volumes = da.load_tiff_from_query(query, data_region_location)

    volume_um3 = aa.getdatavolume(synaptic_volumes, resolution)
    print(volume_um3)

    # Run Synapse Detection
    print('running synapse detection')
    resultvol = syn.getSynapseDetections_astro(synaptic_volumes, query)

    # Save the probability map to file, if you want
    # outputNPYlocation = os.path.join(
    #     data_location, output_foldername, region_name)
    # syn.saveresultvol(resultvol, outputNPYlocation, 'query_', queryID)

    thresh = 0.9
    queryresult = compute_measurements(
        resultvol, query, volume_um3, thresh)

    output_dict = {'queryID': queryID,
                   'query': query, 'queryresult': queryresult}
    return output_dict


def organize_result_lists(result_list):
    """
    output_dict = {'queryID': queryID,
                   'query': query, 'queryresult': queryresult}
    """
    query_inds = []
    list_of_queryresult = []
    for result in result_list:
        query_inds.append(result['queryID'])
        list_of_queryresult.append(result['queryresult'])

    sorted_inds = np.argsort(query_inds)
    sorted_queryresult = [list_of_queryresult[n] for n in sorted_inds]

    return sorted_queryresult


def mask_synaptic_volumes(synaptic_volumes, mask):
    """
    Mask synaptic volumes 

    Parameters
    -------------
    synaptic_volumes : dict 
    mask : 2D array 

    Returns 
    --------------
    synaptic_volumes : dict 
    """

    keys = synaptic_volumes.keys()
    masked_synaptic_volumes = {key: [] for key in keys}

    for key in synaptic_volumes.keys():
        print(key)
        for volume in synaptic_volumes[key]:
            maskedVol = np.zeros(volume.shape)
            for sliceInd in range(0, volume.shape[2]):
                maskedVol[:, :, sliceInd] = volume[:, :, sliceInd] * mask
            masked_synaptic_volumes[key].append(maskedVol)

    return masked_synaptic_volumes


def get_masked_volume(synaptic_volumes, mask, resolution):
    """
    Compute volume of data in cubic microns

    Parameters
    -------------
    synaptic_volumes : dict
    resolution : dict
    mask : numpy 2d array

    Return
    --------------
    volume_um3 : double
    """

    res_xy_nm = resolution['res_xy_nm']
    res_z_nm = resolution['res_z_nm']

    slice_volume_um3 = np.count_nonzero(
        mask) * (res_xy_nm / 1000) * (res_xy_nm / 1000)

    # Compute Volume
    if len(synaptic_volumes['presynaptic']) > 0:
        volume_um3 = np.prod(
            synaptic_volumes['presynaptic'][0].shape[2]) * (res_z_nm / 1000) * slice_volume_um3

    elif len(synaptic_volumes['postsynaptic']) > 0:
        volume_um3 = np.prod(
            synaptic_volumes['postsynaptic'][0].shape[2]) * (res_z_nm / 1000) * slice_volume_um3

    return volume_um3
