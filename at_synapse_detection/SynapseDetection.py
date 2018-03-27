import scipy
import csv
import json
import os
import math
import numpy as np
from scipy.stats import norm
from scipy.stats import gamma
from scipy import signal
import scipy.ndimage as ndimage
from at_synapse_detection import synaptogram
from at_synapse_detection import dataAccess as da

# def calculateGammaParams(data):
#     mean = np.mean(data)
#     std = np.std(data)
#     shape = (mean/std)**2
#     scale = (std**2)/mean
#     return (shape, 0, scale)


# def getProbMap_gamma(data):
#     """
#     Returns probability map of input image
#     Parameters
#     ----------
#     data : 3D numpy - input volume

#     Returns
#     ----------
#     data : 3D numpy
#         output volume with values scaled between 0 to 1
#     """

#     if len(data.shape) == 2:
#         data = scipy.stats.norm.cdf(data, np.mean(data), np.std(data))
#     else:
#         for zInd in range(0, data.shape[2]):
#             # Calculate foreground probabilities
#             eshape, eloc, escale = calculateGammaParams(data[:, :, zInd].flatten())
#             output = gamma.cdf(data[:, :, zInd], eshape, eloc, escale)
#             data[:, :, zInd] = output
#     print('Prob Calculated')
#     return data


def getProbMap_rayleigh(data):
    """
    Returns probability map of input image
    Parameters
    ----------
    data : 3D numpy - input volume

    Returns
    ----------
    data : 3D numpy
        output volume with values scaled between 0 to 1
    """

    for zInd in range(0, data.shape[2]):

        # The maximum likelihood estimate has a simple form
        phat = np.sqrt(0.5 * np.mean(np.power(data[:, :, zInd], 2)))
        output = 1 - np.exp(-1*np.power(data[:, :, zInd], 2) / (2*np.power(phat, 2))) 

        # Calculate foreground probabilities
        data[:, :, zInd] = output

    return data


def getProbMap(data):
    """
    Returns probability map of input image
    Parameters
    ----------
    data : 3D numpy - input volume

    Returns
    ----------
    data : 3D numpy
        output volume with values scaled between 0 to 1
    """

    if len(data.shape) == 2:
        data = scipy.stats.norm.cdf(data, np.mean(data), np.std(data))
    else:
        for zInd in range(0, data.shape[2]):
            # Calculate foreground probabilities
            data[:, :, zInd] = scipy.stats.norm.cdf(
                data[:, :, zInd], np.mean(data[:, :, zInd]), np.std(data[:, :, zInd]))
    return data


def convolveVolume(vol, kernelLength):
    """
    Returns convolved volume
    Parameters
    ----------
    vol : 3D numpy volume
    kernelLength : ind - minimum blob size

    Returns
    ----------
    vol : 3D numpy volume
    """
    vol = np.log(vol)

    kernel = np.ones([kernelLength, kernelLength])

    for n in range(0, vol.shape[2]):
        img = vol[:, :, n]

        if (kernelLength % 2 == 0):
            img = signal.convolve2d(img, kernel, 'full')

            rstartInd = int(kernelLength / 2)
            rendInd = img.shape[0] - kernelLength / 2 + 1
            rendInd = int(rendInd)

            # Python3 division is converted to float
            cstartInd = int(kernelLength / 2)
            cendInd = img.shape[1] - kernelLength / 2 + 1
            cendInd = int(cendInd)

            Csame = img[rstartInd:rendInd, cstartInd:cendInd]
            vol[:, :, n] = Csame

        else:
            img = signal.convolve2d(img, kernel, 'same')
            vol[:, :, n] = img

    kernelsize = np.prod(kernel.shape)
    vol = np.divide(vol, kernelsize)
    vol = np.exp(vol)

    return vol


