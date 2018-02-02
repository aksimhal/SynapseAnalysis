import scipy
import csv
import json
import os
import math
import numpy as np
from scipy.stats import norm
from scipy import signal
import scipy.ndimage as ndimage
from at_synapse_detection import synaptogram
from at_synapse_detection import dataAccess as da


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
            data[:, :, zInd] = scipy.stats.norm.cdf(data[:, :, zInd], np.mean(data[:, :, zInd]), np.std(data[:, :, zInd]))
    return data

def getProbMap_MW(data, chname, win=30, stepsize=1):
    """
    Returns probability map of input image.  Uses a moving window for background/foreground seperation
    Saves probability map to file; if the file already exists, it reloads it and returns it

    Issue: Current output location is hard coded

    Parameters
    ----------
    data : 3D numpy - input volume
    chname : str - channel name
    win : int - window size (default = 30)
    stepsize : int - moving window step size (default = 1)

    Returns
    ----------
    data : 3D numpy
        output volume with values scaled between 0 to 1
    """

    #test to see if data exists # FIX filepath
    outputlocation = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/collman17/Site3Align2Stacks/'
    fn = chname + '_probvol.npy'
    fn = os.path.join(outputlocation, fn)

    doesfileexist = os.path.exists(fn)

    if doesfileexist:
        outputvol = np.load(fn)
        print("loaded file")
        return outputvol
    else:
        print("compute prob file")

        outputvol = np.zeros(data.shape)
        for zInd in range(0, data.shape[2]):
            img = data[:, :, zInd]

            print("Calculating probability slice: ", zInd)
            imgsize = img.shape
            outputimg = np.zeros(imgsize)

            startRow = 0
            endRow = 0
            oldEndRow = 0

            exitRowLoop = False
            for rowstep in range(0, int(np.ceil(imgsize[0]/stepsize))):
                startCol = 0
                endCol = 0
                oldEndCol = 0

                if exitRowLoop:
                    break

                if ((startRow + win) < imgsize[0]):
                    endRow = startRow + win
                else:
                    endRow = imgsize[0]
                    exitRowLoop = True

                exitColLoop = False
                for colstep in range(0, int(np.ceil(imgsize[1]/stepsize))):

                    if exitColLoop:
                        break

                    if ((startCol + win) < imgsize[1]):
                         endCol = startCol + win
                    else:
                        endCol = imgsize[1]
                        exitColLoop = True


                    cutout = img[startRow:endRow, startCol:endCol]
                    cutout = scipy.stats.norm.cdf(cutout, np.mean(cutout), np.std(cutout))

                    if oldEndRow != 0 and oldEndCol != 0:

                        priordata = outputimg[startRow:oldEndRow, startCol:oldEndCol]
                        meancutout = np.mean([priordata, cutout[0:-(endRow-oldEndRow), 0:-(endCol-oldEndCol)]], 0)
                        cutout[0:-(endRow-oldEndRow), 0:-(endCol-oldEndCol)] = meancutout

                    outputimg[startRow:endRow, startCol:endCol] = cutout
                    oldEndCol = endCol
                    startCol = startCol + stepsize

                oldEndRow = endRow
                startRow = startRow + stepsize

            outputvol[:, :, zInd] = outputimg
        np.save(fn, outputvol)

    return outputvol


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

            rstartInd = int(kernelLength/2)
            rendInd = img.shape[0] - kernelLength/2 + 1
            rendInd = int(rendInd)

            cstartInd = int(kernelLength/2) # Python3 division is converted to float
            cendInd = img.shape[1] - kernelLength/2 + 1
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
        if n == 1:
            diff = np.exp(-1 * (np.power((vol[:, :, n] - vol[:, :, n + 1]), 2)))

        # Last slice
        elif n == (vol.shape[2] - 1):
            diff = np.exp(-1 * (np.power((vol[:, :, n] - vol[:, :, n - 1]), 2)))
        # Middle slices
        else:
            if (numslices == 3):
                diff = np.exp((-1 * (np.power((vol[:, :, n] - vol[:, :, n + 1]), 2) +
                                     np.power((vol[:, :, n] - vol[:, :, n - 1]), 2))))
            elif (numslices == 2):
                diff = np.exp(-1 * (np.power((vol[:, :, n] - vol[:, :, n + 1]), 2)))

        factorVol[:, :, n] = diff

    return factorVol


