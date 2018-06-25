"""
Create the query files for exploring the FXS data
"""
import os
import sys
import json
from at_synapse_detection import dataAccess as da


def mouse_generic_queries(mouse_number):
    """ The generic list of queries plus Yi's interest in VGLUT+Gephyrin

    Parameters
    -------------
    mouse_number
    """
    listOfQueries = []
    punctum_size = 2

    # Query 0
    preIF_str = str(mouse_number) + 'ss_Synap.tif'
    preIF = [preIF_str]
    preIF_z = [3]
    postIF_str = str(mouse_number) + 'ss_PSD.tif'
    postIF = [postIF_str]
    postIF_z = [3]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
             'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    # Query 1
    preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
    preIF_str2 = str(mouse_number) + 'ss_VGluT1.tif'
    preIF = [preIF_str1, preIF_str2]
    preIF_z = [3, 3]
    postIF_str = str(mouse_number) + 'ss_PSD.tif'
    postIF = [postIF_str]
    postIF_z = [3]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
             'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    # Query 2
    preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
    preIF_str2 = str(mouse_number) + 'ss_VGluT2.tif'
    preIF = [preIF_str1, preIF_str2]
    preIF_z = [3, 3]
    postIF_str = str(mouse_number) + 'ss_PSD.tif'
    postIF = [postIF_str]
    postIF_z = [3]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
             'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    # Query 3
    preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
    preIF_str2 = str(mouse_number) + 'ss_VGluT1.tif'
    preIF_str3 = str(mouse_number) + 'ss_VGluT2.tif'
    preIF = [preIF_str1, preIF_str2, preIF_str3]
    preIF_z = [3, 3, 3]
    postIF_str = str(mouse_number) + 'ss_PSD.tif'
    postIF = [postIF_str]
    postIF_z = [3]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
             'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    # Query 4
    preIF_str1 = str(mouse_number) + 'ss_VGAT.tif'
    preIF_str2 = str(mouse_number) + 'ss_GAD.tif'
    preIF = [preIF_str1, preIF_str2]
    preIF_z = [3, 3]
    postIF_str1 = str(mouse_number) + 'ss_Geph.tif'
    postIF = [postIF_str1]
    postIF_z = [3]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
             'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    # NEW GEPHYRIN QUERIES FROM YI
    # Query 5
    preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
    preIF_str2 = str(mouse_number) + 'ss_VGluT1.tif'
    preIF = [preIF_str1, preIF_str2]
    preIF_z = [3, 3]
    postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
    postIF_str2 = str(mouse_number) + 'ss_Geph.tif'
    postIF = [postIF_str1, postIF_str2]
    postIF_z = [3, 3]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
             'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    # Query 6
    preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
    preIF_str2 = str(mouse_number) + 'ss_VGluT2.tif'
    preIF = [preIF_str1, preIF_str2]
    preIF_z = [3, 3]
    postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
    postIF_str2 = str(mouse_number) + 'ss_Geph.tif'
    postIF = [postIF_str1, postIF_str2]
    postIF_z = [3, 3]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
             'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    data = {'listOfQueries': listOfQueries}
    fn = '/Users/anish/Documents/Connectome/SynapseAnalysis/data/fragile_x/' + \
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
    fn = '/Users/anish/Documents/Connectome/SynapseAnalysis/data/fragile_x/' + \
        str(mouse_number) + 'ss_inhibitory_queries.json'
    da.writeJSONFile(fn, data)


def mouse_YFP_queries(mouse_number):
    """The generic list of queries expanded to include YFP for 2ss
    """

    listOfQueries = []
    punctum_size = 2

    # Query 0
    preIF_str = str(mouse_number) + 'ss_Synap.tif'
    preIF = [preIF_str]
    preIF_z = [2]
    postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
    postIF_str2 = str(mouse_number) + 'ss_YFP.tif'
    postIF = [postIF_str1, postIF_str2]
    postIF_z = [2, 2]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
             'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    # Query 1
    preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
    preIF_str2 = str(mouse_number) + 'ss_VGluT1.tif'
    preIF = [preIF_str1, preIF_str2]
    preIF_z = [2, 2]
    postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
    postIF_str2 = str(mouse_number) + 'ss_YFP.tif'
    postIF = [postIF_str1, postIF_str2]
    postIF_z = [2, 2]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
             'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    # Query 2
    preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
    preIF_str2 = str(mouse_number) + 'ss_VGluT2.tif'
    preIF = [preIF_str1, preIF_str2]
    preIF_z = [2, 2]
    postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
    postIF_str2 = str(mouse_number) + 'ss_YFP.tif'
    postIF = [postIF_str1, postIF_str2]
    postIF_z = [2, 2]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
             'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    # Query 3
    preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
    preIF_str2 = str(mouse_number) + 'ss_VGluT1.tif'
    preIF_str3 = str(mouse_number) + 'ss_VGluT2.tif'
    preIF = [preIF_str1, preIF_str2, preIF_str3]
    preIF_z = [2, 2, 2]
    postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
    postIF_str2 = str(mouse_number) + 'ss_YFP.tif'
    postIF = [postIF_str1, postIF_str2]
    postIF_z = [2, 2]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
             'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    # Query 4
    preIF_str1 = str(mouse_number) + 'ss_VGAT.tif'
    preIF_str2 = str(mouse_number) + 'ss_GAD.tif'
    preIF = [preIF_str1, preIF_str2]
    preIF_z = [2, 2]
    postIF_str1 = str(mouse_number) + 'ss_Geph.tif'
    postIF_str2 = str(mouse_number) + 'ss_YFP.tif'
    postIF = [postIF_str1, postIF_str2]
    postIF_z = [1, 2]

    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF,
             'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    data = {'listOfQueries': listOfQueries}
    fn = '/Users/anish/Documents/Connectome/SynapseAnalysis/data/fragile_x/' + \
        str(mouse_number) + 'ss_YFP_queries.json'
    da.writeJSONFile(fn, data)