def computeFactor(vol, numslices):
    """
    Returns convolved volume
    Parameters
    ----------
    vol : 3D numpy volume
    numslices: int - number of slices to span
        note from anish: numslices can only be 2 or 3.
        todo - add more slices
    Returns
    ----------
    factorVol : 3D numpy volume
    """

    factorVol = np.ones(vol.shape)

    if (numslices == 1):
        return factorVol

    for n in range(0, vol.shape[2]):

        # Edge cases
        # First Slice
        #print(vol.shape)
        if n == 0:
            #print(n)
            diff = np.exp(-1 *
                          (np.power((vol[:, :, n] - vol[:, :, n + 1]), 2)))

        # Last slice
        elif n == (vol.shape[2] - 1):
            diff = np.exp(-1 *
                          (np.power((vol[:, :, n] - vol[:, :, n - 1]), 2)))
        # Middle slices
        else:
            if (numslices == 3):
                diff = np.exp((-1 * (np.power((vol[:, :, n] - vol[:, :, n + 1]), 2) +
                                     np.power((vol[:, :, n] - vol[:, :, n - 1]), 2))))
            elif (numslices == 2):
                diff = np.exp(-1 *
                              (np.power((vol[:, :, n] - vol[:, :, n + 1]), 2)))

        factorVol[:, :, n] = diff

    return factorVol


# def computeFactor_grid(vol, numslices):
#     """
#     Returns convolved volume
#     Parameters
#     ----------
#     vol : 3D numpy volume
#     numslices: int - number of slices to span
#         note from anish: numslices can only be 2 or 3.
#         todo - add more slices
#     Returns
#     ----------
#     factorVol : 3D numpy volume
#     """

#     factorVol = np.ones(vol.shape)
#     max_filt_vol = np.ones(vol.shape)

#     if (numslices == 1):
#         return factorVol

#     for n in range(0, vol.shape[2]): 
#         max_filt_vol[:, :, n] = scipy.ndimage.filters.maximum_filter(vol[:, :, n], size=(3, 3))


#     for n in range(0, vol.shape[2]):

#         # Edge cases
#         # First Slice
#         #print(vol.shape)
#         if n == 0:
#             #print(n)
#             diff = np.exp(-1 *
#                           (np.power((vol[:, :, n] - max_filt_vol[:, :, n + 1]), 2)))

#         # Last slice
#         elif n == (vol.shape[2] - 1):
#             diff = np.exp(-1 *
#                           (np.power((vol[:, :, n] - max_filt_vol[:, :, n - 1]), 2)))
#         # Middle slices
#         else:
#             if (numslices == 3):
#                 diff = np.exp((-1 * (np.power((vol[:, :, n] - max_filt_vol[:, :, n + 1]), 2) +
#                                      np.power((vol[:, :, n] - max_filt_vol[:, :, n - 1]), 2))))
#             elif (numslices == 2):
#                 diff = np.exp(-1 *
#                               (np.power((vol[:, :, n] - max_filt_vol[:, :, n + 1]), 2)))

#         factorVol[:, :, n] = diff

#     return factorVol



def loadQueriesJSON(fileName):
    """
    Load query file (in JSON format).

    Parameters
    ----------
    fileName : str - location of file

    Returns
    ----------
    listOfQueries : list of queries
    """

    data = json.load(open(fileName))
    listOfQueries = data['listOfQueries']

    return listOfQueries


def createLookupTables(inputVol):
    """
    Create Look Up tables

    Parameters
    ----------
    inputVol : 3D Numpy Array

    Returns
    ----------
    inputVol : 3D Numpy Array

    """
    #print(len(inputVol))
    for volItr in range(0, len(inputVol)):
        for z in range(0, inputVol[0].shape[2]):
            inputVol[volItr][:, :, z] = np.cumsum(
                np.cumsum(inputVol[volItr][:, :, z], 1), 0)

    return inputVol


