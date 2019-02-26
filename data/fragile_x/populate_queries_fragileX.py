"""
Create the query files for exploring the FXS data
"""
import os
import sys
import json
from at_synapse_detection import dataAccess as da


def single_channel_queries(mouse_number):
    """ Single channel queries

    Parameters
    -------------
    mouse_number
    """
    listOfQueries = []
    punctum_size = 2

    for slice_span in range(1, 4):

        # Query 0 - PSD-95
        preIF = []
        preIF_z = []
        postIF_str = str(mouse_number) + 'ss_PSD.tif'
        postIF = [postIF_str]
        postIF_z = [slice_span]
        query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
                 'postIF_z': postIF_z, 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 1 - Synapsin
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF = [preIF_str1]
        preIF_z = [slice_span]
        postIF = []
        postIF_z = []
        query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
                 'postIF_z': postIF_z, 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 2 - VGluT1
        preIF_str1 = str(mouse_number) + 'ss_VGluT1.tif'
        preIF = [preIF_str1]
        preIF_z = [slice_span]
        postIF = []
        postIF_z = []
        query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
                 'postIF_z': postIF_z, 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 3 - VGluT2
        preIF_str1 = str(mouse_number) + 'ss_VGluT2.tif'
        preIF = [preIF_str1]
        preIF_z = [slice_span]
        postIF = []
        postIF_z = []
        query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
                 'postIF_z': postIF_z, 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 4 - Gephyrin
        preIF = []
        preIF_z = []
        postIF_str = str(mouse_number) + 'ss_Geph.tif'
        postIF = [postIF_str]
        postIF_z = [slice_span]
        query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
                 'postIF_z': postIF_z, 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 5 - GAD
        preIF_str1 = str(mouse_number) + 'ss_GAD.tif'
        preIF = [preIF_str1]
        preIF_z = [slice_span]
        postIF = []
        postIF_z = []
        query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
                 'postIF_z': postIF_z, 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 6 - GS
        preIF_str1 = str(mouse_number) + 'ss_GS.tif'
        preIF = [preIF_str1]
        preIF_z = [slice_span]
        postIF = []
        postIF_z = []
        query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
                 'postIF_z': postIF_z, 'punctumSize': punctum_size}
        listOfQueries.append(query)

    data = {'listOfQueries': listOfQueries}
    fn = '/Users/anish/Documents/Connectome/SynapseAnalysis/data/fragile_x/queries/' + \
        str(mouse_number) + 'ss_puncta_queries.json'
    da.writeJSONFile(fn, data)


def excitatory_queries(mouse_number):
    """ List of excitatory queries

    Parameters
    -------------
    mouse_number
    """
    listOfQueries = []
    punctum_size = 2

    for slice_span in range(1, 4):

        # Query 0
        preIF_str = str(mouse_number) + 'ss_Synap.tif'
        preIF = [preIF_str]
        preIF_z = [slice_span]
        postIF_str = str(mouse_number) + 'ss_PSD.tif'
        postIF = [postIF_str]
        postIF_z = [slice_span]
        query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
                 'postIF_z': postIF_z, 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 1
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF_str2 = str(mouse_number) + 'ss_VGluT1.tif'
        preIF = [preIF_str1, preIF_str2]
        preIF_z = [slice_span, slice_span]
        postIF_str = str(mouse_number) + 'ss_PSD.tif'
        postIF = [postIF_str]
        postIF_z = [slice_span]
        query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
                 'postIF_z': postIF_z, 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 2
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF_str2 = str(mouse_number) + 'ss_VGluT2.tif'
        preIF = [preIF_str1, preIF_str2]
        preIF_z = [slice_span, slice_span]
        postIF_str = str(mouse_number) + 'ss_PSD.tif'
        postIF = [postIF_str]
        postIF_z = [slice_span]
        query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
                 'postIF_z': postIF_z, 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 3
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF_str2 = str(mouse_number) + 'ss_VGluT1.tif'
        preIF_str3 = str(mouse_number) + 'ss_VGluT2.tif'
        preIF = [preIF_str1, preIF_str2, preIF_str3]
        preIF_z = [slice_span, slice_span, slice_span]
        postIF_str = str(mouse_number) + 'ss_PSD.tif'
        postIF = [postIF_str]
        postIF_z = [slice_span]
        query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
                 'postIF_z': postIF_z, 'punctumSize': punctum_size}
        listOfQueries.append(query)

    data = {'listOfQueries': listOfQueries}
    fn = '/Users/anish/Documents/Connectome/SynapseAnalysis/data/fragile_x/queries/' + \
        str(mouse_number) + 'ss_queries.json'
    da.writeJSONFile(fn, data)


