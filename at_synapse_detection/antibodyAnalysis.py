"""
Antibody Analysis
"""
import os
import numpy as np
import pandas as pd
from skimage import measure
from at_synapse_detection import SynapseDetection as syn
from at_synapse_detection import dataAccess as da

def getdatavolume(synaptic_volumes, resolution):
    """
    Compute volume of data in cubic microns

    Parameters
    -------------
    synaptic_volumes : dict
    resolution : dict

    Return
    --------------
    volume_um3 : double
    """

    res_xy_nm = resolution['res_xy_nm']
    res_z_nm = resolution['res_z_nm']

    # Compute Volume
    if len(synaptic_volumes['presynaptic']) > 0:
        volume_um3 = np.prod(synaptic_volumes['presynaptic'][0].shape) \
        * (res_xy_nm/1000) * (res_xy_nm/1000) * (res_z_nm/1000)

    elif len(synaptic_volumes['postsynaptic']) > 0:
        volume_um3 = np.prod(synaptic_volumes['postsynaptic'][0].shape) \
        * (res_xy_nm/1000) * (res_xy_nm/1000) * (res_z_nm/1000)

    return volume_um3

class ABMeasures:
    """
    Single channel measurements
    """

    def __init__(self, name):
        """
        name : str - name of channel
        puncta_density : float
        puncta_size : float
        puncta_std : float
        puncta_count : int
        """
        self.name = name
        self.puncta_density = 0.0
        self.puncta_size = 0.0
        self.puncta_std = 0.0
        self.puncta_count = 0



class AntibodyAnalysis:
    """
    Contains the results of run_ab_analysis()

    Attributes
    --------------
    synapse_count : int
    synapse_density : double - Synapse Density
    specificity_ratio: double - TSR
    volume_um3: double
    presynaptic : list of dicts
    postsynaptic : list of dicts

    """
    def __init__(self, query):
        """
        query : dict
        """

        self.synapse_density = 0.0
        self.specificity_ratio = 0.0
        self.volume_um3 = 0.0
        self.synapse_count = 0

        presynaptic_list = []
        for name in query['preIF']:
            ab_measure = ABMeasures(name)
            presynaptic_list.append(ab_measure)

        postsynaptic_list = []
        for name in query['postIF']:
            ab_measure = ABMeasures(name)
            postsynaptic_list.append(ab_measure)

        self.presynaptic_list = presynaptic_list
        self.postsynaptic_list = postsynaptic_list


def single_channel_measurements(synaptic_volumes, antibody_measure, thresh, synaptic_side):
    """Compute single channel measurements
    Parameters
    ---------------
    synaptic_volumes : list
    antibody_measure : AntibodyAnalysis()
    thresh : float
    synaptic_side : str

    Return
    ---------------
    ab_measure : AntibodyAnalysis()
    """

    if synaptic_side == 'presynaptic':
        for n in range(0, len(synaptic_volumes)):
            label_vol = measure.label(synaptic_volumes[n] > thresh)
            stats = measure.regionprops(label_vol)
            antibody_measure.presynaptic_list[n].puncta_density = len(stats) / antibody_measure.volume_um3
            antibody_measure.presynaptic_list[n].puncta_count = len(stats)

            arealist = []
            for stat in stats:
                arealist.append(stat.area)

            antibody_measure.presynaptic_list[n].puncta_size = np.mean(arealist)
            antibody_measure.presynaptic_list[n].puncta_std = np.std(arealist)

    elif synaptic_side == 'postsynaptic':
        for n in range(0, len(synaptic_volumes)):
            label_vol = measure.label(synaptic_volumes[n] > thresh)
            stats = measure.regionprops(label_vol)
            antibody_measure.postsynaptic_list[n].puncta_density = len(stats) / antibody_measure.volume_um3
            antibody_measure.postsynaptic_list[n].puncta_count = len(stats)
            arealist = []
            for stat in stats:
                arealist.append(stat.area)
            antibody_measure.postsynaptic_list[n].puncta_size = np.mean(arealist)
            antibody_measure.postsynaptic_list[n].puncta_std = np.std(arealist)

    return antibody_measure

