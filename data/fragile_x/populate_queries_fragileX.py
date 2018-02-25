import os
import sys
import json 
from at_synapse_detection import dataAccess as da


def mouse_2_queries():
    listOfQueries = []
    punctum_size = 2

    preIF = ['2ss_Synap.tif']
    preIF_z = [2]
    postIF = ['2ss_PSD.tif']
    postIF_z = [2]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)


    preIF = ['2ss_Synap.tif', '2ss_VGluT1.tif']
    preIF_z = [2, 2]
    postIF = ['2ss_PSD.tif']
    postIF_z = [2]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)


    preIF = ['2ss_Synap.tif', '2ss_VGluT2.tif']
    preIF_z = [2, 2]
    postIF = ['2ss_PSD.tif']
    postIF_z = [2]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)


    preIF = ['2ss_Synap.tif', '2ss_VGluT1.tif', '2ss_VGluT2.tif']
    preIF_z = [2, 2, 2]
    postIF = ['2ss_PSD.tif']
    postIF_z = [2]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    preIF = ['2ss_VGAT.tif', '2ss_GAD.tif']
    preIF_z = [2, 2]
    postIF = ['2ss_Geph.tif']
    postIF_z = [1]

    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    data = {'listOfQueries': listOfQueries}
    fn = '/Users/anish/Documents/Connectome/SynapseAnalysis/data/fragile_x/2ss_queries.json'
    da.writeJSONFile(fn, data)

def mouse_3_queries():
    listOfQueries = []
    punctum_size = 2

    preIF = ['3ss_Synap.tif']
    preIF_z = [2]
    postIF = ['3ss_PSD.tif']
    postIF_z = [2]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)


    preIF = ['3ss_Synap.tif', '3ss_VGluT1.tif']
    preIF_z = [2, 2]
    postIF = ['3ss_PSD.tif']
    postIF_z = [2]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)


    preIF = ['3ss_Synap.tif', '3ss_VGluT2.tif']
    preIF_z = [2, 2]
    postIF = ['3ss_PSD.tif']
    postIF_z = [2]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)


    preIF = ['3ss_Synap.tif', '3ss_VGluT1.tif', '3ss_VGluT2.tif']
    preIF_z = [2, 2, 2]
    postIF = ['3ss_PSD.tif']
    postIF_z = [2]
    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    preIF = ['3ss_VGAT.tif', '3ss_GAD.tif']
    preIF_z = [2, 2]
    postIF = ['3ss_Geph.tif']
    postIF_z = [1]

    query = {'preIF': preIF, 'preIF_z': preIF_z, 'postIF': postIF, 'postIF_z': postIF_z, 'punctumSize': punctum_size}
    listOfQueries.append(query)

    data = {'listOfQueries': listOfQueries}
    fn = '/Users/anish/Documents/Connectome/SynapseAnalysis/data/fragile_x/3ss_queries.json'
    da.writeJSONFile(fn, data)


def main():
    mouse_2_queries()
    mouse_3_queries()


if __name__ == '__main__':
    main()