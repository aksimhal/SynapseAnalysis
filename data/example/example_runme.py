"""
Example runme for synapse detection.  Requires installation of at_synapse_detection
"""

from skimage import measure
from at_synapse_detection import dataAccess as da
from at_synapse_detection import SynapseDetection as syn


def main():
    
    # Example use case of the synapse detection pipeline
    # Location of Queries
    queryFN = 'data/example/example_queries.json'

    # List of Queries
    listOfQueries = syn.loadQueriesJSON(queryFN)

    # Test the first query
    query = listOfQueries[0]

    # Load the data 
    synapticVolumes = da.loadChannelVolFromQuery(query)

    # Run Synapse Detection
    # Takes ~5 minutes to run
    resultVol = syn.getSynapseDetections(synapticVolumes, query)

    # Verify Output  
    labelVol = measure.label(resultVol > 0.9)
    stats = measure.regionprops(labelVol)
    print(len(stats)) #output should be 5440


if __name__ == '__main__':
    main()