def mouse_astro_queries(mouse_number):
    """The query format expanded to include astrocytes for 2ss
    """
    listOfQueries = []
    punctum_size = 2

    # Query 0
    preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
    preIF = [preIF_str1]
    preIF_z = [2]
    postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
    postIF = [postIF_str1]
    postIF_z = [2]
    glialIF_str = str(mouse_number) + 'ss_GS.tif'
    glialIF = [glialIF_str]
    glialIF_z = [2]
    query = {'glialIF': glialIF, 'glialIF_z': glialIF_z, 'preIF': preIF,
             'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z,
             'punctumSize': punctum_size}
    listOfQueries.append(query)

    # Query 1
    preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
    preIF_str2 = str(mouse_number) + 'ss_VGluT1.tif'
    preIF = [preIF_str1, preIF_str2]
    preIF_z = [2, 2]
    postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
    postIF = [postIF_str1]
    postIF_z = [2]
    glialIF_str = str(mouse_number) + 'ss_GS.tif'
    glialIF = [glialIF_str]
    glialIF_z = [2]
    query = {'glialIF': glialIF, 'glialIF_z': glialIF_z, 'preIF': preIF,
             'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z,
             'punctumSize': punctum_size}
    listOfQueries.append(query)

    # Query 2
    preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
    preIF_str2 = str(mouse_number) + 'ss_VGluT2.tif'
    preIF = [preIF_str1, preIF_str2]
    preIF_z = [2, 2]
    postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
    postIF = [postIF_str1]
    postIF_z = [2]
    glialIF_str = str(mouse_number) + 'ss_GS.tif'
    glialIF = [glialIF_str]
    glialIF_z = [2]
    query = {'glialIF': glialIF, 'glialIF_z': glialIF_z, 'preIF': preIF,
             'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z,
             'punctumSize': punctum_size}
    listOfQueries.append(query)

    # Query 3
    preIF_str1 = str(mouse_number) + 'ss_Synap.tif'
    preIF_str2 = str(mouse_number) + 'ss_VGluT1.tif'
    preIF_str3 = str(mouse_number) + 'ss_VGluT2.tif'
    preIF = [preIF_str1, preIF_str2, preIF_str3]
    preIF_z = [2, 2, 2]
    postIF_str1 = str(mouse_number) + 'ss_PSD.tif'
    postIF = [postIF_str1]
    postIF_z = [2]
    glialIF_str = str(mouse_number) + 'ss_GS.tif'
    glialIF = [glialIF_str]
    glialIF_z = [2]
    query = {'glialIF': glialIF, 'glialIF_z': glialIF_z, 'preIF': preIF,
             'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z,
             'punctumSize': punctum_size}
    listOfQueries.append(query)

    # Query 4
    preIF_str1 = str(mouse_number) + 'ss_VGAT.tif'
    preIF_str2 = str(mouse_number) + 'ss_GAD.tif'
    preIF = [preIF_str1, preIF_str2]
    preIF_z = [2, 2]
    postIF_str1 = str(mouse_number) + 'ss_Geph.tif'
    postIF = [postIF_str1]
    postIF_z = [1]
    glialIF_str = str(mouse_number) + 'ss_GS.tif'
    glialIF = [glialIF_str]
    glialIF_z = [2]
    query = {'glialIF': glialIF, 'glialIF_z': glialIF_z, 'preIF': preIF,
             'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z,
             'punctumSize': punctum_size}
    listOfQueries.append(query)

    data = {'listOfQueries': listOfQueries}
    fn = '/Users/anish/Documents/Connectome/SynapseAnalysis/data/fragile_x/' + \
        str(mouse_number) + 'ss_astro_queries.json'
    da.writeJSONFile(fn, data)


def main():

    # mouse_generic_queries(2)
    # mouse_YFP_queries(2)
    # mouse_astro_queries(2)

    # mouse_generic_queries(3)
    # mouse_YFP_queries(3)
    # mouse_astro_queries(3)

    # mouse_generic_queries(4)
    # mouse_YFP_queries(4)
    # mouse_astro_queries(4)

    # mouse_generic_queries(6)
    # mouse_YFP_queries(6)
    # mouse_astro_queries(6)

    # mouse_generic_queries(5)
    # mouse_YFP_queries(5)
    # mouse_astro_queries(5)

    # mouse_generic_queries(7)
    # mouse_YFP_queries(7)
    # mouse_astro_queries(7)

    for n in range(2, 8):
        mouse_inhibitory_queries(n)


if __name__ == '__main__':
    main()