def searchAdjacentChannel(adjacentVolList, search_win, cInd, rInd, zInd):
    """
    Search adjacent channels for data, with respect to a center point

    Parameters
    ----------
    adjaventVolList : list of numpy 3D volumes
    search_win : ind - search window
    cInd : ind
    rInd : ind
    zInd : ind

    Returns
    ----------
    result : double - max signal in the 3D search region

    """
    searchgrid = np.zeros([27, len(adjacentVolList)])
    ind = 0

    if (zInd == 0):
        zrange = [0, 1]
    elif (zInd == (adjacentVolList[0].shape[2] - 1)):
        zrange = range(
            (adjacentVolList[0].shape[2] - 2), adjacentVolList[0].shape[2])
    else:
        zrange = range(zInd - 1, zInd + 2)

    for zItr in zrange:
        rstart = rInd - 1.5 * search_win

        for row in range(0, 3):
            cstart = cInd - 1.5 * search_win
            for col in range(0, 3):
                for volItr in range(0, len(adjacentVolList)):

                    sumIF1 = \
                        adjacentVolList[volItr][int(rstart + search_win), int(cstart + search_win), zItr] + \
                        adjacentVolList[volItr][int(rstart), int(cstart), zItr] - \
                        adjacentVolList[volItr][int(rstart + search_win), int(cstart), zItr] - \
                        adjacentVolList[volItr][int(rstart), int(
                            cstart + search_win), zItr]

                    searchgrid[ind, volItr] = sumIF1 / \
                        (search_win * search_win)

                ind = ind + 1

                cstart = cstart + search_win
            rstart = rstart + search_win

    # Find the max of the first presynaptic channel.
    # This insures the adjacent sections colocalize.
    max_ind = np.argmax(searchgrid[:, 0])
    result = np.prod(searchgrid[max_ind, :])
    return result


def searchColocalizeChannel(baseVolList, search_win, cInd, rInd, zInd):
    """
    Search for markers which colocalize

    Parameters
    ----------
    baseVolList : list of volumes who's markers are supposed to colocalize with each other
    search_win : ind - search window
    cInd : ind
    rInd : ind
    zInd : ind

    Returns
    ----------
    output : double - product of colocalization across channels

    """
    localizationGrid = np.zeros(len(baseVolList) - 1)
    rstart = rInd - search_win / 2
    cstart = cInd - search_win / 2

    for volItr in range(1, len(baseVolList)):
        sumIF1 = baseVolList[volItr][int(rstart + search_win), int(cstart + search_win), int(zInd)] + \
            baseVolList[volItr][int(rstart), int(cstart), int(zInd)] - baseVolList[volItr][int(rstart + search_win), int(cstart), int(zInd)] - \
            baseVolList[volItr][int(rstart), int(
                cstart + search_win), int(zInd)]

        localizationGrid[volItr - 1] = sumIF1 / (search_win * search_win)

    output = np.prod(localizationGrid)
    return output


def combinePrePostVolumes(baseVolList, adjacentVolList, edge_win, search_win):
    """
    Combines Volumes
    Parameters
    ----------
    baseVol : 3D numpy array
    adjacentVolList : Adjacent volumes list. pass empty array if no
                      adjacent synaptic volumes are present in the dataset
    baseThresh : float - minimum probability value to consider
    edge_win : int - edge to ignore
    search_win - search_win must be even

    Returns
    ----------
    outputVol : 3D Numpy Array - Final Probability Map
    """
    # Allocate memory
    outputVol = np.zeros(baseVolList[0].shape)

    # If there are multiple volumes associated with the same synaptic side
    if len(baseVolList) > 1:
        baseVolList[1:] = createLookupTables(baseVolList[1:])

    # Create lookup tables
    if len(adjacentVolList) > 0:
        adjacentVolList = createLookupTables(adjacentVolList)

    #print('starting to loop through each slice')
    baseVol = baseVolList[0]
    rStartEdge = edge_win
    rEndEdge = baseVol.shape[0] - edge_win
    cStartEdge = edge_win
    cEndEdge = baseVol.shape[1] - edge_win

    # For each z slice
    for zInd in range(0, baseVol.shape[2]):
        print("starting z ind: " + str(zInd))

        for rInd in range(rStartEdge, rEndEdge):
            for cInd in range(cStartEdge, cEndEdge):

                if (baseVol[rInd, cInd, zInd] < 0.5):
                    continue

                if len(adjacentVolList) > 0:
                    adjResult = searchAdjacentChannel(adjacentVolList, search_win, cInd, rInd, zInd)
                    outputVol[rInd, cInd, zInd] = baseVol[rInd,cInd, zInd] * adjResult

                    if len(baseVolList) > 1:
                        coresult = searchColocalizeChannel(baseVolList, search_win, cInd, rInd, zInd)
                        outputVol[rInd, cInd, zInd] = baseVol[rInd,cInd, zInd] * coresult * adjResult
                else:
                    coresult = searchColocalizeChannel(baseVolList, search_win, cInd, rInd, zInd)
                    outputVol[rInd, cInd, zInd] = baseVol[rInd,cInd, zInd] * coresult

    return outputVol

