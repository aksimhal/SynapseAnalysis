"""
Antibody Analysis
Contains the functions needed to run SACT
"""
import os
import copy
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
            * (res_xy_nm / 1000) * (res_xy_nm / 1000) * (res_z_nm / 1000)

    elif len(synaptic_volumes['postsynaptic']) > 0:
        volume_um3 = np.prod(synaptic_volumes['postsynaptic'][0].shape) \
            * (res_xy_nm / 1000) * (res_xy_nm / 1000) * (res_z_nm / 1000)

    return volume_um3


class SingleChannelMeasurements:
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
        raw_mean : float
        raw_std : float
        """
        self.name = name
        self.puncta_density = 0.0
        self.puncta_size = 0.0
        self.puncta_std = 0.0
        self.puncta_count = 0
        self.raw_mean = 0.0
        self.raw_std = 0.0
        self.signal_mean = 0.0
        self.signal_std = 0.0


class AntibodyAnalysis:
    """
    Contains the results of run_SACT()

    Attributes
    --------------
    synapse_count : int
    synapse_density : double - Synapse Density
    specificity_ratio: double - TSR
    volume_um3: double
    presynaptic : list of SingleChannelMeasurements objects
    postsynaptic : list of SingleChannelMeasurements objects
    """

    def __init__(self, query):
        """
        Initialize an Antibody Analysis object 

        Parameters 
        ---------------
        query : dict
        """

        self.synapse_density = 0.0
        self.specificity_ratio = 0.0
        self.volume_um3 = 0.0
        self.synapse_count = 0

        presynaptic_list = []
        for name in query['preIF']:
            ab_measure = SingleChannelMeasurements(name)
            presynaptic_list.append(ab_measure)

        postsynaptic_list = []
        for name in query['postIF']:
            ab_measure = SingleChannelMeasurements(name)
            postsynaptic_list.append(ab_measure)

        self.presynaptic_list = presynaptic_list
        self.postsynaptic_list = postsynaptic_list


def compute_single_channel_measurements(synaptic_volumes, antibody_measure, thresh, synaptic_side):
    """Compute single channel measurements needed for SACT

    Parameters
    ---------------
    synaptic_volumes : list
    antibody_measure : AntibodyAnalysis()
    thresh : float
    synaptic_side : str - needed to place results in the correct position of an AntibodyAnalysis object

    Return
    ---------------
    ab_measure : AntibodyAnalysis()
    """

    if synaptic_side == 'presynaptic':
        for n in range(0, len(synaptic_volumes)):
            label_vol = measure.label(synaptic_volumes[n] > thresh)
            stats = measure.regionprops(label_vol)
            antibody_measure.presynaptic_list[n].puncta_density = len(
                stats) / antibody_measure.volume_um3
            antibody_measure.presynaptic_list[n].puncta_count = len(stats)

            arealist = []
            for stat in stats:
                arealist.append(stat.area)

            antibody_measure.presynaptic_list[n].puncta_size = np.mean(
                arealist)
            antibody_measure.presynaptic_list[n].puncta_std = np.std(arealist)

    elif synaptic_side == 'postsynaptic':
        for n in range(0, len(synaptic_volumes)):
            label_vol = measure.label(synaptic_volumes[n] > thresh)
            stats = measure.regionprops(label_vol)
            antibody_measure.postsynaptic_list[n].puncta_density = len(
                stats) / antibody_measure.volume_um3
            antibody_measure.postsynaptic_list[n].puncta_count = len(stats)
            arealist = []
            for stat in stats:
                arealist.append(stat.area)
            antibody_measure.postsynaptic_list[n].puncta_size = np.mean(
                arealist)
            antibody_measure.postsynaptic_list[n].puncta_std = np.std(arealist)

    return antibody_measure


def calculuate_target_ratio(antibody_measure, target_antibody_name):
    """
    Calculate target specificity ratio (tsr) for the antibody specified

    Parameters
    -------------
    antibody_measure : AntibodyAnalysis()
    target_antibody_name : str

    Returns
    ----------------
    antibody_measure : AntibodyAnalysis()

    """
    # find target antibody name
    puncta_count = 0

    for ab_measure in antibody_measure.presynaptic_list:
        if target_antibody_name == ab_measure.name:
            puncta_count = ab_measure.puncta_count

    for ab_measure in antibody_measure.postsynaptic_list:
        if target_antibody_name == ab_measure.name:
            puncta_count = ab_measure.puncta_count

    antibody_measure.specificity_ratio = antibody_measure.synapse_count / puncta_count

    return antibody_measure


def run_SACT(synaptic_volumes, query, thresh, resolution, target_antibody_name):
    """
    Run SACT. 

    MEASURES
    - Puncta Density
    - Average punctum size
    - Standard deviation of the size
    - Synapse density
    - Target Specificity Ratio (tsr)
    - Raw data mean/std

    Parameters
    -----------
    synaptic_volumes : dict - has two keys, 'postsynaptic' and 'presynaptic.' Each key contains a list of volumes. 
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
    print('data volume: ', antibody_measure.volume_um3, 'um3')

    # Check to see if user supplied blobsize
    if 'punctumSize' in query.keys():
        blobsize = query['punctumSize']
        edge_win = int(np.ceil(blobsize * 1.5))

    # Data
    presynaptic_volumes = synaptic_volumes['presynaptic']
    postsynaptic_volumes = synaptic_volumes['postsynaptic']

    # Number of slices each blob should span
    preIF_z = query['preIF_z']
    postIF_z = query['postIF_z']

    # Compute raw mean and standard deviation
    antibody_measure = compute_raw_measures(
        presynaptic_volumes, antibody_measure, 'presynaptic')

    # SNR test
    raw_presynaptic_volumes = []
    for vol in presynaptic_volumes:
        raw_presynaptic_volumes.append(np.copy(vol))

    for n in range(0, len(presynaptic_volumes)):
        presynaptic_volumes[n] = syn.getProbMap(
            presynaptic_volumes[n])  # Step 1
        presynaptic_volumes[n] = syn.convolveVolume(
            presynaptic_volumes[n], blobsize)  # Step 2
        if preIF_z[n] > 1:
            factor_vol = syn.computeFactor(
                presynaptic_volumes[n], int(preIF_z[n]))  # Step 3
            presynaptic_volumes[n] = presynaptic_volumes[n] * factor_vol

    # Compute single channel measurements
    antibody_measure = compute_single_channel_measurements(
        presynaptic_volumes, antibody_measure, thresh, 'presynaptic')

    # SNR test
    antibody_measure = compute_SNR_synapticside(raw_presynaptic_volumes,
                                                presynaptic_volumes, thresh,
                                                antibody_measure, 'presynaptic')

    print('Computed presynaptic single channel measurements')

    # Compute raw mean and standard deviation
    antibody_measure = compute_raw_measures(
        postsynaptic_volumes, antibody_measure, 'postsynaptic')

    # SNR test
    raw_postsynaptic_volumes = []
    for vol in postsynaptic_volumes:
        raw_postsynaptic_volumes.append(np.copy(vol))

    for n in range(0, len(postsynaptic_volumes)):
        postsynaptic_volumes[n] = syn.getProbMap(
            postsynaptic_volumes[n])  # Step 1
        postsynaptic_volumes[n] = syn.convolveVolume(
            postsynaptic_volumes[n], blobsize)  # Step 2
        if postIF_z[n] > 1:
            factor_vol = syn.computeFactor(
                postsynaptic_volumes[n], int(postIF_z[n]))  # Step 3
            postsynaptic_volumes[n] = postsynaptic_volumes[n] * factor_vol

    # Compute single channel measurements
    antibody_measure = compute_single_channel_measurements(
        postsynaptic_volumes, antibody_measure, thresh, 'postsynaptic')

    # SNR test
    antibody_measure = compute_SNR_synapticside(raw_postsynaptic_volumes,
                                                postsynaptic_volumes, thresh,
                                                antibody_measure, 'postsynaptic')
    print('Computed postsynaptic single channel measurements')

    #"""
    if len(postsynaptic_volumes) == 0:
        resultVol = syn.combinePrePostVolumes(
            presynaptic_volumes, postsynaptic_volumes, edge_win, blobsize)
    else:
        resultVol = syn.combinePrePostVolumes(
            postsynaptic_volumes, presynaptic_volumes, edge_win, blobsize)

    # Compute whole statistics
    label_vol = measure.label(resultVol > thresh)
    stats = measure.regionprops(label_vol)
    antibody_measure.synapse_density = len(stats) / antibody_measure.volume_um3
    antibody_measure.synapse_count = len(stats)

    antibody_measure = calculuate_target_ratio(
        antibody_measure, target_antibody_name)
    #"""
    return antibody_measure