def mouse_query_vglut2(mouse_number):
    """ query for psd, synapsin, vglut1, and vglut2

    Parameters
    -------------
    mouse_number
    """

    listOfQueries = []
    punctum_size = 2

    # Query 0
    preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
    preIF_str2 = str(mouse_number) + 'ss_VGluT2.tif'
    preIF = [preIF_str1, preIF_str2]
    preIF_z = [1, 2]
    postIF_str = str(mouse_number) + 'ss_PSD.tif'
    postIF = [postIF_str]
    postIF_z = [1]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
             'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    # Query 1
    preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
    preIF_str2 = str(mouse_number) + 'ss_VGluT1.tif'
    preIF_str3 = str(mouse_number) + 'ss_VGluT2.tif'
    preIF = [preIF_str1, preIF_str2, preIF_str3]
    preIF_z = [1, 1, 2]
    postIF_str = str(mouse_number) + 'ss_PSD.tif'
    postIF = [postIF_str]
    postIF_z = [1]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
             'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    data = {'listOfQueries': listOfQueries}
    fn = '/Users/anish/Documents/Connectome/SynapseAnalysis/data/fragile_x/queries/' + \
        str(mouse_number) + 'ss_vglut2_queries.json'
    da.writeJSONFile(fn, data)


def inhibitory_queries(mouse_number):
    """ Inhibitory queries at different sizes

    Parameters
    -------------
    mouse_number
    """
    listOfQueries = []
    punctum_size = 2
    for slice_span in range(1, 4):

        # Query - 1
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF_str2 = str(mouse_number) + 'ss_GAD.tif'
        preIF = [preIF_str1, preIF_str2]
        preIF_z = [slice_span, slice_span]
        postIF_str1 = str(mouse_number) + 'ss_Geph.tif'
        postIF = [postIF_str1]
        postIF_z = [slice_span]
        query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
                 'postIF_z': postIF_z, 'punctumSize': punctum_size}
        listOfQueries.append(query)

    data = {'listOfQueries': listOfQueries}
    fn = '/Users/anish/Documents/Connectome/SynapseAnalysis/data/fragile_x/queries/' + \
        str(mouse_number) + 'ss_inhibitory_queries.json'
    da.writeJSONFile(fn, data)


