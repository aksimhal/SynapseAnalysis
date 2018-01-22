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
from at_synapse_detection import SynapseDetection as syn


def checkQueryAgainstAnno(anno, query, threshlist, win_xy, win_z, filepath): 
    """
    Given a manual annotation, see if a synapse can be detected.  
    Input is a manual annotation and a query, output is a array that 
    indicates at which threshold the annotation is detected or not detected 

    Parameters: 
    -------------------
    anno : dict - manual synapse annotation 
    query : dict
    threshlist : list - list of thresholds 
    win_xy : int - window to search in (full window is 2x)
    win_z : int - window, z dimension 
    filepath : str - data location 

    Returns: 
    --------------------
    synapseDetected : list - same size as threslist, T/F if detected
    """

    synapseDetected = np.zeros(len(threshlist), dtype=bool)

    # Get range of coordinates 
    bbox = synaptogram.getAnnotationBoundingBox2(anno)
    bbox = synaptogram.transformSynapseCoordinates(bbox)

    expandedBox = synaptogram.expandBoundingBox(bbox, win_xy, win_z)
    zrange = list(range(expandedBox['startZ'], expandedBox['endZ']+1))

    synapticVolumes = syn.loadSynapseDataFromQuery(query, anno, win_xy, win_z, filepath)
    resultVol = getSynapseDetections(synapticVolumes, query)

    synapsevol = annotationToBinaryVolume(resultVol.shape, anno, expandedBox, bbox, zrange) 
    SE = np.ones((2, 2, 2))
         
    for n, thresh in enumerate(threshlist): 
        
        dilated_volume = ndimage.binary_dilation(resultVol > thresh, SE)
        overlaidvolumes = dilated_volume + synapsevol

        if overlaidvolumes.max() > 1: 
            #print("Synapse Detected!")
            synapseDetected[n] = 1
        else: 
            synapseDetected[n] = 0
            #print("Synapse not detected")
            
    return synapseDetected

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

def annotationToBinaryVolume(shape, anno, expandedBox, bbox, zrange): 
    """
    convert annotation to binary volume that matches the cutout size in checkQueryAgainstAnno()

    Parameters: 
    -------------
    shape : size of output volume
    anno : annotation object 
    expandedBox :
    bbox
    zrange

    Returns: 
    -------------
    synapsevol : 3D Numpy 
    """
    synapsevol = np.zeros(shape)

    synapseOutlinesDict = synaptogram.getAnnotationOutlines(anno)
    synapseOutlinesDict = synaptogram.transformSynapseOutlinesDict(synapseOutlinesDict)
    listOfZinds = synapseOutlinesDict['zInds']
    listOfZinds = sorted(listOfZinds)
    
    startX = expandedBox['startX']
    startY = expandedBox['startY']
    minX = math.floor(bbox['minX'] - startX)
    maxX = math.ceil(bbox['maxX'] - startX)
    minY = math.floor(bbox['minY'] - startY)
    maxY = math.ceil(bbox['maxY'] - startY)

    offsetZ = 0 
    for localZ, globalZ in enumerate(zrange): 
        if zrange[localZ] == listOfZinds[offsetZ]: 
            synapsevol[minY:maxY, minX:maxX, localZ] = 1
            offsetZ = offsetZ + 1 

            if offsetZ == len(listOfZinds): 
                break


    return synapsevol

def getSynapseDetectionsMW(synapticVolumes, query, kernelLength=2, edge_win = 3,
                         search_win = 2):
    """
    This function calls the functions needed to run probabilistic synapse detection 

    Parameters
    ----------
    synapticVolumes : dict
        has two keys (presynaptic,postsynaptic) which contain lists of 3D numpy arrays 
    query : dict
        contains the minumum slice information for each channel 
    kernelLength : int
        Minimum 2D Blob Size (default 2)
    edge_win: int
        Edge window (default 8)
    search_win: int
        Search windows (default 2)

    Returns
    ----------
    resultVol : 3D numpy array - final probability map 
    """

    # Data
    presynapticVolumes = synapticVolumes['presynaptic']
    postsynapticVolumes = synapticVolumes['postsynaptic']

    # Number of slices each blob should span 
    preIF_z = query['preIF_z']
    postIF_z = query['postIF_z']

    for n in range(0, len(presynapticVolumes)):

        presynapticVolumes[n] = getProbMap_MW(presynapticVolumes[n], query['preIF'][n]) # Step 1
        presynapticVolumes[n] = syn.convolveVolume(presynapticVolumes[n], kernelLength) # Step 2

        if preIF_z[n] > 1: 
            factorVol = syn.computeFactor(presynapticVolumes[n], int(preIF_z[n])) # Step 3
            presynapticVolumes[n] = presynapticVolumes[n] * factorVol

    for n in range(0, len(postsynapticVolumes)):
        
        postsynapticVolumes[n] = syn.getProbMap_MW(postsynapticVolumes[n], query['postIF'][n]) # Step 1
        postsynapticVolumes[n] = syn.convolveVolume(postsynapticVolumes[n], kernelLength) # Step 2

        if postIF_z[n] > 1:
            factorVol = syn.computeFactor(postsynapticVolumes[n], int(postIF_z[n])) # Step 3
            postsynapticVolumes[n] = postsynapticVolumes[n] * factorVol

    # combinePrePostVolumes(base, adjacent)
    # Step 4 

    #print(len(presynapticVolumes))
    #print(len(postsynapticVolumes))
    if len(postsynapticVolumes) == 0: 
        resultVol = syn.combinePrePostVolumes(presynapticVolumes, postsynapticVolumes, edge_win, search_win)
    else: 
        resultVol = syn.combinePrePostVolumes(postsynapticVolumes, presynapticVolumes, edge_win, search_win)

    return resultVol; 
