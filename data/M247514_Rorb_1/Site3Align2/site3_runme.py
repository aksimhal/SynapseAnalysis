"""
run site3 synapse detections
uses metadata generated from populate_metadata.ipynb
"""

from at_synapse_detection import dataAccess as da
from at_synapse_detection import SynapseDetection as syn
from at_synapse_detection import processDetections as pd

def main():
    """
    run site 3 synapse detection
    """
    # Load metadata
    metadata_fn = 'site3_metadata.json'
    metadata = syn.loadMetadata(metadata_fn)

    # This is where the image data is located on disk
    datalocation = metadata['datalocation']
    query_fn = metadata['querylocation']

    # List of Queries
    listOfQueries = syn.loadQueriesJSON(query_fn)
    print("Number of Queries: ", len(listOfQueries))

    for n in range(0, len(listOfQueries)):

        query = listOfQueries[n]
        print(query)

        # Load the data
        synapticVolumes = da.loadTiffSeriesFromQuery(query, datalocation)

        # Run Synapse Detection
        # Takes ~5 minutes to run
        resultVol = syn.getSynapseDetections(synapticVolumes, query)

        # Save the probability map to file
        syn.saveresultvol(resultVol, datalocation, n)

        # Save the thresholded results as annotation objects
        # in a json file
        pd.probMapToJSON(resultVol, metadata, query, n)


if __name__ == '__main__':
    main()

