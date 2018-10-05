"""
Create the query files for exploring the FXS data
"""
import os
import sys
import json
from at_synapse_detection import dataAccess as da


def mouse_generic_queries(mouse_number):
    """ The generic list of queries

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
        str(mouse_number) + 'ss_queries.json'
    da.writeJSONFile(fn, data)


def mouse_inhibitory_queries(mouse_number):
    """ Inhibitory queries at different sizes

    Parameters
    -------------
    mouse_number
    """
    listOfQueries = []
    punctum_size = 2

    # Query - 1 slice
    preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
    preIF_str2 = str(mouse_number) + 'ss_GAD.tif'
    preIF = [preIF_str1, preIF_str2]
    preIF_z = [1, 1]
    postIF_str1 = str(mouse_number) + 'ss_Geph.tif'
    postIF = [postIF_str1]
    postIF_z = [1]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
             'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    # Query
    preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
    preIF_str2 = str(mouse_number) + 'ss_GAD.tif'
    preIF = [preIF_str1, preIF_str2]
    preIF_z = [2, 2]
    postIF_str1 = str(mouse_number) + 'ss_Geph.tif'
    postIF = [postIF_str1]
    postIF_z = [1]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
             'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    # Query
    preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
    preIF_str2 = str(mouse_number) + 'ss_GAD.tif'
    preIF = [preIF_str1, preIF_str2]
    preIF_z = [2, 2]
    postIF_str1 = str(mouse_number) + 'ss_Geph.tif'
    postIF = [postIF_str1]
    postIF_z = [2]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
             'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    # Query
    preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
    preIF_str2 = str(mouse_number) + 'ss_GAD.tif'
    preIF = [preIF_str1, preIF_str2]
    preIF_z = [3, 3]
    postIF_str1 = str(mouse_number) + 'ss_Geph.tif'
    postIF = [postIF_str1]
    postIF_z = [3]
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


def mouse_astro_queries(mouse_number):
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
        str(mouse_number) + 'ss_astro_queries.json'
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

    mouse_generic_queries(22)
    mouse_YFP_queries(22)
    mouse_astro_queries(22)
    mouse_astroYFP_queries(22)

    for n in range(1, 8):
        mouse_YFP_queries(n)

    for n in range(1, 8):
        mouse_astro_queries(n)

    for n in range(1, 8):
        mouse_astroYFP_queries(n)

    for n in range(1, 8):
        mouse_generic_queries(n)


if __name__ == '__main__':
    main()
