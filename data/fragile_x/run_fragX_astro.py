"""
Run FragileX Astrocyte Queries
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
import numpy as np


def run_queries():
    """
    Run FragileX astrocyte queries
    """
    # Select data
    mouse_id_list = [1, 22, 2, 3, 4, 5, 6, 7]
    mouse_region_list = ['F000', 'F001', 'F002', 'F003']
    # Specify output
    output_foldername = 'results_astro'
    sheet_name = 'results_astro'
    # Set global
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9
    # Set multiprocessing pool
    num_workers = mp.cpu_count() - 1
    pool = mp.Pool(num_workers)

    atet_inputs_list = []
    result_list = []
    foldernames = []
    queryID = 0

    # Collect data for mp pool
    for n, mouse_number in enumerate(mouse_id_list):
        # Load specific query file
        query_fn = 'queries/' + str(mouse_number) + 'ss_astro_queries.json'
        listOfQueries = syn.loadQueriesJSON(query_fn)

        hostname = socket.gethostname()
        if hostname == 'Galicia':
            data_location = '/data5TB/yi_mice/' + \
                str(mouse_number) + 'ss_stacks'
            dapi_mask_str_base = '/data5TB/yi_mice/dapi-masks/' + \
                str(mouse_number) + 'ss_stacks'

            mask_location_str = None
        elif hostname == 'anish':
            data_location = '/Users/anish/Documents/yi_mice/' + \
                str(mouse_number) + 'ss_stacks/'
            mask_location_str = None

        # Set up processes
        for region_name in mouse_region_list:
            data_region_location = os.path.join(data_location, region_name)

            dapi_mask_str = os.path.join(dapi_mask_str_base, region_name)

            # Iterate over queries
            for nQuery, query in enumerate(listOfQueries):
                foldername = str(mouse_number) + 'ss-' + \
                    region_name + '-Q' + str(nQuery)
                foldernames.append(foldername)
                print(foldername)

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


def run_queries_astroYFP():
    """
    Run FragileX astrocyte queries
    """
    # Select data
    mouse_id_list = [1, 2, 3, 4, 5, 6, 7, 22]
    mouse_region_list = ['F000', 'F001', 'F002', 'F003']
    # Specify output
    output_foldername = 'results_astroYFP'
    sheet_name = 'results_astroYFP'
    # Set global
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    thresh = 0.9
    # Set multiprocessing pool
    num_workers = mp.cpu_count() - 1
    pool = mp.Pool(num_workers)

    atet_inputs_list = []
    result_list = []
    foldernames = []
    queryID = 0

    # Collect data for mp pool
    for n, mouse_number in enumerate(mouse_id_list):
        # Load specific query file
        query_fn = 'queries/' + str(mouse_number) + 'ss_astroYFP_queries.json'
        listOfQueries = syn.loadQueriesJSON(query_fn)

        hostname = socket.gethostname()
        if hostname == 'Galicia':
            data_location = '/data5TB/yi_mice/' + \
                str(mouse_number) + 'ss_stacks'
            dapi_mask_str_base = '/data5TB/yi_mice/dapi-masks/' + \
                str(mouse_number) + 'ss_stacks'

            mask_location_str = None
        elif hostname == 'anish':
            data_location = '/Users/anish/Documents/yi_mice/' + \
                str(mouse_number) + 'ss_stacks/'
            mask_location_str = None

        # Set up processes
        for region_name in mouse_region_list:
            data_region_location = os.path.join(data_location, region_name)

            dapi_mask_str = os.path.join(dapi_mask_str_base, region_name)

            # Iterate over queries
            for nQuery, query in enumerate(listOfQueries):
                foldername = str(mouse_number) + 'ss-' + \
                    region_name + '-Q' + str(nQuery)
                foldernames.append(foldername)
                print(foldername)

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
    run_queries()
    run_queries_astroYFP()


if __name__ == '__main__':
    main()
