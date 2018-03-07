"""
run fragilex synapse detections for YFP
"""
import os
import pandas as pd
from at_synapse_detection import dataAccess as da
from at_synapse_detection import SynapseDetection as syn
from at_synapse_detection import antibodyAnalysis as aa 
from at_synapse_detection import SynapseAnalysis as sa
import socket


def main():
    """
    run synapse detection
    """
    outputFoldername = 'results_YFP'
    query_fn = '2ss_YFP_queries.json'
    datalocation = '/Users/anish/Documents/yi_mice/2ss_stacks/'
    hostname = socket.gethostname()
    if hostname == 'Galicia': 
        datalocation = '/data5TB/yi_mice/2ss_stacks'

    mouse2_df = sa.run_synapses(query_fn, datalocation, outputFoldername)

    query_fn = '3ss_YFP_queries.json'
    datalocation = '/Users/anish/Documents/yi_mice/3ss_stacks/'
    if hostname == 'Galicia': 
        datalocation = '/data5TB/yi_mice/3ss_stacks'

    mouse3_df = sa.run_synapses(query_fn, datalocation, outputFoldername)
    
    sheet_name = 'FragileX YFP'
    fn = 'fragileX_YFP_experiment.xlsx'
    df_list = [mouse2_df, mouse3_df]
    aa.write_dfs_to_excel(df_list, sheet_name, fn)



if __name__ == '__main__':
    main()
