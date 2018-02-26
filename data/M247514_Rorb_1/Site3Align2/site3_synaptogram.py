"""
Site3 Synaptograms
"""
import os
import numpy as np
import scipy
from at_synapse_detection import synaptogram
from at_synapse_detection import SynapseDetection as syn
from at_synapse_detection import processDetections as pd

def generateResultTiffStacks(listOfQueryNumbers, listOfThresholds, data_location, outputNPYlocation): 
    """
    """
    resultVolList = []  # list of thresholded result volumes
    for n, queryNum in enumerate(listOfQueryNumbers):
        # load result volume
        fn = os.path.join(outputNPYlocation, 'resultVol')
        fn = fn + str(queryNum) + '.npy'
        resultVol_n = np.load(fn)
        resultVol_n = resultVol_n > listOfThresholds[n]
        resultVolList.append(resultVol_n)

    resultVol = resultVolList[0]
    for volItr in range(1, len(resultVolList)):
        resultVol = resultVol + resultVolList[volItr]

    folderpath = os.path.join(data_location, 'results')
    if not os.path.isdir(folderpath):
        os.makedirs(folderpath)


    for z in range(0, resultVol.shape[2]): 
        fn = os.path.join(folderpath, str(z).zfill(5))
        fn = fn + '.tiff'
        scipy.misc.imsave(fn, resultVol[:, :, z])





def main():
    """
    Site3 Synaptograms
    """

    metadata_fn = '/Users/anish/Documents/Connectome/SynapseAnalysis/data/M247514_Rorb_1/Site3Align2/site3_metadata_dev.json'
    metadata = syn.loadMetadata(metadata_fn)
    query_fn = metadata['querylocation']
    listOfQueries = syn.loadQueriesJSON(query_fn)
    evalargs = metadata['evalparam']

    # listOfThresholds = []
    # for query in listOfQueries:
    #     listOfThresholds.append(query['thresh'])

    # listOfQueryNumbers = list(range(0, len(listOfQueries)))
    listOfThresholds = [0.8, 0.7, 0.7] 
    listOfQueryNumbers = [0, 2, 4]

    queryresult = pd.combineResultVolumes(
        listOfQueryNumbers, listOfThresholds, metadata, evalargs)

    data_location = metadata['datalocation']
    outputpath = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/collman17/Site3Align2Stacks/synaptograms/'
    stack_list = ['results', 'PSD95', 'synapsin', 'VGlut1', 'GluN1', 'GABA', 'Gephyrin', 'TdTomato']
    text_x_offset = 0
    text_y_offset = 5
    win_xy = 4
    win_z = 1

    generateResultTiffStacks(listOfQueryNumbers, listOfThresholds, data_location, metadata['outputNPYlocation'])

    synaptogram_args = {'win_xy': win_xy, 'win_z': win_z, 'data_location': data_location,
                        'stack_list': stack_list, 'text_x_offset': text_x_offset,
                        'text_y_offset': text_y_offset, 'outputpath': outputpath}


    # Detected synapses (True Positives)
    # detected_annotations = queryresult['detected_annotations']
    # synaptogram_args['outputpath'] = os.path.join(outputpath, 'true_positive_detections')
    # for counter, synapse in enumerate(detected_annotations):
    #     synaptogram.synapseAnnoToSynaptogram(synapse, synaptogram_args)

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
