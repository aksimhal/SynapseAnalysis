# evaluate site3 synapse detections 
import os 
import json
import numpy as np
from skimage import measure
from at_synapse_detection import dataAccess as da
from at_synapse_detection import SynapseDetection as syn
from at_synapse_detection import processDetections as pd
from at_synapse_detection import evaluate_synapse_detection as esd




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

        mod = esd.EvaluateSynapseDetection(evalparam)
        evalresults = mod.run()
        listofevals.append(evalresults)

    pd.printEvalToText(listofevals, listOfQueries, listOfThresholds)

    # Combine Queries  
    evaluation_parameters = metadata['evalparam']
    pd.combineResultVolumes(list(range(0,len(listOfQueries))), listOfThresholds, metadata, evaluation_parameters)

    


if __name__ == '__main__':
    main()