def calculuate_target_ratio(antibody_measure, target_antibody_name):
    """
    Calculate target specificity ratio (tsr)

    Parameters
    -------------
    antibody_measure : AntibodyAnalysis()
    target_antibody_name : str

    Returns
    ----------------
    antibody_measure : AntibodyAnalysis()

    """
    #find target antibody name
    puncta_count = 0

    for ab_measure in antibody_measure.presynaptic_list:
        if target_antibody_name == ab_measure.name:
            puncta_count = ab_measure.puncta_count

    for ab_measure in antibody_measure.postsynaptic_list:
        if target_antibody_name == ab_measure.name:
            puncta_count = ab_measure.puncta_count

    antibody_measure.specificity_ratio = antibody_measure.synapse_count / puncta_count

    return antibody_measure



def run_ab_analysis(synaptic_volumes, query, thresh, resolution, target_antibody_name):
    """
    Run AB Analysis

    MEASURES
    - Puncta Density
    - Average punctum size
    - Standard deviation of the size
    - Synapse density
    - Target Specificity Ratio (tsr)

    Parameters
    -----------
    synaptic_volumes : dict
    query : dict
    thresh : float
    resolution : dict

    Returns
    -----------
    antibody_measure : AntibodyAnalysis()
    """

    antibody_measure = AntibodyAnalysis(query)

    # Get data volume
    antibody_measure.volume_um3 = getdatavolume(synaptic_volumes, resolution)
    print('data volume: ', antibody_measure.volume_um3)

    #Check to see if user supplied blobsize
    if 'punctumSize' in query.keys():
        blobsize = query['punctumSize']
        edge_win = int(np.ceil(blobsize*1.5))

    # Data
    presynaptic_volumes = synaptic_volumes['presynaptic']
    postsynaptic_volumes = synaptic_volumes['postsynaptic']

    # Number of slices each blob should span
    preIF_z = query['preIF_z']
    postIF_z = query['postIF_z']

    for n in range(0, len(presynaptic_volumes)):
        presynaptic_volumes[n] = syn.getProbMap(presynaptic_volumes[n]) # Step 1
        presynaptic_volumes[n] = syn.convolveVolume(presynaptic_volumes[n], blobsize) # Step 2
        if preIF_z[n] > 1:
            factor_vol = syn.computeFactor(presynaptic_volumes[n], int(preIF_z[n])) # Step 3
            presynaptic_volumes[n] = presynaptic_volumes[n] * factor_vol

    # Compute single channel measurements
    antibody_measure = single_channel_measurements(presynaptic_volumes, antibody_measure, thresh, 'presynaptic')
    print('Computed presynaptic single channel measurements')


    for n in range(0, len(postsynaptic_volumes)):
        postsynaptic_volumes[n] = syn.getProbMap(postsynaptic_volumes[n]) # Step 1
        postsynaptic_volumes[n] = syn.convolveVolume(postsynaptic_volumes[n], blobsize) # Step 2
        if postIF_z[n] > 1:
            factor_vol = syn.computeFactor(postsynaptic_volumes[n], int(postIF_z[n])) # Step 3
            postsynaptic_volumes[n] = postsynaptic_volumes[n] * factor_vol

    # Compute single channel measurements
    antibody_measure = single_channel_measurements(postsynaptic_volumes, antibody_measure, thresh, 'postsynaptic')
    print('Computed postsynaptic single channel measurements')



    if len(postsynaptic_volumes) == 0:
        resultVol = syn.combinePrePostVolumes(presynaptic_volumes, postsynaptic_volumes, edge_win, blobsize)
    else:
        resultVol = syn.combinePrePostVolumes(postsynaptic_volumes, presynaptic_volumes, edge_win, blobsize)

    # Compute whole statistics
    label_vol = measure.label(resultVol > thresh)
    stats = measure.regionprops(label_vol)
    antibody_measure.synapse_density = len(stats) / antibody_measure.volume_um3
    antibody_measure.synapse_count = len(stats)

    antibody_measure = calculuate_target_ratio(antibody_measure, target_antibody_name)

    return antibody_measure



