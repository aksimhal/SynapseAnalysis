"""
evaluate site3 synapse detections
"""

import os

from at_synapse_detection import SynapseDetection as syn
from at_synapse_detection import processDetections as pd
from at_synapse_detection import evaluate_synapse_detection as esd


def main():
    """
    Evaluation of site3 synapse detection results
    """

    # Load metadata
    metadataFN = 'site3_metadata.json'
    metadata = syn.loadMetadata(metadataFN)
    outputJSONlocation = metadata['outputJSONlocation']

    metadata['outputNPYlocation'] = '/Users/anish/Documents/Connectome/SynapseAnalysis/data/M247514_Rorb_1/Site3Align2/results/results_npy_norm/'
    queryFN = metadata['querylocation']
    evalparam = metadata['evalparam']

    # List of Queries
    listOfQueries = syn.loadQueriesJSON(queryFN)
    listOfThresholds = []
    listOfThresholds_to_text = []
    listOfQueries_to_text = []
    listofevals = []
    thresh_list = [0.7, 0.8, 0.9]
    # Evaluate each query individually
    for n, query in enumerate(listOfQueries):
        listOfThresholds.append(query['thresh'])
        print(query)

        for thresh in thresh_list:
            listOfThresholds_to_text.append(thresh)
            listOfQueries_to_text.append(query)
            queryresult = pd.combineResultVolumes(
                [n], [thresh], metadata, evalparam)
            listofevals.append(queryresult)

    pd.printEvalToText(listofevals, listOfQueries_to_text,
                       listOfThresholds_to_text)

    # Combine Queries
    evaluation_parameters = metadata['evalparam']
    metadata['datalocation'] = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/collman17/Site3Align2Stacks/originalresult'
    pd.combineResultVolumes(list(range(0, len(listOfQueries))),
                            listOfThresholds, metadata, evaluation_parameters)


if __name__ == '__main__':
    main()
