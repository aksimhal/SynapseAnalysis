"""
Site3 Synaptograms
"""
import os
from at_synapse_detection import synaptogram
from at_synapse_detection import SynapseDetection as syn
from at_synapse_detection import processDetections as pd


def main():
    """
    Site3 Synaptograms
    """

    metadata_fn = 'site3_metadata.json'
    metadata = syn.loadMetadata(metadata_fn)
    query_fn = metadata['querylocation']
    listOfQueries = syn.loadQueriesJSON(query_fn)
    evalargs = metadata['evalparam']

    listOfThresholds = []
    for query in listOfQueries:
        listOfThresholds.append(query['thresh'])

    listOfQueryNumbers = list(range(0, len(listOfQueries)))
    listOfThresholds = [0.8, 0.7, 0.7] 
    listOfQueryNumbers = [0, 2, 4]
    print(listOfQueries[2])
    queryresult = pd.combineResultVolumes(
        listOfQueryNumbers, listOfThresholds, metadata, evalargs)

    data_location = metadata['datalocation']
    outputpath = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/collman17/Site3Align2Stacks/synaptograms/'
    stack_list = ['labels', 'PSD95', 'synapsin',
                  'VGlut1', 'GluN1', 'GABA', 'Gephyrin', 'TdTomato']
    text_x_offset = 0
    text_y_offset = 5
    win_xy = 4
    win_z = 1

    synaptogram_args = {'win_xy': win_xy, 'win_z': win_z, 'data_location': data_location,
                        'stack_list': stack_list, 'text_x_offset': text_x_offset,
                        'text_y_offset': text_y_offset, 'outputpath': outputpath}


    # Detected synapses (True Positives)
    detected_annotations = queryresult['detected_annotations']
    synaptogram_args['outputpath'] = os.path.join(outputpath, 'true_positive_detections')
    for counter, synapse in enumerate(detected_annotations):
        synaptogram.synapseAnnoToSynaptogram(synapse, synaptogram_args)

    # False negatives
    missed_annotations = queryresult['missed_annotations']
    synaptogram_args['outputpath'] = os.path.join(outputpath, 'false_negative')
    for counter, synapse in enumerate(missed_annotations):
        synaptogram.synapseAnnoToSynaptogram(synapse, synaptogram_args)

    # False positive detections
    false_positives = queryresult['false_positives']
    synaptogram_args['outputpath'] = os.path.join(outputpath, 'false_positive')
    for synapse in false_positives:
        synaptogram.synapseAnnoToSynaptogram(synapse, synaptogram_args)


if __name__ == '__main__':
    main()
