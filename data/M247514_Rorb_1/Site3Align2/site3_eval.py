# evaluate site3 synapse detections 
import os 
import json
import numpy as np
from skimage import measure
from at_synapse_detection import dataAccess as da
from at_synapse_detection import SynapseDetection as syn
from at_synapse_detection import processDetections as pd
from at_synapse_detection import evaluate_synapse_detection as esd


def printEvalToText(listofevals, listOfQueries, thresh): 
    """
    Outputs the evaluation results for each query to a text file 

    Parameters
    --------------
    listofevals : list of dictionaries 
    listOfQueries: list of dictionaries 
    thresh: threshold at which detections are computed
    """
    file = open('output.txt', 'w')
    
    file.write('Threshold: ' + str(thresh))
    file.write('\n\n')
    
    for n, evalresult in enumerate(listofevals): 
        query = listOfQueries[n]
        file.write(json.dumps(query))
        file.write('\n')

        file.write('EM_per_LM: ' + str(evalresult['EM_per_LM']) + '\n')
        file.write('LM_per_EM: ' + str(evalresult['LM_per_EM']) + '\n')
        
        file.write('lm_edge_detections: ' + str(evalresult['lm_edge_detections']) + '\n')
        file.write('em_edge_annotations: ' + str(evalresult['em_edge_annotations']) + '\n')
        file.write('LM_detections: ' + str(evalresult['LM_detections']) + '\n')
        file.write('EM_detections: ' + str(evalresult['EM_detections']) + '\n')
        file.write('\n')


    file.close()




def main():
    # Example use case of the synapse detection pipeline
    # Load metadata
    metadataFN = 'site3_metadata.json'
    metadata = syn.loadMetadata(metadataFN)
    outputJSONlocation = metadata['outputJSONlocation']; 
    queryFN = metadata['querylocation']
    evalparam = metadata['evalparam']

    # List of Queries
    listOfQueries = syn.loadQueriesJSON(queryFN)
    listOfThresholds = [] 
    listofevals = []

    # Evaluate each query individually
    for n, query in enumerate(listOfQueries): 
        print(query)
        listOfThresholds.append(query['thresh'])
        jsonfile = os.path.join(outputJSONlocation, 'resultVol'); 
        jsonfile = jsonfile + str(n) + '.json'
        
        # Location of LM detection output
        evalparam['LM_annotation_json'] = jsonfile

        # mod = esd.EvaluateSynapseDetection(evalparam)
        # evalresults = mod.run()
        # listofevals.append(evalresults)

        # printEvalToText(listofevals, listOfQueries, metadata['thresh'])

    # Combine Queries  
    evaluation_parameters = metadata['evalparam']
    pd.combineResultVolumes(list(range(0,len(listOfQueries))), listOfThresholds, metadata, evaluation_parameters)

    


if __name__ == '__main__':
    main()

