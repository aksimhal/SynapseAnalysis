"""
run fragilex synapse detections
"""
import os
import sys
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

    if len(sys.argv) < 4:
        print('Not enough arguements')
        print(sys.argv)
        return
    else:
        print('we have arguments')
        print(sys.argv)


    mouse_number = sys.argv[1]
    mouse_project_str = sys.argv[2]
    sheet_name = sys.argv[3]

    outputFoldername = 'results'
    query_fn = mouse_project_str + '_queries.json'
    datalocation = '/Users/anish/Documents/yi_mice/' + str(mouse_number) + 'ss_stacks/'
    hostname = socket.gethostname()
    if hostname == 'Galicia':
        datalocation = '/data5TB/yi_mice/' + str(mouse_number) + 'ss_stacks'
    print('Query Filename: ', query_fn)
    print('Data Location: ', datalocation)
    print('OutputFoldername: ', outputFoldername)
    print('Sheetname: ', sheet_name)
    mouse_df = sa.run_synapses(query_fn, datalocation, outputFoldername)

    #sheet_name = 'FragileX Mouse'
    fn = sheet_name + '.xlsx'
    df_list = [mouse_df]
    aa.write_dfs_to_excel(df_list, sheet_name, fn)



if __name__ == '__main__':
    main()
