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
import multiprocessing as mp
import copy
import numpy as np


def run_synapse_detection(atet_input):
    """
    Run synapse detection and result evalution.  The parameters need to be rethought 

    Parameters
    -------------------
    atet_input : dict 

    Returns
    -------------------
    output_dict : dict 

    """

    query = atet_input['query']
    queryID = atet_input['queryID']
    nQuery = atet_input['nQuery']
    resolution = atet_input['resolution']
    data_location = atet_input['data_location']
    data_region_location = atet_input['data_region_location']
    output_foldername = atet_input['output_foldername']
    region_name = atet_input['region_name']

    # Load the data
    synaptic_volumes = da.load_tiff_from_query(query, data_region_location)
    volume_um3 = aa.getdatavolume(synaptic_volumes, resolution)
    print(volume_um3)

    # Run Synapse Detection
    print('running synapse detection')
    resultvol = syn.getSynapseDetections(synaptic_volumes, query)

    # Save the probability map to file, if you want
    outputNPYlocation = os.path.join(
        data_location, output_foldername, region_name)
    syn.saveresultvol(resultvol, outputNPYlocation, 'query_', queryID)

    thresh = 0.9
    queryresult = sa.compute_measurements(
        resultvol, query, volume_um3, thresh)

    output_dict = {'queryID': queryID,
                   'query': query, 'queryresult': queryresult}
    return output_dict


def organize_result_lists(result_list):
    """
    output_dict = {'queryID': queryID,
                   'query': query, 'queryresult': queryresult}
    """
    query_inds = []
    list_of_queryresult = []
    for result in result_list:
        query_inds.append(result['queryID'])
        list_of_queryresult.append(result['queryresult'])

    sorted_inds = np.argsort(query_inds)
    sorted_queryresult = [list_of_queryresult[n] for n in sorted_inds]

    return sorted_queryresult


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
    query_fn = mouse_project_str + '_queries.json'
    data_location = '/Users/anish/Documents/yi_mice/' + \
        str(mouse_number) + 'ss_stacks/'

    hostname = socket.gethostname()
    if hostname == 'Galicia':
        data_location = '/data5TB/yi_mice/' + str(mouse_number) + 'ss_stacks'

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

    queryID = 0
    foldernames = []
    for region_num in range(0, 4):
        region_name = region_name_base + str(region_num)
        data_region_location = os.path.join(data_location, region_name)

        for nQuery, query in enumerate(listOfQueries):
            foldername = region_name + '-Q' + str(nQuery)
            foldernames.append(foldername)
            print(foldername)

            atet_input = {'query': query, 'queryID': queryID, 'nQuery': nQuery, 'resolution': resolution,
                          'data_region_location': data_region_location, 'data_location': data_location,
                          'output_foldername': output_foldername, 'region_name': region_name}
            atet_inputs_list.append(atet_input)

            queryID = queryID + 1

    # Run processes
    result_list = pool.map(run_synapse_detection, atet_inputs_list)

    pool.close()
    pool.join()

    print('Get process results from the output queue')
    sorted_queryresult = organize_result_lists(result_list)

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
        run_list_of_queries(
            mouse_number=5, mouse_project_str='5ss', sheet_name='5ss_fragX')
        run_list_of_queries(
            mouse_number=7, mouse_project_str='7ss', sheet_name='7ss_fragX')

        run_list_of_queries(
            mouse_number=5, mouse_project_str='5ss_YFP', sheet_name='5ss_YFP_fragX')
        run_list_of_queries(
            mouse_number=7, mouse_project_str='7ss_YFP', sheet_name='7ss_YFP_fragX')

        run_list_of_queries(
            mouse_number=2, mouse_project_str='2ss', sheet_name='2ss_fragX')
        run_list_of_queries(
            mouse_number=3, mouse_project_str='3ss', sheet_name='3ss_fragX')
        run_list_of_queries(
            mouse_number=4, mouse_project_str='4ss', sheet_name='4ss_fragX')
        run_list_of_queries(
            mouse_number=6, mouse_project_str='6ss', sheet_name='6ss_fragX')

        # python run_fragX.py 4 '4ss_YFP' '4ss_YFP_fragX'
        run_list_of_queries(
            mouse_number=2, mouse_project_str='2ss_YFP', sheet_name='2ss_YFP_fragX')
        run_list_of_queries(
            mouse_number=3, mouse_project_str='3ss_YFP', sheet_name='3ss_YFP_fragX')
        run_list_of_queries(
            mouse_number=4, mouse_project_str='4ss_YFP', sheet_name='4ss_YFP_fragX')
        run_list_of_queries(
            mouse_number=6, mouse_project_str='6ss_YFP', sheet_name='6ss_YFP_fragX')

    else:
        print('we have arguments')
        print(sys.argv)
        mouse_number = sys.argv[1]
        mouse_project_str = sys.argv[2]
        sheet_name = sys.argv[3]
        run_list_of_queries(mouse_number, mouse_project_str, sheet_name)


if __name__ == '__main__':
    main()
