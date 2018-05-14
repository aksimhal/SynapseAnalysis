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


def run_synapse_detection(query, queryID, nQuery, resolution, data_location, data_location_base,
                          output_foldername, region_name):
    """
    Run synapse detection and result evalution.  The parameters need to be rethought 

    Parameters
    -------------------
    query : dict
    resolution : dict 
    data_location : str - raw IF data folder (ie F000, F001, F002, F003)
    data_location_base - folder for the mouse (ie 2ss, 3ss)
    output_foldername : str (ie result)
    region_name : str (ie F001)
    output : Queue object() 
    """

    print(query)

    # Load the data
    synaptic_volumes = da.load_tiff_from_query(query, data_location)
    volume_um3 = aa.getdatavolume(synaptic_volumes, resolution)

    # # Run Synapse Detection
    # resultvol = syn.getSynapseDetections(synaptic_volumes, query)

    # # Save the probability map to file, if you want
    # outputNPYlocation = os.path.join(
    #     data_location_base, output_foldername, region_name)
    # syn.saveresultvol(resultvol, outputNPYlocation, 'query_', queryID)

    # thresh = 0.9
    # queryresult = sa.compute_measurements(
    #     resultvol, query, volume_um3, thresh)
    queryresult = sa.SynapseAnalysis(query)

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

    # mouse_number = 2
    # mouse_project_str = '2ss'
    # sheet_name = '2ss_fragX'

    output_foldername = 'results_' + sheet_name
    query_fn = mouse_project_str + '_queries.json'
    datalocation = '/Users/anish/Documents/yi_mice/' + \
        str(mouse_number) + 'ss_stacks/'
    data_location_base = '/Users/anish/Documents/yi_mice/' + \
        str(mouse_number) + 'ss_stacks/'

    hostname = socket.gethostname()
    if hostname == 'Galicia':
        datalocation = '/data5TB/yi_mice/' + str(mouse_number) + 'ss_stacks'
        data_location_base = '/data5TB/yi_mice/'
    print('Query Filename: ', query_fn)
    print('Data Location: ', datalocation)
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

    def log_result(result):
        # This is called whenever foo_pool(i) returns a result.
        # result_list is modified only by the main process, not the pool workers.
        result_list.append(result)

    # Setup a list of processes that we want to run
    processes = []
    queryID = 0
    foldernames = []
    for region_num in range(0, 4):
        region_name = region_name_base + str(region_num)
        data_location = os.path.join(data_location_base, region_name)

        for nQuery, query in enumerate(listOfQueries):
            foldername = region_name + '-Q' + str(nQuery)
            foldernames.append(foldername)
            print(foldername)

            pool.apply_async(run_synapse_detection, args=(query, queryID, nQuery, resolution, data_location,
                                                          data_location_base, output_foldername, region_name), callback=log_result)

            queryID = queryID + 1

    # Run processes
    pool.close()
    pool.join()

    print('Get process results from the output queue')

    sorted_queryresult = organize_result_lists(result_list)

    mouse_df = sa.create_synapse_df(sorted_queryresult, foldernames)
    print(mouse_df)

    sheet_name = 'FragileX Mouse'
    fn = sheet_name + '.xlsx'
    df_list = [mouse_df]
    aa.write_dfs_to_excel(df_list, sheet_name, fn)


if __name__ == '__main__':
    main()
