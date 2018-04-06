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
    metadata_fn = '/Users/anish/Documents/Connectome/SynapseAnalysis/data/M247514_Rorb_1/Site3Align2/site3_metadata.json'
    #metadata_fn = 'site3_metadata_TdTomato.json'
    metadata = syn.loadMetadata(metadata_fn)

    datalocation = metadata['datalocation']
    outputNPYlocation = metadata['outputNPYlocation']
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

        # Save the probability map to file, if you want
        syn.saveresultvol(resultVol, outputNPYlocation, 'resultVol', n)

        # Save the thresholded results as annotation objects
        # in a json file
        # pd.probMapToJSON(resultVol, metadata, query, n)




    """
    Evaluation of site3 synapse detection results
    """

    # Load metadata
    metadataFN = 'site3_metadata.json'
    metadata = syn.loadMetadata(metadataFN)
    outputJSONlocation = metadata['outputJSONlocation']

    queryFN = metadata['querylocation']
    evalparam = metadata['evalparam']

    # List of Queries
    listOfQueries = syn.loadQueriesJSON(queryFN)
    listOfThresholds = []
    listOfThresholds_to_text = []
    listOfQueries_to_text = []
    listofevals = []
    thresh_list = [0.7, 0.8, 0.9]
    # Evaluate each query individually
    for n, query in enumerate(listOfQueries):
        listOfThresholds.append(query['thresh'])
        
        for thresh in thresh_list:
            listOfThresholds_to_text.append(thresh)
            query['thresh'] = thresh
            print(query)
            listOfQueries_to_text.append(query)
            queryresult = pd.combineResultVolumes(
                [n], [thresh], metadata, evalparam)
            listofevals.append(queryresult)

    pd.printEvalToText(listofevals, listOfQueries_to_text,
                       listOfThresholds_to_text)

    # Combine Queries
    evaluation_parameters = metadata['evalparam']

    pd.combineResultVolumes(list(range(0, len(listOfQueries))),
                            listOfThresholds, metadata, evaluation_parameters)



if __name__ == '__main__':
    main()
