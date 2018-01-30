import numpy as np
from at_synapse_detection import processDetections as pd
from at_synapse_detection import SynapseDetection as syn 
import os 

def main():
    
    # Example use case of processing detections
    # Load probability map 
    metadataFN = '/Users/anish/Documents/Connectome/SynapseAnalysis/data/M247514_Rorb_1/Site3Align2/site3_metadata.json'
    metadata = syn.loadMetadata(metadataFN)
    
    queryFN = metadata['querylocation']

    # List of Queries
    listOfQueries = syn.loadQueriesJSON(queryFN)

    for n in range(0, len(listOfQueries)): 
        fn = os.path.join(metadata['datalocation'], 'resultVol')
        fn = fn + str(n) + '.npy'

        resultVol = np.load(fn)
        print(fn)

        pd.probMapToJSON(resultVol, metadata, listOfQueries[n], n)
    

if __name__ == '__main__':
    main()


