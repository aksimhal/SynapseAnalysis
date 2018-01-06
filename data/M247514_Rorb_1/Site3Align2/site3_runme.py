# run site3 synapse detections 
import numpy as np
from skimage import measure
from at_synapse_detection import dataAccess as da
from at_synapse_detection import SynapseDetection as syn
from at_synapse_detection import processDetections as pd

def main():
    
    # Example use case of the synapse detection pipeline
    # Load metadata
    metadataFN = 'site3_metadata.json'
    metadata = syn.loadMetadata(metadataFN)
    
    datalocation = metadata['datalocation']
    queryFN = metadata['querylocation']

    # List of Queries
    listOfQueries = syn.loadQueriesJSON(queryFN)

    for n in range(0, len(listOfQueries)): 
        
        query = listOfQueries[n]
        print(query)
        
        # Load the data 
        synapticVolumes = da.loadTiffSeriesFromQuery(query, datalocation)

        # Run Synapse Detection
        # Takes ~5 minutes to run
        resultVol = syn.getSynapseDetections(synapticVolumes, query)

        # Save the probability map 
        syn.saveresultvol(resultVol, datalocation, n)

        # Save the thresholded results as annotation objects
        # in a json file
        pd.probMapToJSON(resultVol, metadata, query, n)


if __name__ == '__main__':
    main()

