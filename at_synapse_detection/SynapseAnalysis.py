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
    layer_mask_str = atet_input['mask_str']
    dapi_mask_str = atet_input['dapi_mask_str']
    mouse_number = atet_input['mouse_number']

    # Load the data
    synaptic_volumes = da.load_tiff_from_query(query, data_region_location)

    # Load layer mask
    if layer_mask_str != -1:
        layer_mask = Image.open(layer_mask_str)
        layer_mask = np.array(layer_mask)

    # Load DAPI mask
    dapi_mask_fn = os.path.join(dapi_mask_str, str(
        mouse_number) + 'ss-DAPI-mask.tiff')
    dapi_mask = da.imreadtiff(dapi_mask_fn)

    # Merge DAPI mask and Layer 4 mask
    if layer_mask_str != -1:
        combined_mask = merge_DAPI_L4_masks(layer_mask, dapi_mask)
    else:
        dapi_mask = dapi_mask.astype(np.bool)
        combined_mask = np.logical_not(dapi_mask)  # keep portions without dapi

    # Mask data
    synaptic_volumes = mask_synaptic_volumes(synaptic_volumes, combined_mask)

    volume_um3 = get_masked_volume(synaptic_volumes, combined_mask, resolution)
    print(volume_um3)

    # Run Synapse Detection
    print('running synapse detection')
    resultvol = syn.getSynapseDetections(synaptic_volumes, query)

    # Save the probability map to file, if you want
    outputNPYlocation = os.path.join(
        data_location, output_foldername, region_name)
    syn.saveresultvol(resultvol, outputNPYlocation, 'query_', queryID)

    thresh = 0.9
    queryresult = compute_measurements(
        resultvol, query, volume_um3, thresh)

    output_dict = {'queryID': queryID,
                   'query': query, 'queryresult': queryresult}
    return output_dict


def merge_DAPI_L4_masks(layer_mask, dapi_mask):
    """
    Combine the layer 4 mask and dapi mask into a single mask 
    px=1 good, px=0 bad 

    Parameters 
    --------------
    layer_mask - 3D numpy array.  ones indicate good region (uint8)
    dapi_mask - 3D numpy array. ones indicate dapi or tears (uint8)

    Return
    --------------
    combined_mask - 3D array. ones - good regions (bool)
    """
    # convert to boolean
    dapi_mask = dapi_mask.astype(np.bool)
    layer_mask = layer_mask.astype(np.bool)
    # invert dapi mask
    dapi_mask = np.logical_not(dapi_mask)
    # tile layer mask
    layer_mask_3d = np.zeros(dapi_mask.shape, dtype=np.bool)
    for n in range(0, layer_mask_3d.shape[2]):
        layer_mask_3d[:, :, n] = layer_mask

    combined_mask = np.logical_and(layer_mask_3d, dapi_mask)

    return combined_mask


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
    layer_mask_str = atet_input['mask_str']
    dapi_mask_str = atet_input['dapi_mask_str']
    mouse_number = atet_input['mouse_number']

    # Load the data
    synaptic_volumes = da.load_tiff_from_astro_query(
        query, data_region_location)

    # Load DAPI mask
    dapi_mask_fn = os.path.join(dapi_mask_str, str(
        mouse_number) + 'ss-DAPI-mask.tiff')
    dapi_mask = da.imreadtiff(dapi_mask_fn)
    dapi_mask = dapi_mask.astype(np.bool)
    combined_mask = np.logical_not(dapi_mask)
    # Mask data
    synaptic_volumes = mask_synaptic_volumes(synaptic_volumes, combined_mask)

    volume_um3 = get_masked_volume(synaptic_volumes, combined_mask, resolution)
    print(volume_um3)

    # Run Synapse Detection
    print('running synapse detection')
    resultvol = syn.getSynapseDetections_astro(synaptic_volumes, query)

    # Save the probability map to file, if you want
    outputNPYlocation = os.path.join(
        data_location, output_foldername, region_name)
    syn.saveresultvol(resultvol, outputNPYlocation, 'query_', queryID)

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
                maskedVol[:, :, sliceInd] = volume[:,
                                                   :, sliceInd] * mask[:, :, sliceInd]
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
        mask) * (res_xy_nm / 1000) * (res_xy_nm / 1000) * (res_z_nm / 1000)

    volume_um3 = slice_volume_um3
    # Compute Volume
    # if len(synaptic_volumes['presynaptic']) > 0:
    #     volume_um3 = np.prod(
    #         synaptic_volumes['presynaptic'][0].shape[2]) * (res_z_nm / 1000) * slice_volume_um3

    # elif len(synaptic_volumes['postsynaptic']) > 0:
    #     volume_um3 = np.prod(
    #         synaptic_volumes['postsynaptic'][0].shape[2]) * (res_z_nm / 1000) * slice_volume_um3

    return volume_um3
