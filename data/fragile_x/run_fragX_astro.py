"""
Run FragileX data synapse detections
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


def run_list_of_queries(mouse_number, mouse_project_str, sheet_name):
    """
    run queries in a parallel manner

    Parameters
    -----------------
    mouse_number : int 
    mouse_project_str : str
    sheet_name : str 

    """

    output_foldername = 'results_' + sheet_name
    query_fn = 'queries/' + mouse_project_str + '_queries.json'
    data_location = '/Users/anish/Documents/yi_mice/' + \
        str(mouse_number) + 'ss_stacks/'

    hostname = socket.gethostname()
    if hostname == 'Galicia':
        data_location = '/data5TB/yi_mice/' + str(mouse_number) + 'ss_stacks'
        dapi_mask_str_base = '/data5TB/yi_mice/dapi-masks/' + \
            str(mouse_number) + 'ss_stacks'

    print('Query Filename: ', query_fn)
    print('Data Location: ', data_location)
    print('OutputFoldername: ', output_foldername)
    print('Sheetname: ', sheet_name)

    listOfQueries = syn.loadQueriesJSON(query_fn)
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    region_name_base = 'F00'
    thresh = 0.9

    result_list = []
    num_workers = mp.cpu_count() - 1

    print(num_workers)
    pool = mp.Pool(num_workers)

    atet_inputs_list = []
    mask_location_str = -1
    queryID = 0
    foldernames = []
    for region_num in range(0, 4):
        region_name = region_name_base + str(region_num)
        data_region_location = os.path.join(data_location, region_name)
        dapi_mask_str = os.path.join(dapi_mask_str_base, region_name)

        for nQuery, query in enumerate(listOfQueries):
            foldername = region_name + '-Q' + str(nQuery)
            foldernames.append(foldername)
            print(foldername)

            mask_location_str = -1
            #dapi_mask_str = -1

            atet_input = {'query': query, 'queryID': queryID, 'nQuery': nQuery, 'resolution': resolution,
                          'data_region_location': data_region_location, 'data_location': data_location,
                          'output_foldername': output_foldername, 'region_name': region_name,
                          'mask_str': mask_location_str, 'dapi_mask_str': dapi_mask_str, 'mouse_number': mouse_number}
            atet_inputs_list.append(atet_input)

            queryID = queryID + 1

    # Run processes
    result_list = pool.map(sa.run_synapse_detection_astro, atet_inputs_list)

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

    if len(sys.argv) < 4:
        print('Run All Combinations')
        print(sys.argv)
        # mouse_number = 2
        # mouse_project_str = '2ss'
        # sheet_name = '2ss_fragX'
        # python run_fragX.py 4 '4ss_inhibitory' '4ss_inhibitory_fragX'

        # run_list_of_queries(
        #     mouse_number=1, mouse_project_str='1ss_inhibitory_astro', sheet_name='1ss_inhibitory_astro')
        # run_list_of_queries(
        #     mouse_number=22, mouse_project_str='22ss_inhibitory_astro', sheet_name='22ss_inhibitory_astro')
        # run_list_of_queries(
        #     mouse_number=2, mouse_project_str='2ss_inhibitory_astro', sheet_name='2ss_inhibitory_astro')
        # run_list_of_queries(
        #     mouse_number=3, mouse_project_str='3ss_inhibitory_astro', sheet_name='3ss_inhibitory_astro')
        # run_list_of_queries(
        #     mouse_number=4, mouse_project_str='4ss_inhibitory_astro', sheet_name='4ss_inhibitory_astro')
        # run_list_of_queries(
        #     mouse_number=6, mouse_project_str='6ss_inhibitory_astro', sheet_name='6ss_inhibitory_astro')
        # run_list_of_queries(
        #     mouse_number=5, mouse_project_str='5ss_inhibitory_astro', sheet_name='5ss_inhibitory_astro')
        # run_list_of_queries(
        #     mouse_number=7, mouse_project_str='7ss_inhibitory_astro', sheet_name='7ss_inhibitory_astro')

        run_list_of_queries(
            mouse_number=1, mouse_project_str='1ss_excitatory_astro1slice', sheet_name='1ss_fragX_excitatory_astro1slice')
        run_list_of_queries(
            mouse_number=22, mouse_project_str='22ss_excitatory_astro1slice', sheet_name='22ss_fragX_excitatory_astro1slice')
        run_list_of_queries(
            mouse_number=2, mouse_project_str='2ss_excitatory_astro1slice', sheet_name='2ss_fragX_excitatory_astro1slice')
        run_list_of_queries(
            mouse_number=3, mouse_project_str='3ss_excitatory_astro1slice', sheet_name='3ss_fragX_excitatory_astro1slice')
        run_list_of_queries(
            mouse_number=4, mouse_project_str='4ss_excitatory_astro1slice', sheet_name='4ss_fragX_excitatory_astro1slice')
        run_list_of_queries(
            mouse_number=6, mouse_project_str='6ss_excitatory_astro1slice', sheet_name='6ss_fragX_excitatory_astro1slice')
        run_list_of_queries(
            mouse_number=5, mouse_project_str='5ss_excitatory_astro1slice', sheet_name='5ss_fragX_excitatory_astro1slice')
        run_list_of_queries(
            mouse_number=7, mouse_project_str='7ss_excitatory_astro1slice', sheet_name='7ss_fragX_excitatory_astro1slice')

    else:
        print('we have arguments')
        print(sys.argv)
        mouse_number = sys.argv[1]
        mouse_project_str = sys.argv[2]
        sheet_name = sys.argv[3]
        run_list_of_queries(mouse_number, mouse_project_str, sheet_name)


if __name__ == '__main__':
    main()