def compute_SNR_synapticside(raw_synaptic_volumes, synaptic_volumes, thresh, antibody_measure, synaptic_side):
    """
    """
    if synaptic_side == 'presynaptic':
        for n in range(0, len(synaptic_volumes)):
            signal_mean, signal_std = compute_SNR(
                raw_synaptic_volumes[n], synaptic_volumes[n], thresh)

            antibody_measure.presynaptic_list[n].signal_mean = signal_mean
            antibody_measure.presynaptic_list[n].signal_std = signal_std

    elif synaptic_side == 'postsynaptic':
        for n in range(0, len(synaptic_volumes)):
            signal_mean, signal_std = compute_SNR(
                raw_synaptic_volumes[n], synaptic_volumes[n], thresh)

            antibody_measure.postsynaptic_list[n].signal_mean = signal_mean
            antibody_measure.postsynaptic_list[n].signal_std = signal_std

    return antibody_measure


def compute_SNR(raw_synaptic_volume, synaptic_volume, thresh):
    """ Compute SNR.  
    Threshold 3D blobs, mask out raw data, compute mean blob intensity value

    Parameters
    ----------------
    raw_synaptic_volume : np array
    synaptic_volume : list of np array
    thresh : float
    synaptic_side : str

    Return
    -----------------

    """
    result = []
    bw_vol = synaptic_volume > thresh
    masked_vol = raw_synaptic_volume * bw_vol
    flatvol = masked_vol.flatten()
    zero_inds = np.where(flatvol == 0)
    no_zeros_flatvol = np.delete(flatvol, zero_inds)
    signal_mean = np.mean(no_zeros_flatvol)
    signal_std = np.std(no_zeros_flatvol)

    return signal_mean, signal_std


