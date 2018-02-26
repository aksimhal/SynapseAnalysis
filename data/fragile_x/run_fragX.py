"""
run fragilex synapse detections
"""
import os
import pandas as pd
from at_synapse_detection import dataAccess as da
from at_synapse_detection import SynapseDetection as syn
from at_synapse_detection import antibodyAnalysis as aa 
from at_synapse_detection import SynapseAnalysis as sa
import socket

def run_synapses(query_fn, data_location_base): 

    listOfQueries = syn.loadQueriesJSON(query_fn)
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    region_name_base = 'F00'
    thresh = 0.9

    foldernames = []
    result_list = []
    for region_num in range(0, 4): 
        region_name = region_name_base + str(region_num)
        data_location = os.path.join(data_location_base, region_name)

        for n, query in enumerate(listOfQueries):
            print(query)
            foldernames.append(region_name + '-Q' + str(n))
            # Load the data
            
            synaptic_volumes = da.load_tiff_from_query(query, data_location)
            volume_um3 = aa.getdatavolume(synaptic_volumes, resolution)

            # Run Synapse Detection
            resultvol = syn.getSynapseDetections(synaptic_volumes, query)
            queryresult = sa.compute_measurements(resultvol, query, volume_um3, thresh)
            result_list.append(queryresult)

    df = sa.create_synapse_df(result_list, foldernames)

    return df

def main():
    """
    run synapse detection
    """
    
    query_fn = '2ss_queries.json'
    datalocation = '/Users/anish/Documents/yi_mice/2ss_stacks/'
    hostname = socket.gethostname()
    if hostname == 'Galicia': 
        datalocation = '/data5TB/yi_mice/2ss_stacks'

    mouse2_df = run_synapses(query_fn, datalocation)

    query_fn = '3ss_queries.json'
    datalocation = '/Users/anish/Documents/yi_mice/3ss_stacks/'
    if hostname == 'Galicia': 
        datalocation = '/data5TB/yi_mice/3ss_stacks'

    mouse3_df = run_synapses(query_fn, datalocation)
    
    sheet_name = 'FragileX Mouse'
    fn = 'fragileX_experiment.xlsx'
    df_list = [mouse2_df, mouse3_df]
    aa.write_dfs_to_excel(df_list, sheet_name, fn)



if __name__ == '__main__':
    main()