def loadQueriesCSV(fileName):
    """
    Create query object from csv
    Query format is:
    "
    presynapticvol1, slicespan, presynapticvol2, slicespan
    postsynapticvol1, slicespan, postsynapticvol2, slicespan
    ,,,,
    presynapticvol1, slicespan, presynapticvol2, slicespan,
    NULL,,,,
    "
    If there is no adjacent signal, the empty synaptic side should be listed as "none"
    Use loadQueriesJSON instead

    Parameters
    ----------
    fileName : str - location of csv file

    Returns
    ----------
    listOfQueries : list of queries
    """

    preIF = []
    preIF_z = []
    postIF = []
    postIF_z = []

    listOfQueries = []

    # Parse through a csv file containing queries
    with open(fileName) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        rowItr = 0
        for row in readCSV:
            # Read the presynaptic row
            if (rowItr == 0):

                rowItr = rowItr + 1
                cellItr = 0
                for ncell in range(0, len(row)):

                    if (row[ncell] == ''):
                        break
                    if (row[ncell] == "NULL"):
                        break

                    if (cellItr == 0):
                        preIF.append(row[ncell])
                        cellItr = cellItr + 1
                    elif (cellItr == 1):
                        preIF_z.append(int(row[ncell]))
                        cellItr = 0

            # Read the postsynaptic row
            elif (rowItr == 1):
                # print row[0]
                rowItr = rowItr + 1

                cellItr = 0
                for ncell in range(0, len(row)):

                    if (row[ncell] == "NULL"):
                        # print row[ncell]
                        break
                    if (row[ncell] == ''):
                        break

                    if (cellItr == 0):
                        postIF.append(row[ncell])
                        cellItr = cellItr + 1
                    elif (cellItr == 1):
                        postIF_z.append(int(row[ncell]))
                        cellItr = 0

            # blank row separating queries
            else:
                rowItr = 0
                query = {'preIF': preIF, 'preIF_z': preIF_z,
                         'postIF': postIF, 'postIF_z': postIF_z}
                listOfQueries.append(query)
                preIF = []
                preIF_z = []
                postIF = []
                postIF_z = []

    return listOfQueries

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
            inputVol[volItr][:, :, z] = np.cumsum(np.cumsum(inputVol[volItr][:, :, z], 1), 0)

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
        zrange = range((adjacentVolList[0].shape[2] - 2), adjacentVolList[0].shape[2])
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
                        adjacentVolList[volItr][int(rstart), int(cstart + search_win), zItr]

                    searchgrid[ind, volItr] = sumIF1 / (search_win * search_win)

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
    rstart = rInd - search_win/2
    cstart = cInd - search_win/2

    for volItr in range(1, len(baseVolList)):
        sumIF1 = baseVolList[volItr][int(rstart+search_win), int(cstart+search_win), int(zInd)] + \
            baseVolList[volItr][int(rstart), int(cstart), int(zInd)] - baseVolList[volItr][int(rstart+search_win), int(cstart), int(zInd)] - \
            baseVolList[volItr][int(rstart), int(cstart + search_win), int(zInd)]

        localizationGrid[volItr-1] = sumIF1/(search_win * search_win)

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
                    outputVol[rInd, cInd, zInd] = baseVol[rInd, cInd, zInd] * adjResult

                    if len(baseVolList) > 1:
                        coresult = searchColocalizeChannel(baseVolList, search_win, cInd, rInd, zInd)
                        outputVol[rInd, cInd, zInd] = baseVol[rInd, cInd, zInd] * coresult
                else:
                    coresult = searchColocalizeChannel(baseVolList, search_win, cInd, rInd, zInd)
                    outputVol[rInd, cInd, zInd] = baseVol[rInd, cInd, zInd] * coresult


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
        edge_win = int(np.ceil(blobsize*1.5))


    # Data
    presynapticVolumes = synapticVolumes['presynaptic']
    postsynapticVolumes = synapticVolumes['postsynaptic']

    # Number of slices each blob should span
    preIF_z = query['preIF_z']
    postIF_z = query['postIF_z']

    for n in range(0, len(presynapticVolumes)):

        presynapticVolumes[n] = getProbMap(presynapticVolumes[n]) # Step 1
        presynapticVolumes[n] = convolveVolume(presynapticVolumes[n], blobsize) # Step 2

        if preIF_z[n] > 1:
            factorVol = computeFactor(presynapticVolumes[n], int(preIF_z[n])) # Step 3
            presynapticVolumes[n] = presynapticVolumes[n] * factorVol

    for n in range(0, len(postsynapticVolumes)):

        postsynapticVolumes[n] = getProbMap(postsynapticVolumes[n]) # Step 1
        postsynapticVolumes[n] = convolveVolume(postsynapticVolumes[n], blobsize) # Step 2

        if postIF_z[n] > 1:
            factorVol = computeFactor(postsynapticVolumes[n], int(postIF_z[n])) # Step 3
            postsynapticVolumes[n] = postsynapticVolumes[n] * factorVol


    if len(postsynapticVolumes) == 0:
        resultVol = combinePrePostVolumes(presynapticVolumes, postsynapticVolumes, edge_win, blobsize)
    else:
        resultVol = combinePrePostVolumes(postsynapticVolumes, presynapticVolumes, edge_win, blobsize)

    return resultVol;


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