def compute_raw_measures(synaptic_volumes, antibody_measure, synaptic_side):
    """Compute measurements on the raw data volumes 

    Parameters
    ---------------
    synaptic_volumes : list
    antibody_measure : AntibodyAnalysis()
    synaptic_side : str

    Return
    ---------------
    ab_measure : AntibodyAnalysis()
    """

    if synaptic_side == 'presynaptic':
        for n in range(0, len(synaptic_volumes)):
            raw_mean = np.mean(synaptic_volumes[n])
            raw_std = np.std(synaptic_volumes[n])

            antibody_measure.presynaptic_list[n].raw_mean = raw_mean
            antibody_measure.presynaptic_list[n].raw_std = raw_std

    elif synaptic_side == 'postsynaptic':
        for n in range(0, len(synaptic_volumes)):
            raw_mean = np.mean(synaptic_volumes[n])
            raw_std = np.std(synaptic_volumes[n])

            antibody_measure.postsynaptic_list[n].raw_mean = raw_mean
            antibody_measure.postsynaptic_list[n].raw_std = raw_std

    return antibody_measure


def run_ab_analysis_rayleigh(synaptic_volumes, query, thresh, resolution, target_antibody_name):
    """
    Run AB Analysis - special case 

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

    # Check to see if user supplied blobsize
    if 'punctumSize' in query.keys():
        blobsize = query['punctumSize']
        edge_win = int(np.ceil(blobsize * 1.5))

    # Data
    presynaptic_volumes = synaptic_volumes['presynaptic']
    postsynaptic_volumes = synaptic_volumes['postsynaptic']

    # Number of slices each blob should span
    preIF_z = query['preIF_z']
    postIF_z = query['postIF_z']

    for n in range(0, len(presynaptic_volumes)):
        presynaptic_volumes[n] = syn.getProbMap_rayleigh(
            presynaptic_volumes[n])  # Step 1
        presynaptic_volumes[n] = syn.convolveVolume(
            presynaptic_volumes[n], blobsize)  # Step 2
        if preIF_z[n] > 1:
            factor_vol = syn.computeFactor(
                presynaptic_volumes[n], int(preIF_z[n]))  # Step 3
            presynaptic_volumes[n] = presynaptic_volumes[n] * factor_vol

    # Compute single channel measurements
    antibody_measure = compute_single_channel_measurements(
        presynaptic_volumes, antibody_measure, thresh, 'presynaptic')
    print('Computed presynaptic single channel measurements')

    for n in range(0, len(postsynaptic_volumes)):
        postsynaptic_volumes[n] = syn.getProbMap_rayleigh(
            postsynaptic_volumes[n])  # Step 1
        postsynaptic_volumes[n] = syn.convolveVolume(
            postsynaptic_volumes[n], blobsize)  # Step 2
        if postIF_z[n] > 1:
            factor_vol = syn.computeFactor(
                postsynaptic_volumes[n], int(postIF_z[n]))  # Step 3
            postsynaptic_volumes[n] = postsynaptic_volumes[n] * factor_vol

    # Compute single channel measurements
    antibody_measure = compute_single_channel_measurements(
        postsynaptic_volumes, antibody_measure, thresh, 'postsynaptic')
    print('Computed postsynaptic single channel measurements')

    if len(postsynaptic_volumes) == 0:
        resultVol = syn.combinePrePostVolumes(
            presynaptic_volumes, postsynaptic_volumes, edge_win, blobsize)
    else:
        resultVol = syn.combinePrePostVolumes(
            postsynaptic_volumes, presynaptic_volumes, edge_win, blobsize)

    # Compute whole statistics
    label_vol = measure.label(resultVol > thresh)
    stats = measure.regionprops(label_vol)
    antibody_measure.synapse_density = len(stats) / antibody_measure.volume_um3
    antibody_measure.synapse_count = len(stats)

    antibody_measure = calculuate_target_ratio(
        antibody_measure, target_antibody_name)

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
    """This function compares multiple antibody clones by using SACT

    Paramters
    ---------------
    query_list : list of dicts - contains queries
    folder_names : list of strs - contains the foldernames if each antibody subclone is in its own folder
    base_dir : str - data location
    thresh : float
    resolution : dict
    target_filename : list

    Return
    ----------------
    measure_list : list
    """
    measure_list = []
    for n, query in enumerate(query_list):

        if folder_names == None:
            data_location = base_dir
        else:
            foldername = folder_names[n]
            data_location = os.path.join(base_dir, foldername)

        target_antibody_name = target_filenames[n]
        synaptic_volumes = da.load_tiff_from_query(query, data_location)
        measure = run_SACT(synaptic_volumes, query, thresh,
                           resolution, target_antibody_name)

        measure_list.append(measure)

    return measure_list


def calculate_measure_lists_rayleigh(query_list, folder_names, base_dir, thresh,
                                     resolution, target_filenames):
    """compare multiple antibody clones - special case 

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
        measure = run_ab_analysis_rayleigh(
            synaptic_volumes, query, thresh, resolution, target_antibody_name)

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
                    'Puncta Volume', 'Puncta STD', 'Synapse Density',
                    'TSR', 'Raw Mean', 'Raw STD', 'Signal Mean', 'Signal STD']

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
        df.iloc[n, 7] = target_measure.raw_mean
        df.iloc[n, 8] = target_measure.raw_std
        df.iloc[n, 9] = target_measure.signal_mean
        df.iloc[n, 10] = target_measure.signal_std

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


