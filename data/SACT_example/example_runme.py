"""
Example runme for the synaptic antibody characterization tool.
"""
import os
import sys
import socket
import numpy as np
import pandas as pd #also requires xlsxwriter
from at_synapse_detection import dataAccess as da
from at_synapse_detection import antibodyAnalysis as aa


def psd_pairwise_comparison():
    """Compare two PSD-95 clones.  This is just one way of setting up the 
    queries/data locations.  See the 'antibody_analysis' folder for multiple examples 
    of how to set up the tool. 

    Query Format (dict): 
        preIF : list of strs - name of the channel
        preIF_z : list of ints - number of slices to span. default=[2]
        postIF : list of strs
        postIF_z : list of ints. default=[2]
        punctumSize : number of pixels x/y that a puncta should span. default=2
    
    Returns
    -----------------
    df : dataframe - contains the results of the SACT 
    """
    # Location of the data 
    base_dir = '../example/' 
    
    # Data resolution, in nanometers 
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70}
    
    # Threshold value for the probability maps. This value does not usually need to be changed. 
    thresh = 0.9

    # List the file names 
    target_filenames = ['PSD95m_1st.tif', 'PSD95r_2nd.tif']
    reference_filenames = ['synapsin_1st.tif', 'synapsin_1st.tif']

    # Create a query for each pair
    query_list = []
    for n in range(0, len(target_filenames)):
        target_name = target_filenames[n] # The AB we're interested in testing (PSD)
        reference_name = reference_filenames[n] # The previously validated AB (synapsin)
        
        # Formulate the query
        query = {'preIF': [reference_name], 'preIF_z': [2], 
                 'postIF': [target_name], 'postIF_z': [2],
                 'punctumSize': 2}
        query_list.append(query)

    # Run the SACT 
    measure_list = aa.calculate_measure_lists(query_list, None, base_dir,
                                        thresh, resolution, target_filenames)
    
    # Convert measure object to a dataframe 
    project_names = ['PSD_M', 'PSD_R']
    df = aa.create_df(measure_list, project_names, target_filenames, reference_filenames)
    print(df)

    return df


def main():
    # Output filename
    fn = 'sact_psd_example.xlsx'
    sheet_name = 'sact_psd_example'

    # Determine if file exists. This is only an issue when running on windows
    if  os.path.isfile(fn): 
        print('A sheet with this name already exists; rename sheet and rerun')
        if socket.gethostname() != 'anish': #this line is optional 
            sys.exit()

    
    
    psd_df = psd_pairwise_comparison()
    df_list = [psd_df]

    # Export the dataframe to excel 
    aa.write_dfs_to_excel(df_list, sheet_name, fn)


if __name__ == '__main__':
    main()