def saveresultvol(vol, datalocation, n):
    """
    save result volume
    Parameters
    -------------
    vol : numpy 3D array
    datalocation: str
    n : int
    """

    fn = os.path.join(datalocation, 'resultVol')
    fn = fn + str(n) + '.npy'
    np.save(fn, vol)




def loadSynapseDataFromQuery(query, anno, win_xy, win_z, filepath):
    """
    Load tiff stacks associated with a query
    Parameters
    ----------
    query : dict - object containing filenames associated with pre/post synaptic markers
    filepath : str - location of data

    Returns
    ----------
    synapticVolumes : dict
        dict with two (pre/post) lists of synaptic volumes
    """

    bbox = synaptogram.getAnnotationBoundingBox2(anno)
    bbox = synaptogram.transformSynapseCoordinates(bbox)

    # query = {'preIF' : preIF, 'preIF_z' : preIF_z, 'postIF' : postIF, 'postIF_z' : postIF_z};

    #presynaptic volumes
    presynapticvolumes = []
    preIF = query['preIF']

    # Loop over every presynaptic channel
    for n in range(0, len(preIF)):
        #print(preIF[n])

        volume = getVolume(bbox, win_xy, win_z, preIF[n], filepath)
        presynapticvolumes.append(volume)

    #postsynaptic volumes
    postsynapticvolumes = []
    postIF = query['postIF']

    # Loop over every postsynaptic channel
    for n in range(0, len(postIF)):
       # print(postIF[n])
        volume = getVolume(bbox, win_xy, win_z, postIF[n], filepath)

        postsynapticvolumes.append(volume)

    synapticVolumes = {'presynaptic': presynapticvolumes,
                       'postsynaptic': postsynapticvolumes}

    return synapticVolumes

def getVolume(bboxCoordinates, win_xy, win_z, volname, filepath):
    """
    Load a portion of image data

    Parameters
    -----------
    bboxCoordinates : dict - coordinates of EM ennotation
    win_xy : int - radius of expansion
    win_z : int - z radius of expansion
    volname : str - name of volume to load
    filepath : str - location of data

    Returns
    -----------
    vol : 3D Numpy array
    """

    # check for boundary issues
    startZ = bboxCoordinates['minZ']
    if (startZ - win_z > -1):
        startZ = startZ - win_z;

    endZ = bboxCoordinates['maxZ']

    if (endZ + win_z < 50):
        endZ = endZ + win_z;

    # get range of x, y values
    startX = bboxCoordinates['minX'] - win_xy;
    startY = bboxCoordinates['minY'] - win_xy;
    deltaX = bboxCoordinates['maxX'] - startX + win_xy;
    deltaY = bboxCoordinates['maxY'] - startY + win_xy;

    startX = int(round(startX))
    startY = int(round(startY))
    deltaX = int(round(deltaX))
    deltaY = int(round(deltaY))
    startZ = int(round(startZ))
    endZ   = int(round(endZ))

    numSlices = endZ - startZ + 1

    # allocate volume
    vol = np.zeros((deltaY, deltaX, numSlices), dtype=np.float64)

    # iterate over each slice
    sliceitr = 0
    for sliceInd in range(startZ, endZ + 1):

        cutout = da.getImageCutoutFromFile(volname, sliceInd, startX, startY, deltaX, deltaY, filepath)
        cutout.astype(np.float64)
        cutout = getProbMap(cutout)

        vol[:, :, sliceitr] = cutout;
        sliceitr = sliceitr + 1

    return vol