def mouse_YFP_queries(mouse_number):
    """The generic list of queries expanded to include YFP for 2ss
    """

    listOfQueries = []
    punctum_size = 2

    for slice_span in range(1, 4):

        # Query 0
        preIF_str = str(mouse_number) + 'ss_Synap.tif'
        preIF = [preIF_str]
        preIF_z = [slice_span]
        postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
        postIF_str2 = str(mouse_number) + 'ss_YFP.tif'
        postIF = [postIF_str1, postIF_str2]
        postIF_z = [slice_span, slice_span]
        query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
                 'postIF_z': postIF_z, 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 1
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF_str2 = str(mouse_number) + 'ss_VGluT1.tif'
        preIF = [preIF_str1, preIF_str2]
        preIF_z = [slice_span, slice_span]
        postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
        postIF_str2 = str(mouse_number) + 'ss_YFP.tif'
        postIF = [postIF_str1, postIF_str2]
        postIF_z = [slice_span, slice_span]
        query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
                 'postIF_z': postIF_z, 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 2
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF_str2 = str(mouse_number) + 'ss_VGluT2.tif'
        preIF = [preIF_str1, preIF_str2]
        preIF_z = [slice_span, slice_span]
        postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
        postIF_str2 = str(mouse_number) + 'ss_YFP.tif'
        postIF = [postIF_str1, postIF_str2]
        postIF_z = [slice_span, slice_span]
        query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
                 'postIF_z': postIF_z, 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 3
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF_str2 = str(mouse_number) + 'ss_GAD.tif'
        preIF = [preIF_str1, preIF_str2]
        preIF_z = [slice_span, slice_span]
        postIF_str1 = str(mouse_number) + 'ss_Geph.tif'
        postIF_str2 = str(mouse_number) + 'ss_YFP.tif'
        postIF = [postIF_str1, postIF_str2]
        postIF_z = [slice_span, slice_span]
        query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
                 'postIF_z': postIF_z, 'punctumSize': punctum_size}
        listOfQueries.append(query)

    data = {'listOfQueries': listOfQueries}
    fn = '/Users/anish/Documents/Connectome/SynapseAnalysis/data/fragile_x/queries/' + \
        str(mouse_number) + 'ss_YFP_queries.json'
    da.writeJSONFile(fn, data)