def combinePrePostVolumes_astro(baseVolList, adjacentVolList, glialvolumes, edge_win, search_win):
    """
    Combines Volumes
    Parameters
    ----------
    baseVol : 3D numpy array
    adjacentVolList : Adjacent volumes list. pass empty array if no
                      adjacent synaptic volumes are present in the dataset
    baseThresh : float - minimum probability value to consider
    edge_win : int - edge to ignore
    search_win - search_win must be even

    Returns
    ----------
    outputVol : 3D Numpy Array - Final Probability Map
    """
    # Allocate memory
    outputVol = np.zeros(baseVolList[0].shape)

    # If there are multiple volumes associated with the same synaptic side
    if len(baseVolList) > 1:
        baseVolList[1:] = createLookupTables(baseVolList[1:])

    # Create lookup tables
    if len(adjacentVolList) > 0:
        adjacentVolList = createLookupTables(adjacentVolList)
        glialvolumes = createLookupTables(glialvolumes)

    #print('starting to loop through each slice')
    baseVol = baseVolList[0]
    rStartEdge = edge_win
    rEndEdge = baseVol.shape[0] - edge_win
    cStartEdge = edge_win
    cEndEdge = baseVol.shape[1] - edge_win

    # For each z slice
    for zInd in range(0, baseVol.shape[2]):
        print("starting z ind: " + str(zInd))

        # if zInd > 2: 
        #     return outputVol

            
        for rInd in range(rStartEdge, rEndEdge):
            for cInd in range(cStartEdge, cEndEdge):

                if (baseVol[rInd, cInd, zInd] < 0.5):
                    continue

                if len(adjacentVolList) > 0:
                    adjResult = searchAdjacentChannel(adjacentVolList, search_win, cInd, rInd, zInd)
                    adjResult2 = searchAdjacentChannel(glialvolumes, search_win, cInd, rInd, zInd)
                    #outputVol[rInd, cInd, zInd] = adjResult2
                    outputVol[rInd, cInd, zInd] = baseVol[rInd,cInd, zInd] * adjResult * adjResult2


                    if len(baseVolList) > 1:
                        coresult = searchColocalizeChannel(baseVolList, search_win, cInd, rInd, zInd)
                        #outputVol[rInd, cInd, zInd] = baseVol[rInd,cInd, zInd] * coresult * adjResult * adjResult2
                        
                else:
                    coresult = searchColocalizeChannel(baseVolList, search_win, cInd, rInd, zInd)
                    outputVol[rInd, cInd, zInd] = baseVol[rInd,cInd, zInd] * coresult

    return outputVol



def getSynapseDetections(synapticVolumes, query, blobsize=2, edge_win=3):
    """
    This function calls the functions needed to run probabilistic synapse detection

    Parameters
    ----------
    synapticVolumes : dict
        has two keys (presynaptic,postsynaptic) which contain lists of 3D numpy arrays
    query : dict
        contains the minumum slice information for each channel
    blobsize : int
        Minimum 2D Blob Size (default 2)
    edge_win: int
        Edge window (default is 1.5*blobsize)


    Returns
    ----------
    resultVol : 3D numpy array - final probability map
    """

    #Check to see if user supplied blobsize
    if 'punctumSize' in query.keys():
        blobsize = query['punctumSize']
        edge_win = int(np.ceil(blobsize * 1.5))

    # Data
    presynapticVolumes = synapticVolumes['presynaptic']
    postsynapticVolumes = synapticVolumes['postsynaptic']

    # Number of slices each blob should span
    preIF_z = query['preIF_z']
    postIF_z = query['postIF_z']

    for n in range(0, len(presynapticVolumes)):

        presynapticVolumes[n] = getProbMap(presynapticVolumes[n])  # Step 1
        presynapticVolumes[n] = convolveVolume(
            presynapticVolumes[n], blobsize)  # Step 2

        if preIF_z[n] > 1:
            factorVol = computeFactor(
                presynapticVolumes[n], int(preIF_z[n]))  # Step 3
            presynapticVolumes[n] = presynapticVolumes[n] * factorVol

    for n in range(0, len(postsynapticVolumes)):

        postsynapticVolumes[n] = getProbMap(postsynapticVolumes[n])  # Step 1
        postsynapticVolumes[n] = convolveVolume(
            postsynapticVolumes[n], blobsize)  # Step 2

        if postIF_z[n] > 1:
            factorVol = computeFactor(
                postsynapticVolumes[n], int(postIF_z[n]))  # Step 3
            postsynapticVolumes[n] = postsynapticVolumes[n] * factorVol

    if len(postsynapticVolumes) == 0:
        resultVol = combinePrePostVolumes(
            presynapticVolumes, postsynapticVolumes, edge_win, blobsize)
    else:
        resultVol = combinePrePostVolumes(
            postsynapticVolumes, presynapticVolumes, edge_win, blobsize)

    return resultVol

