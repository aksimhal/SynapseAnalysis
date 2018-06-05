"""
Run FragileX Queries on Layer 4
"""
import os
import sys
import pandas as pd
from at_synapse_detection import dataAccess as da
from at_synapse_detection import SynapseDetection as syn
from at_synapse_detection import antibodyAnalysis as aa
from at_synapse_detection import SynapseAnalysis as sa
import socket
import multiprocessing as mp
import copy
import numpy as np


def run_queries_layer4():
    """
    Run queries on L4 of the data 
    F000 for 2ss, 3ss, 4ss, 5ss
    F003 for 6ss, 7ss
    """

    mouse_id_list = [2, 3, 4, 5, 6, 7]
    mouse_region_list = ['F000', 'F000', 'F000', 'F000', 'F003', 'F003']
    output_foldername = 'results_layer4'
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9
    sheet_name = 'results_layer4'

    for n, mouse_number in enumerate(mouse_id_list):

        query_fn = mouse_number + 'ss_queries.json'
        data_location = '/Users/anish/Documents/yi_mice/' + \
            str(mouse_number) + 'ss_stacks/'
        mask_location_str = '/Users/anish/Documents/yi_mice/masks/' + \
            str(mouse_number) + 'ss_mask.png'

        hostname = socket.gethostname()
        if hostname == 'Galicia':
            data_location = '/data5TB/yi_mice/' + \
                str(mouse_number) + 'ss_stacks'
            mask_location_str = '/data5TB/yi_mice/L4masks/' + \
                str(mouse_number) + 'ss_mask.png'

        listOfQueries = syn.loadQueriesJSON(query_fn)
        region_name = mouse_region_list[n]

        num_workers = mp.cpu_count() - 1
        print(num_workers)
        pool = mp.Pool(num_workers)

        atet_inputs_list = []
        result_list = []
        foldernames = []
        queryID = 0

        data_region_location = os.path.join(data_location, region_name)

        for nQuery, query in enumerate(listOfQueries):
            foldername = str(mouse_number) + 'ss-' + \
                region_name + '-Q' + str(nQuery)
            foldernames.append(foldername)
            print(foldername)

            atet_input = {'query': query, 'queryID': queryID, 'nQuery': nQuery, 'resolution': resolution,
                          'data_region_location': data_region_location, 'data_location': data_location,
                          'output_foldername': output_foldername, 'region_name': region_name}
            atet_inputs_list.append(atet_input)

            queryID = queryID + 1

    # Run processes
    result_list = pool.map(sa.run_synapse_detection, atet_inputs_list)

    pool.close()
    pool.join()

    print('Get process results from the output queue')
    sorted_queryresult = sa.organize_result_lists(result_list)

    mouse_df = sa.create_synapse_df(sorted_queryresult, foldernames)
    print(mouse_df)

    fn = sheet_name + '.xlsx'
    df_list = [mouse_df]
    aa.write_dfs_to_excel(df_list, sheet_name, fn)


def main():
    run_queries_layer4()


if __name__ == '__main__':
    main()
