"""
Site3 Synaptograms
"""
from at_synapse_detection import synaptogram
from at_synapse_detection import SynapseDetection as syn
from at_synapse_detection import processDetections as pd


def main():
    """
    Site3 Synaptograms
    """

    metadata_fn = '../data/M247514_Rorb_1/Site3Align2/site3_metadata.json'
    metadata = syn.loadMetadata(metadata_fn)

    args = {
        "EM_annotation_json":"../data/M247514_Rorb_1/Site3Align2/json_annotations/m247514_Site3Annotation_MN_global_v2.json",
        "LM_annotation_json":"../data/M247514_Rorb_1/Site3Align2/results/resultVol9.json",
        "EM_metadata_csv":"../data/M247514_Rorb_1/Site3Align2/MNSite3Synaptograms_v2.csv",
        "LM_metadata_file":"../data/M247514_Rorb_1/Site3Align2/site3_metadata.json",
        "EM_inclass_column":"glutsynapse",
        "EM_not_synapse_column":"ConsensusNotSynapse",
        "output_json":"../data/M247514_Rorb_1/Site3Align2/results/Anish_evaluation_output.json",
        "annotationToRemove": "../data/M247514_Rorb_1/Site3Align2/missedanno.json"
        }

    listOfQueryNumbers = [  0]
    listOfThresholds   = [0.8]
    metadata['datalocation']  = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/collman17/Site3Align2Stacks/mwresult/'
    queryresult = pd.combineResultVolumes(listOfQueryNumbers, listOfThresholds, metadata, args)

    data_location = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/collman17/Site3Align2Stacks/';
    outputpath = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/collman17/Site3Align2Stacks/good'
    stack_list = ['PSD95', 'synapsin', 'VGlut1', 'GluN1', 'GABA', 'Gephyrin', 'TdTomato']
    text_x_offset = 0
    text_y_offset = 5
    win_xy = 4
    win_z = 1

    synaptogram_args = {'win_xy': win_xy, 'win_z': win_z, 'data_location': data_location,
                        'stack_list': stack_list, 'text_x_offset': text_x_offset,
                        'text_y_offset': text_y_offset, 'outputpath': outputpath}

    EM_edge = queryresult['EM_edge']
    good_annotations = queryresult['good_annotations']
    false_positives = queryresult['false_positives']
    missed_annotations = queryresult['missed_annotations']

    # Detected synapses (True Positives)
    for counter, synapse in enumerate(good_annotations):
        if EM_edge[counter] == False:
            synaptogram.synapseAnnoToSynaptogram(synapse, synaptogram_args)

    # Missed synapse annotations         
    synaptogram_args['outputpath'] = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/collman17/Site3Align2Stacks/missed'
    for counter, synapse in enumerate(missed_annotations): 
        if EM_edge[counter] == False:
            synaptogram.synapseAnnoToSynaptogram(synapse, synaptogram_args)

    # False positive detections 
    synaptogram_args['outputpath'] = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/collman17/Site3Align2Stacks/false_positives'
    for counter, synapse in enumerate(false_positives): 
        synaptogram.synapseAnnoToSynaptogram(synapse, synaptogram_args)


if __name__ == '__main__':
    main()