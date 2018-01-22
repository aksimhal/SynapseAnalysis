from skimage import measure
from at_synapse_detection import dataAccess as da
from at_synapse_detection import SynapseDetection as syn


def main():
    
    # Example use case of the synapse detection pipeline
    # Location of Queries
    fileName = 'examplequeries.csv'

    # List of Queries
    listOfQueries = syn.loadQueriesCSV(fileName)

    # Test the first query
    query = listOfQueries[0]

    # Load the data 
    synapticVolumes = da.loadChannelVolFromQuery(query)

    # Run Synapse Detection
    # Takes ~5 minutes to run
    resultVol = syn.getSynapseDetections(synapticVolumes, query)

    # Verify Output Matches 
    labelVol = measure.label(resultVol > 0.9)
    stats = measure.regionprops(labelVol)
    print(len(stats)) #output should be 5402


if __name__ == '__main__':
    main()