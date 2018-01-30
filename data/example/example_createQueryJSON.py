"""
Create the JSON Query file needed to run the probabilistic synapse detector

Format:
Query (dict)
    - preIF (list of strs) : str corresponds to either the data file name or foldername containing the data
    - postIF (list of strs)
    - preIF_z (list of ints) : int corresponds to the number of slices a blob should span. Current values can be 1, 2, or 3. 
    - postIF_z (list of ints)
    - punctumSize (int) : 2D blob size, unit is pixels
    - thersh (float) : (optional) threshold associated with the query 
"""

import os
import sys
import json 
from at_synapse_detection import dataAccess as da
from at_synapse_detection import SynapseDetection as syn

def main():
    # The 2D Blob size xy, units: pixels
    punctumSize = 2; 
    # Threshold associated with query (optional)
    thresh = 0.7

    listOfQueries = []

    ## QUERY 1 
    preIF = ['synapsin_1st.tif'] #corresponds to the file name
    preIF_z = [2]
    postIF = ['PSD95m_1st.tif']
    postIF_z = [2]

    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF, 
            'postIF_z': postIF_z, 'punctumSize': punctumSize, 'thresh': thresh}
    listOfQueries.append(query)
    data = {'listOfQueries': listOfQueries}
    fn = 'example_queries.json'
    da.writeJSONFile(fn, data)
    
    # Load Query File 
    querylist = syn.loadQueriesJSON(fn)
    print(len(querylist))



if __name__ == '__main__':
    main()