def write_dfs_to_excel(df_list, sheets, file_name, spaces=1):
    """
    Write multiple dataframes to an excel file
    source:https://stackoverflow.com/questions/32957441/\
                   putting-many-python-pandas-dataframes-to-one-excel-worksheet

    Parameters
    --------------
    df_list : list of dataframes
    sheets : str - name of sheet in excel
    file_name : str
    spaces : int - number of rows to skip, default = 1

    """

    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    row = 0
    for dataframe in df_list:
        dataframe.to_excel(writer, sheet_name=sheets, startrow=row, startcol=0)
        row = row + len(dataframe.index) + spaces + 1
    writer.save()


def find_target_measure(measure, target_ab_name):
    """Find target antibody measurement object

    Paramters
    -----------
    measure : AntibodyAnalysis
    target_ab_name : str

    Return
    ------------
    target_measure : ABMeasures
    """
    for n in measure.postsynaptic_list:
        if n.name == target_ab_name:
            target_measure = n

    for n in measure.presynaptic_list:
        if n.name == target_ab_name:
            target_measure = n

    return target_measure


def calculate_measure_lists(query_list, folder_names, base_dir, thresh,
                                 resolution, target_filenames):
    """compare multiple antibody clones

    Paramters
    ---------------
    query_list : list
    folder_names : list
    base_dir : str
    thresh : float
    resolution : dict
    target_filename : list

    Return
    ----------------
    measure_list : list
    """

    measure_list = []
    for n, query in enumerate(query_list):
        #query = query_list[n]

        if folder_names == None:
            data_location = base_dir
        else:
            foldername = folder_names[n]
            data_location = os.path.join(base_dir, foldername)
        target_antibody_name = target_filenames[n]
        synaptic_volumes = da.load_tiff_from_query(query, data_location)
        measure = run_ab_analysis(synaptic_volumes, query, thresh, resolution, target_antibody_name)

        measure_list.append(measure)

    return measure_list



def create_df(measure_list, folder_names, target_filenames, conjugate_filenames):
    """Create concetration comparison dataframes

    Paramters
    ------------
    measure_list : list
    folder_names : list
    target_filenames : list
    conjugate_filenames : list

    Return
    -------------
    df : dataframe
    """
    columnlabels = ['Target AB', 'Conjugate AB', 'Puncta Density',
                    'Puncta Volume', 'Puncta STD', 'Synapse Density', 'TSR']

    df = pd.DataFrame(np.nan, index=folder_names, columns=columnlabels)

    for n, measure in enumerate(measure_list):
        target_antibody_name = target_filenames[n]
        conjugate_antibody_name = conjugate_filenames[n]
        df.iloc[n, 0] = target_antibody_name
        df.iloc[n, 1] = conjugate_antibody_name

        target_measure = find_target_measure(measure, target_antibody_name)
        df.iloc[n, 2] = target_measure.puncta_density
        df.iloc[n, 3] = target_measure.puncta_size
        df.iloc[n, 4] = target_measure.puncta_std
        df.iloc[n, 5] = measure.synapse_density
        df.iloc[n, 6] = measure.specificity_ratio

    return df

def getListOfFolders(base_dir):
    """Get list of folders in specified directory

    Paramters
    -----------
    base_dir : str

    Return
    -----------
    folder_list : list of strs
    """
    folder_list = os.listdir(base_dir)
    #print('Raw Folder List: ', folder_list)
    foldernames_to_remove = []
    # Remove hidden folders
    for foldername in folder_list:
        if foldername[0] == '.':
            foldernames_to_remove.append(foldername)
            continue

        if foldername[0:4] == 'Icon':
            foldernames_to_remove.append(foldername)
            continue

        if foldername == 'Icon':
            foldernames_to_remove.append(foldername)
            continue

    for foldername in foldernames_to_remove:
        folder_list.remove(foldername)
    #print('Cleaned folder_list: ', cleaned_folderlist)
    return folder_list


def find_filename(str_to_match, foldername, base_dir):
    """Find target filename

    Parameters
    --------------
    str_to_match : str

    Returns
    --------------
    matched_filename : str
    """

    input_dir = os.path.join(base_dir, foldername)
    file_list = os.listdir(input_dir)
    matched_filename = None
    for filename in file_list:

        # Find string
        if str_to_match == filename[0:len(str_to_match)]:
            matched_filename = filename

    if matched_filename == None:
        print(file_list)

    return matched_filename