def getSynapseDetections_astro(synapticVolumes, query, blobsize=2, edge_win=3):
    """
    This function calls the functions needed to run probabilistic synapse detection

    Parameters
    ----------
    synapticVolumes : dict
        has two keys (presynaptic,postsynaptic) which contain lists of 3D numpy arrays
    query : dict
        contains the minumum slice information for each channel
    blobsize : int
        Minimum 2D Blob Size (default 2)
    edge_win: int
        Edge window (default is 1.5*blobsize)


    Returns
    ----------
    resultVol : 3D numpy array - final probability map
    """

    #Check to see if user supplied blobsize
    if 'punctumSize' in query.keys():
        blobsize = query['punctumSize']
        edge_win = int(np.ceil(blobsize * 1.5))

    # Data
    presynapticVolumes = synapticVolumes['presynaptic']
    postsynapticVolumes = synapticVolumes['postsynaptic']
    glialVolumes = synapticVolumes['glialvolumes']

    # Number of slices each blob should span
    preIF_z = query['preIF_z']
    postIF_z = query['postIF_z']
    glialIF_z = query['glialIF_z']

    for n in range(0, len(presynapticVolumes)):

        presynapticVolumes[n] = getProbMap(presynapticVolumes[n])  # Step 1
        presynapticVolumes[n] = convolveVolume(
            presynapticVolumes[n], blobsize)  # Step 2

        if preIF_z[n] > 1:
            factorVol = computeFactor(
                presynapticVolumes[n], int(preIF_z[n]))  # Step 3
            presynapticVolumes[n] = presynapticVolumes[n] * factorVol

    for n in range(0, len(postsynapticVolumes)):

        postsynapticVolumes[n] = getProbMap(postsynapticVolumes[n])  # Step 1
        postsynapticVolumes[n] = convolveVolume(
            postsynapticVolumes[n], blobsize)  # Step 2

        if postIF_z[n] > 1:
            factorVol = computeFactor(
                postsynapticVolumes[n], int(postIF_z[n]))  # Step 3
            postsynapticVolumes[n] = postsynapticVolumes[n] * factorVol

    for n in range(0, len(glialVolumes)):

        glialVolumes[n] = getProbMap(glialVolumes[n])  # Step 1
        glialVolumes[n] = convolveVolume(
            glialVolumes[n], blobsize)  # Step 2

        if glialIF_z[n] > 1:
            factorVol = computeFactor(
                glialVolumes[n], int(glialIF_z[n]))  # Step 3
            glialVolumes[n] = glialVolumes[n] * factorVol


    if len(postsynapticVolumes) == 0:
        resultVol = combinePrePostVolumes_astro(
            presynapticVolumes, postsynapticVolumes, glialVolumes, edge_win, blobsize)
    else:
        resultVol = combinePrePostVolumes_astro(
            postsynapticVolumes, presynapticVolumes, glialVolumes, edge_win, blobsize)

    return resultVol


def loadMetadata(fn):
    """
    Load Metadata JSON File
    Parameters:
    -------------
    fn : str - filename

    Returns:
    -------------
    data : dict
    """
    data = json.load(open(fn))
    return data


def saveresultvol(vol, datalocation, filename, n):
    """
    save result volume
    Parameters
    -------------
    vol : numpy 3D array
    datalocation : str
    filename : str
    n : int
    """
    if not os.path.isdir(datalocation):
        os.makedirs(datalocation)

    fn = os.path.join(datalocation, filename)
    fn = fn + str(n) + '.npy'
    np.save(fn, vol)