def create_pairwise_df(measure1, measure2, target_antibody_name1, target_antibody_name2):
    """Create a dataframe for pairwise comparisons

    Paramters
    ------------
    measure1 : AntibodyAnalysis
    measure2 : AntibodyAnalysis
    target_antibody_name1 : str
    target_antibody_name2 : str

    Return
    ------------
    df : dataframe
    """

    columnlabels = ['Target AB', 'Conjugate AB', 'Puncta Density',
                    'Puncta Volume', 'Puncta STD', 'Synapse Density', 'TSR']
    df = pd.DataFrame(np.nan, index=['AB1', 'AB2'], columns=columnlabels)

    df.iloc[0, 0] = target_antibody_name1
    df.iloc[1, 0] = target_antibody_name2

    conjugate_ab_name = find_conjugate_name(measure1, target_antibody_name1)
    df.iloc[0, 1] = conjugate_ab_name
    target_measure = find_target_measure(measure1, target_antibody_name1)
    df.iloc[0, 2] = target_measure.puncta_density
    df.iloc[0, 3] = target_measure.puncta_size
    df.iloc[0, 4] = target_measure.puncta_std
    df.iloc[0, 5] = measure1.synapse_density
    df.iloc[0, 6] = measure1.specificity_ratio

    target_measure = find_target_measure(measure2, target_antibody_name2)
    conjugate_ab_name = find_conjugate_name(measure2, target_antibody_name2)
    df.iloc[1, 1] = conjugate_ab_name
    df.iloc[1, 2] = target_measure.puncta_density
    df.iloc[1, 3] = target_measure.puncta_size
    df.iloc[1, 4] = target_measure.puncta_std
    df.iloc[1, 5] = measure2.synapse_density
    df.iloc[1, 6] = measure2.specificity_ratio

    return df


