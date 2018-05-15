"""Synapse Analysis"""
import os
import numpy as np
import pandas as pd
from skimage import measure
from at_synapse_detection import SynapseDetection as syn
from at_synapse_detection import dataAccess as da
from at_synapse_detection import antibodyAnalysis as aa


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


def run_synapses_astro(query_fn, data_location_base, outputFoldername):
    """
    """

    listOfQueries = syn.loadQueriesJSON(query_fn)
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    region_name_base = 'F00'
    thresh = 0.9

    foldernames = []
    result_list = []
    for region_num in range(0, 4):
        region_name = region_name_base + str(region_num)
        data_location = os.path.join(data_location_base, region_name)

        for n, query in enumerate(listOfQueries):
            print(query)
            foldername = region_name + '-Q' + str(n)
            foldernames.append(foldername)
            print(foldername)
            # Load the data

            synaptic_volumes = da.load_tiff_from_astro_query(
                query, data_location)
            volume_um3 = aa.getdatavolume(synaptic_volumes, resolution)

            # Run Synapse Detection
            resultvol = syn.getSynapseDetections_astro(synaptic_volumes, query)

            # Save the probability map to file, if you want
            outputNPYlocation = os.path.join(
                data_location_base, outputFoldername, region_name)
            syn.saveresultvol(resultvol, outputNPYlocation, 'query_', n)

            queryresult = compute_measurements(
                resultvol, query, volume_um3, thresh)
            result_list.append(queryresult)

    df = create_synapse_df(result_list, foldernames)
    print(df)
    return df
