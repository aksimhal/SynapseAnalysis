"""
Example runme for synapse detection.  Requires installation of at_synapse_detection
"""

from skimage import measure
from at_synapse_detection import dataAccess as da
from at_synapse_detection import SynapseDetection as syn


def main():

    # Example use case of the synapse detection pipeline
    # Location of Queries
    queryFN = 'example_queries.json'

    # List of Queries
    list_of_queries = syn.loadQueriesJSON(queryFN)

    # Test the first query
    query = list_of_queries[0]

    # Load the data
    synaptic_volumes = da.load_tiff_from_query(query)

    # Run Synapse Detection
    # Takes ~5 minutes to run
    result_vol = syn.getSynapseDetections(synaptic_volumes, query)

    # Verify Output
    label_vol = measure.label(result_vol > 0.9)
    stats = measure.regionprops(label_vol)
    print(len(stats))  # output should be 5440


if __name__ == '__main__':
    main()