def find_conjugate_name(measure, target_ab_name):
    """Find conjugate antibody name

    Paramters
    -----------
    measure : AntibodyAnalysis
    target_ab_name : str

    Return
    ------------
    conjugate_name : str
    """
    for n in measure.postsynaptic_list:
        if n.name != target_ab_name:
            conjugate_name = n.name

    for n in measure.presynaptic_list:
        if n.name != target_ab_name:
            conjugate_name = n.name

    return conjugate_name


def run_pairwise(query1, query2, target_antibody_name1, target_antibody_name2,
                 base_dir, thresh, resolution):
    """
    Run pairwise

    Parameters
    -------------
    query1 : dict
    query2 : dict
    target_antibody_name1 : str
    target_antibody_name2 : str
    base_dir : str
    thresh : float
    resultion : dict

    Return
    -------------
    [measure1, measure2] : list of AntibodyAnalysis objects
    """

    synaptic_volumes1 = da.load_tiff_from_query(query1, base_dir)
    measure1 = run_SACT(
        synaptic_volumes1, query1, thresh, resolution, target_antibody_name1)

    synaptic_volumes2 = da.load_tiff_from_query(query2, base_dir)
    measure2 = run_SACT(
        synaptic_volumes2, query2, thresh, resolution, target_antibody_name2)

    return [measure1, measure2]


def findFilenames(reference_fn_str, target_fn_str, filenames, n):
    """
    Find filenames given a start string for UC Davis data

    Parameters
    --------------
    reference_fn_str : str - the control antibody (reference antibody)
    target_fn_str : str - the antibody of interest
    filenames : list of strs - contains the filenames in the folder to search
    n : int
    Returns
    --------------
    reference_name : str - reference antibody filename
    target_name : str - target antibody filename
    """

    reference_str = str(n) + '-' + reference_fn_str  # filename to search for
    target_str = str(n) + '-' + target_fn_str

    # Search for file associated with the specific dataset number
    indices = [i for i, s in enumerate(
        filenames) if reference_str.lower() == s[0:len(reference_str)].lower()]
    reference_name = filenames[indices[0]]
    print(reference_name)
    indices = [i for i, s in enumerate(
        filenames) if target_str.lower() == s[0:len(target_str)].lower()]
    target_name = filenames[indices[0]]
    print(target_name)
    return reference_name, target_name