def excitatory_astro_queries(mouse_number):
    """The query format expanded to include astrocytes for 2ss
    """
    listOfQueries = []
    punctum_size = 2

    for slice_span in range(1, 4):

        # Query 0
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF = [preIF_str1]
        preIF_z = [slice_span]
        postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
        postIF = [postIF_str1]
        postIF_z = [slice_span]
        glialIF_str = str(mouse_number) + 'ss_GS.tif'
        glialIF = [glialIF_str]
        glialIF_z = [slice_span]
        query = {'glialIF': glialIF, 'glialIF_z': glialIF_z, 'preIF': preIF,
                 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z,
                 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 1
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF_str2 = str(mouse_number) + 'ss_VGluT1.tif'
        preIF = [preIF_str1, preIF_str2]
        preIF_z = [slice_span, slice_span]
        postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
        postIF = [postIF_str1]
        postIF_z = [slice_span]
        glialIF_str = str(mouse_number) + 'ss_GS.tif'
        glialIF = [glialIF_str]
        glialIF_z = [slice_span]
        query = {'glialIF': glialIF, 'glialIF_z': glialIF_z, 'preIF': preIF,
                 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z,
                 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 2
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF_str2 = str(mouse_number) + 'ss_VGluT2.tif'
        preIF = [preIF_str1, preIF_str2]
        preIF_z = [slice_span, slice_span]
        postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
        postIF = [postIF_str1]
        postIF_z = [slice_span]
        glialIF_str = str(mouse_number) + 'ss_GS.tif'
        glialIF = [glialIF_str]
        glialIF_z = [slice_span]
        query = {'glialIF': glialIF, 'glialIF_z': glialIF_z, 'preIF': preIF,
                 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z,
                 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 2
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF_str2 = str(mouse_number) + 'ss_VGluT1.tif'
        preIF_str3 = str(mouse_number) + 'ss_VGluT2.tif'
        preIF = [preIF_str1, preIF_str2, preIF_str3]
        preIF_z = [slice_span, slice_span, slice_span]
        postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
        postIF = [postIF_str1]
        postIF_z = [slice_span]
        glialIF_str = str(mouse_number) + 'ss_GS.tif'
        glialIF = [glialIF_str]
        glialIF_z = [slice_span]
        query = {'glialIF': glialIF, 'glialIF_z': glialIF_z, 'preIF': preIF,
                 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z,
                 'punctumSize': punctum_size}
        listOfQueries.append(query)

    data = {'listOfQueries': listOfQueries}
    fn = '/Users/anish/Documents/Connectome/SynapseAnalysis/data/fragile_x/queries/' + \
        str(mouse_number) + 'ss_excitatory_astro_queries.json'
    da.writeJSONFile(fn, data)


def excitatory_astro_queries2(mouse_number):
    """GS is held at 1 slice
    """
    listOfQueries = []
    punctum_size = 2

    for slice_span in range(1, 4):

        # Query 0
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF = [preIF_str1]
        preIF_z = [slice_span]
        postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
        postIF = [postIF_str1]
        postIF_z = [slice_span]
        glialIF_str = str(mouse_number) + 'ss_GS.tif'
        glialIF = [glialIF_str]
        glialIF_z = [1]
        query = {'glialIF': glialIF, 'glialIF_z': glialIF_z, 'preIF': preIF,
                 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z,
                 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 1
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF_str2 = str(mouse_number) + 'ss_VGluT1.tif'
        preIF = [preIF_str1, preIF_str2]
        preIF_z = [slice_span, slice_span]
        postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
        postIF = [postIF_str1]
        postIF_z = [slice_span]
        glialIF_str = str(mouse_number) + 'ss_GS.tif'
        glialIF = [glialIF_str]
        glialIF_z = [1]
        query = {'glialIF': glialIF, 'glialIF_z': glialIF_z, 'preIF': preIF,
                 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z,
                 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 2
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF_str2 = str(mouse_number) + 'ss_VGluT2.tif'
        preIF = [preIF_str1, preIF_str2]
        preIF_z = [slice_span, slice_span]
        postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
        postIF = [postIF_str1]
        postIF_z = [slice_span]
        glialIF_str = str(mouse_number) + 'ss_GS.tif'
        glialIF = [glialIF_str]
        glialIF_z = [1]
        query = {'glialIF': glialIF, 'glialIF_z': glialIF_z, 'preIF': preIF,
                 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z,
                 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 3
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF_str2 = str(mouse_number) + 'ss_VGluT1.tif'
        preIF_str3 = str(mouse_number) + 'ss_VGluT2.tif'
        preIF = [preIF_str1, preIF_str2, preIF_str3]
        preIF_z = [slice_span, slice_span, slice_span]
        postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
        postIF = [postIF_str1]
        postIF_z = [slice_span]
        glialIF_str = str(mouse_number) + 'ss_GS.tif'
        glialIF = [glialIF_str]
        glialIF_z = [1]
        query = {'glialIF': glialIF, 'glialIF_z': glialIF_z, 'preIF': preIF,
                 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z,
                 'punctumSize': punctum_size}
        listOfQueries.append(query)

    data = {'listOfQueries': listOfQueries}
    fn = '/Users/anish/Documents/Connectome/SynapseAnalysis/data/fragile_x/queries/' + \
        str(mouse_number) + 'ss_excitatory_astro1slice_queries.json'
    da.writeJSONFile(fn, data)


def inhibitory_astro_queries(mouse_number):
    """The query format expanded to include astrocytes for 2ss
    """
    listOfQueries = []
    punctum_size = 2

    for slice_span in range(1, 4):

        # Query 3
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF_str2 = str(mouse_number) + 'ss_GAD.tif'
        preIF = [preIF_str1, preIF_str2]
        preIF_z = [slice_span, slice_span]
        postIF_str1 = str(mouse_number) + 'ss_Geph.tif'
        postIF = [postIF_str1]
        postIF_z = [slice_span]
        glialIF_str = str(mouse_number) + 'ss_GS.tif'
        glialIF = [glialIF_str]
        glialIF_z = [slice_span]
        query = {'glialIF': glialIF, 'glialIF_z': glialIF_z, 'preIF': preIF,
                 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z,
                 'punctumSize': punctum_size}
        listOfQueries.append(query)

    data = {'listOfQueries': listOfQueries}
    fn = '/Users/anish/Documents/Connectome/SynapseAnalysis/data/fragile_x/queries/' + \
        str(mouse_number) + 'ss_inhibitory_astro_queries.json'
    da.writeJSONFile(fn, data)


def mouse_astroYFP_queries(mouse_number):
    """The query format expanded to include astrocytes and YFP
    """
    listOfQueries = []
    punctum_size = 2

    for slice_span in range(1, 4):

        # Query 0
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF = [preIF_str1]
        preIF_z = [slice_span]
        postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
        postIF_str2 = str(mouse_number) + 'ss_YFP.tif'
        postIF = [postIF_str1, postIF_str2]
        postIF_z = [slice_span, slice_span]
        glialIF_str = str(mouse_number) + 'ss_GS.tif'
        glialIF = [glialIF_str]
        glialIF_z = [slice_span]
        query = {'glialIF': glialIF, 'glialIF_z': glialIF_z, 'preIF': preIF,
                 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z,
                 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 1
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF_str2 = str(mouse_number) + 'ss_VGluT1.tif'
        preIF = [preIF_str1, preIF_str2]
        preIF_z = [slice_span, slice_span]
        postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
        postIF_str2 = str(mouse_number) + 'ss_YFP.tif'
        postIF = [postIF_str1, postIF_str2]
        postIF_z = [slice_span, slice_span]
        glialIF_str = str(mouse_number) + 'ss_GS.tif'
        glialIF = [glialIF_str]
        glialIF_z = [slice_span]
        query = {'glialIF': glialIF, 'glialIF_z': glialIF_z, 'preIF': preIF,
                 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z,
                 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 2
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF_str2 = str(mouse_number) + 'ss_VGluT2.tif'
        preIF = [preIF_str1, preIF_str2]
        preIF_z = [slice_span, slice_span]
        postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
        postIF_str2 = str(mouse_number) + 'ss_YFP.tif'
        postIF = [postIF_str1, postIF_str2]
        postIF_z = [slice_span, slice_span]
        glialIF_str = str(mouse_number) + 'ss_GS.tif'
        glialIF = [glialIF_str]
        glialIF_z = [slice_span]
        query = {'glialIF': glialIF, 'glialIF_z': glialIF_z, 'preIF': preIF,
                 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z,
                 'punctumSize': punctum_size}
        listOfQueries.append(query)

        # Query 3
        preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
        preIF_str2 = str(mouse_number) + 'ss_GAD.tif'
        preIF = [preIF_str1, preIF_str2]
        preIF_z = [slice_span, slice_span]
        postIF_str1 = str(mouse_number) + 'ss_Geph.tif'
        postIF_str2 = str(mouse_number) + 'ss_YFP.tif'
        postIF = [postIF_str1, postIF_str2]
        postIF_z = [slice_span, slice_span]

        glialIF_str = str(mouse_number) + 'ss_GS.tif'
        glialIF = [glialIF_str]
        glialIF_z = [slice_span]
        query = {'glialIF': glialIF, 'glialIF_z': glialIF_z, 'preIF': preIF,
                 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z,
                 'punctumSize': punctum_size}
        listOfQueries.append(query)

    data = {'listOfQueries': listOfQueries}
    fn = '/Users/anish/Documents/Connectome/SynapseAnalysis/data/fragile_x/queries/' + \
        str(mouse_number) + 'ss_astroYFP_queries.json'
    da.writeJSONFile(fn, data)


def main():
    mice_list = [1, 2, 3, 4, 5, 6, 7, 22]

    # for n in mice_list:
    #     excitatory_queries(n)

    # for n in mice_list:
    #     inhibitory_queries(n)

    # for n in mice_list:
    #     excitatory_astro_queries(n)

    # for n in mice_list:
    #     inhibitory_astro_queries(n)

    # for n in mice_list:
    #     single_channel_queries(n)

    for n in mice_list:
        mouse_query_vglut2(n)


if __name__ == '__main__':
    main()
