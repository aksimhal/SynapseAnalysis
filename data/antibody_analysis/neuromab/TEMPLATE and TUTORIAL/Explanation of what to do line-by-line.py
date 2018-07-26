"""
Run antibody characterization tool on the L110-CCK dataset
Output an excel sheet of results
"""
import os
import numpy as np
import pandas as pd #also requires xlsxwriter
from at_synapse_detection import dataAccess as da
from at_synapse_detection import antibodyAnalysis as aa



def NAME():
    """ Run antibody characterization tool on the L110-CCK dataset


    Return
    ----------
    df : dataframe - contains results
    """

    # Location of data
    base_dir = "(Location)" #Location of align tif --> Should be the location of the experiment's align tiff folder, ex: "C/desktop/work/image_processing/YYYYMMDD/align_tiffs"
    resolution = {'res_xy_nm': 100, 'res_z_nm': 70} #Resolution of a pixel (do not alter)
    thresh = 0.9 #What qualifies for final probability map (do not alter)
    number_of_datasets = 20 #Number of wells in the experiemnts, "20" is an example where there are 16 samples and 4 controls

    #Rb Antibody
    conjugate_fn_str = 'GAD2' #String segment to search in a filename
    #conjugate_fn_str should be the term used in the name of the control align tiff for a well (usually "PSD", "GAD2", or "SYNAPSIN")
    target_fn_str = 'L106'
    #Ms Antibody project name, no parent or subclone number needed
    #target_fn_str should be the project number, for instance if this was testing L109 samples, this would be "L109"
    #Takes base directory string and gives you an array of all the files within
    filenames = aa.getListOfFolders(base_dir) #Do not change
    conjugate_filenames = [] #Do not change
    target_filenames = [] #Do not change
    query_list = [] #Do not change
    folder_names = [] #Do not change

    for n in range(1, 17):
        #Use if dataset missing
        #This is where you put in the rangee of wells used as your test samples
        #Since we have 16 samples that are test samples for L106, the range is equal to 1 through n+1, or 1 through 17
        #If your test samples do not begin at well 1, then adjust the beginning of the range accordingly (3 through 17 if the first test sample is in well 3) 
            #continue

        print('Well: ', str(n)) #Do not change
        folder_names.append('Test-' + str(n)) # Collate 'dataset' names for excel sheet #Do not change
        conjugate_str = str(n) + '-' + conjugate_fn_str #creates filename to search for #Creates n-conjugatename #Do not change
        target_str = str(n) + '-' + target_fn_str #Do not change

        # Search for file associated with the specific dataset number
        indices = [i for i, s in enumerate(filenames) if conjugate_str == s[0:len(conjugate_str)]] #Do not change
        conjugate_name = filenames[indices[0]] #Do not change
        print(conjugate_name) #Do not change
        indices = [i for i, s in enumerate(filenames) if target_str == s[0:len(target_str)]] #Do not change
        target_name = filenames[indices[0]] #Do not change
        print(target_name) #Do not change
        
        conjugate_filenames.append(conjugate_name) #Do not change
        target_filenames.append(target_name) #Do not change

        # Create query
        #
        query = {'preIF': [conjugate_name], 'preIF_z': [2],
                'postIF': [target_name], 'postIF_z': [1],
                'punctumSize': 2}
        #preIF = items that are presynaptic targets go here, because GAD2, our conjugate, is presynaptic I put the conjugate_name in this box
        #preIF_z = how many tiffs a puncta must be in to be registered, conjugate sample number is 2 so 2 goes in this box
        #postIF = items that are postsynaptic targets go here, L106 is postsynaptic so I put target_name here
        #postIF_z = how many tiffs a puncta must be in to be registered, target sample number is 1 (for now unless changed later) 
        #punctumSize = size of punctum the algorithm is looking for, do not change unless directed to

        """Example of a presynaptic target and presynaptic conjugate
            query = {'preIF': [target_name,conjugate_name], 'preIF_z': [1,2],
                'postIF': [], 'postIF_z': [],
                'punctumSize': 2}"""

        """Example of a postsynaptic target and presynaptic conjugate
            query = {'preIF': [conjugate_name], 'preIF_z': [2],
                'postIF': [target_name], 'postIF_z': [1],
                'punctumSize': 2}"""

        """Example of a postsynaptic target and postsynaptic conjugate
            query = {'preIF': [], 'preIF_z': [],
                'postIF': [target_name,conjugate_name], 'postIF_z': [1,2],
                'punctumSize': 2}"""

        """Example of a presynaptic target and postsynaptic conjugate
            query = {'preIF': [target_name], 'preIF_z': [1],
                'postIF': [conjugate_name], 'postIF_z': [2],
                'punctumSize': 2}"""


        query_list.append(query)


    #The following n samples are controls - you can add as many of these as you want by copying the block of code and pasting it after the last one
    #The notes in the following block of code apply to all of the controls
    n = 17 #well number of control sample
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet #Do not change
    reference_fn_str = 'GAD2' #String segment to search in a filename #refernce_fn_str is the project number/name of RB control
    target_fn_str = 'L106' #target_fn_str is the project number of the Ms control you are using
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n) #Do not alter
    conjugate_filenames.append(conjugate_name) #Do not alter
    target_filenames.append(target_name) #Do not alter
    query = {'preIF': [conjugate_name], 'preIF_z': [2], 'postIF': [target_name], 'postIF_z': [1], 'punctumSize': 2} #Se the examples and explanations above about "query"
    query_list.append(query) #Do not change

    n = 18
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'GAD2' #String segment to search in a filename
    target_fn_str = 'SP2'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [target_name,conjugate_name], 'preIF_z': [1,2], 'postIF': [], 'postIF_z': [], 'punctumSize': 2}
    query_list.append(query)

    n = 19
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'NP-RB' #String segment to search in a filename
    target_fn_str = 'NP-MS'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [], 'preIF_z': [], 'postIF': [target_name,conjugate_name], 'postIF_z': [1,2], 'punctumSize': 2}
    query_list.append(query)

    n = 20
    folder_names.append('Control' + str(n)) # Collate 'dataset' names for excel sheet
    reference_fn_str = 'NPNS-RB' #String segment to search in a filename
    target_fn_str = 'NPNS-MS'
    conjugate_name, target_name = aa.findFilenames(reference_fn_str, target_fn_str, filenames, n)
    conjugate_filenames.append(conjugate_name)
    target_filenames.append(target_name)
    query = {'preIF': [], 'preIF_z': [], 'postIF': [target_name,conjugate_name], 'postIF_z': [1,2], 'punctumSize': 2}
    query_list.append(query)


    
    measure_list = aa.calculate_measure_lists(query_list, None, base_dir,
                                        thresh, resolution, target_filenames) # Run all the queries

    df = aa.create_df(measure_list, folder_names, target_filenames, conjugate_filenames) #Do not change
    print(df) #Do not change

    return df #Do not change
    

def main(): #Do not change
    """ Run comparisons """

    NAME_df = Name() #The "NAME" should match the term used in line 13
    
    sheet_name = 'YYYYMMDD_(project title)' #name of excel sheet
    fn = 'YYYMMDD_(project title).xlsx' #name of excel file
    df_list = [NAME_df] # the term inside the brackets must match the _____df in line 155
    aa.write_dfs_to_excel(df_list, sheet_name, fn) #Do not change
    

if __name__ == '__main__': #Do not change
    main() #Do not change
