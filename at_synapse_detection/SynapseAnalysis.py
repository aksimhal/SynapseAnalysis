"""Synapse Analysis"""
import os
import numpy as np
import pandas as pd
from skimage import measure
from at_synapse_detection import SynapseDetection as syn
from at_synapse_detection import dataAccess as da

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
    queryresult.synapse_count = len(stats)

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
        df.iloc[n, 1] = queryresult.synapse_count


    return df



