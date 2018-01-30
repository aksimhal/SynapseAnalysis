import renderapi
import scipy
import numpy as np
from scipy.stats import norm
#from at_synapse_detection.render_module import RenderModule
from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from at_synapse_detection import dataAccess as da
from at_synapse_detection import SynapseDetection as syn

def getAnnotationBoundingBox(synapse, render_args):

    """
    Get coordinates of a boundingbox containing the entire synapse annotations
    
    Parameters
    ----------
    synapse : dict
        dictionary object generated from input json file
    Returns
    -------
    bboxCoordinates : dict
        containing min/max x/y/z values
    """
        
    synapseSubareasList = synapse['areas']
    maxX = 0; 
    minX = float("inf")

    maxY = 0;
    minY = float("inf")

    maxZ = 0;
    minZ = float("inf")

    stackname = 'BIGALIGN_LENS_EMclahe_all'

    for synapsesubarea in synapseSubareasList:
        subarea_tile = synapsesubarea['global_path']
        subarea_tile = map(list, zip(*subarea_tile))
        xcolumn = subarea_tile[0]
        ycolumn = subarea_tile[1]

        tileid = synapsesubarea['tileId']

        tspec = renderapi.tilespec.get_tile_spec(stackname, tileid, 
                                                 render_args['host'], render_args['port'], 
                                                 render_args['owner'], render_args['project'])
        if (tspec.z > maxZ):
            maxZ = tspec.z; 
        if (tspec.z < minZ):
            minZ = tspec.z; 

        if (max(xcolumn) > maxX):
            maxX = max(xcolumn)
        if (min(xcolumn) < minX):
            minX = min(xcolumn)

        if (max(ycolumn) > maxY):
            maxY = max(ycolumn)
        if (min(ycolumn) < minY):
            minY = min(ycolumn)

    bboxCoordinates = {'minX': minX, 'maxX': maxX, 'minY': minY, 'maxY': maxY, 'minZ': minZ, 'maxZ': maxZ}
        
    return bboxCoordinates
    
def getAnnotationBoundingBox2(synapse):

    """
    Get coordinates of a boundingbox containing the entire synapse annotations
    
    Parameters
    ----------
    synapse : dict
        dictionary object generated from input json file
    Returns
    -------
    bboxCoordinates : dict
        containing min/max x/y/z values
    """
        
    synapseSubareasList = synapse['areas']
    maxX = 0
    minX = float("inf")

    maxY = 0
    minY = float("inf")

    maxZ = 0
    minZ = float("inf")

    #stackname = 'BIGALIGN_LENS_EMclahe_all'

    for synapsesubarea in synapseSubareasList:
        subarea_tile = synapsesubarea['global_path']
        subarea_tile = list(map(list, zip(*subarea_tile)))
        xcolumn = subarea_tile[0]
        ycolumn = subarea_tile[1]
        z = synapsesubarea['z']
        z = int(z)

        # tileIds_subarea = synapsesubarea['tileIds']
        # #tileid = synapsesubarea['tileId']

        # #for tileid in tileIds_subarea: 
        # tileid = tileIds_subarea[0]
        # tspec = renderapi.tilespec.get_tile_spec(stackname, tileid, 
        #                                          render_args['host'], render_args['port'], 
        #                                          render_args['owner'], render_args['project'])
        if (z > maxZ):
            maxZ = z; 
        if (z < minZ):
            minZ = z; 

        if (max(xcolumn) > maxX):
            maxX = max(xcolumn)
        if (min(xcolumn) < minX):
            minX = min(xcolumn)

        if (max(ycolumn) > maxY):
            maxY = max(ycolumn)
        if (min(ycolumn) < minY):
            minY = min(ycolumn)

    bboxCoordinates = {'minX': minX, 'maxX': maxX, 'minY': minY, 'maxY': maxY, 'minZ': minZ, 'maxZ': maxZ}
        
    return bboxCoordinates
    
def transformSynapseCoordinates(bboxCoordinates): 
    """
    
    
    Parameters
    -----------
    
    Returns
    -----------
    
    """
    xoffset = 0#7096.0*3.0/100.0
    yoffset = 0#5871.0*3.0/100.0
    ds_factor = (3.0 / 100.0)

    bboxCoordinates['maxX'] = bboxCoordinates['maxX'] * ds_factor - xoffset
    bboxCoordinates['minX'] = bboxCoordinates['minX'] * ds_factor - xoffset
    bboxCoordinates['maxY'] = bboxCoordinates['maxY'] * ds_factor - yoffset
    bboxCoordinates['minY'] = bboxCoordinates['minY'] * ds_factor - yoffset

    return bboxCoordinates        

def expandBoundingBox(bboxCoordinates, win_xy, win_z): 
    
    # check for boundary issues
    startZ = bboxCoordinates['minZ']
    if (startZ - win_z > -1):
        startZ = startZ - win_z; 
    
    endZ = bboxCoordinates['maxZ']
    if (endZ + win_z < 101):
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
    endZ = int(round(endZ))
    
    

    expandedBox = {'startX': startX, 'deltaX': deltaX, 
                       'startY': startY, 'deltaY': deltaY, 
                       'startZ': startZ, 'endZ': endZ}
    return expandedBox 

def getSynaptogramFromRender(bboxCoordinates, win_xy, win_z, stackList, scale, showProb, mod): 

    """
    create synaptogram for FC annotation data 
    
    Parameters
    -----------
    
    Returns
    -----------
    
    """
    
    minIntensity = 0; 
    EMfilename = 'BIGALIGN_LENS_EMclahe_all'; 
    
    # check for boundary issues
    startZ = bboxCoordinates['minZ']
    #if (startZ - win_z > -1):
    startZ = startZ - win_z; 
    
    endZ = bboxCoordinates['maxZ']
    #if (endZ + win_z < 101):
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
    endZ = int(round(endZ))
    
    

    numSlices = endZ - startZ + 1;  
    numChannels = len(stackList)
    
    # allocate synaptogram img
    img = np.zeros((numChannels * deltaY, numSlices * deltaX), dtype=np.float64)
    
    slicepos = 0; # x 
    
    # iterate over each slice 
    for sliceInd in range(startZ, endZ + 1):
        #print sliceInd; 
        
        ifpos = 0; # y 
        ifitr = 0;     
        
        # iterate over each channel 
        for stack in stackList: 
            #print stack
            
            if stack == EMfilename: 
                maxIntensity = 255;
            else: 
                maxIntensity = 5000; 
                
            cutout = getCutout(stack, sliceInd, startX, 
                                   startY, deltaX, deltaY, 
                                   scale, minIntensity, maxIntensity, mod);
            #print(startX)    
            # Convert to floating point precision 
            cutout.astype(np.float64)
            
            if (showProb):
                if stack == EMfilename: 
                    cutout = np.divide(cutout, 255.0)
                else: 
                    if (np.mean(cutout) != 0):
                        cutout = getProbMap(cutout)
                        

            #cutout = getProbMap(cutout);
            img[ifpos:(ifpos + deltaY), slicepos:(slicepos + deltaX)] = cutout; 
            
            ifpos = ifpos + deltaY; 
            ifitr = ifitr + 1; 
            
        slicepos = slicepos + deltaX; 
            
    return img; 
            
def getAnnotationOutlines(synapse):

    """
    Get annotation outlines, organized by EM slice. 
    
    Parameters
    ----------
    synapse : dict - synapse object, as defined by FC's json file
    render_args : dict - render arugments to access the server on galicia
    Returns
    -------
    synapseOutlinesDict : dict - contains the synapse outlines 
    """
    
    synapseSubareasList = synapse['areas']
    # stackname = 'BIGALIGN_LENS_EMclahe_all'

    listOfSubAreas = []; 
    listOfZinds = []; 

    for synapsesubarea in synapseSubareasList:
        subarea_tile = synapsesubarea['global_path']

        # remap
        subarea_outline = list(map(list, zip(*subarea_tile)))

        # tileIds_subarea = synapsesubarea['tileIds']
        # tileid = tileIds_subarea[0]
        # tspec = renderapi.tilespec.get_tile_spec(stackname, tileid, 
        #                                          render_args['host'], render_args['port'], 
        #                                          render_args['owner'], render_args['project'])
        listOfSubAreas.append(subarea_outline)
        listOfZinds.append(synapsesubarea['z'])

    synapseOutlinesDict = {'subAreas': listOfSubAreas, 'zInds': listOfZinds}

    return synapseOutlinesDict

def transformSynapseOutlinesDict(synapseOutlinesDict):
    listOfSubAreas = synapseOutlinesDict['subAreas']
    transformedListOfSubAreas = []
    xoffset = 0#7096.0*3.0/100.0
    yoffset = 0#5871.0*3.0/100.0
    ds_factor = (3.0 / 100.0)

    
    for subarea in listOfSubAreas: 
        subarea[0] = np.array(subarea[0]) * ds_factor - xoffset
        subarea[1] = np.array(subarea[1]) * ds_factor - yoffset
        transformedListOfSubAreas.append(subarea)
    
    synapseOutlinesDict['subAreas'] = listOfSubAreas

    return synapseOutlinesDict

def plotOutlinesOnImg(img, synapseOutlinesDict, expandedBox, filename, channelNames, textXOffset, textYOffset):

    """
    Plot outlines. 

    Parameters
    ----------

    Returns
    -------

    """
    #['startZ', 'startX', 'startY', 'deltaX', 'deltaY', 'endZ']
    ypt = textYOffset


    listOfSubAreas = synapseOutlinesDict['subAreas']
    listOfZinds = synapseOutlinesDict['zInds']
    deltaX = expandedBox['deltaX']
    deltaY = expandedBox['deltaY']
    #print deltaY
    #%matplotlib notebook
    plt.ioff()

    plt.imshow(img, cmap='gray')

    yAnnoOffset = 0; 
    xMid = np.round(deltaX / 2)
    yMid = np.round(deltaY / 2)

    for chname in channelNames:  
        plt.text(textXOffset, ypt, chname, color='red', horizontalalignment='right')
        ypt = ypt + deltaY 
        
        xMid = np.round(deltaX / 2)
        xMid = xMid + deltaX

        for x in range(0, len(listOfZinds)): 

            subareaOutline = listOfSubAreas[x]
            xcolumn = np.array(subareaOutline[0])
            ycolumn = np.array(subareaOutline[1])

            startX = expandedBox['startX']
            startY = expandedBox['startY']

            xcolumn -= startX
            ycolumn -= startY

            xOffset = deltaX*(listOfZinds[x] - min(listOfZinds)) + deltaX
            xcolumn += xOffset

            ycolumn = ycolumn + yAnnoOffset; 
            
            plt.plot(xcolumn, ycolumn, color='red', linewidth=0.5)
            listoflines = getGridLines(yMid, xMid)
            for line in listoflines: 
                plt.plot(line[1], line[0], color='green', linewidth=0.5)

            xMid = xMid + deltaX
            
        yAnnoOffset = yAnnoOffset + deltaY
        yMid = yMid + deltaY

    plt.colorbar()
    plt.axis('off')
    #plt.show()

    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.clf()
    plt.close()

def getGridLines(rInd, cInd, search_win=2): 

    # rInd = 10 
    # cInd = 20 
    # search_win = 2 

    rstart = rInd - 1.5 * search_win
    rstart = int(rstart)

    cstart = cInd - 1.5 * search_win
    cstart = int(cstart)

    rinds = list(range(rstart, rstart+search_win*3+1, search_win))
    cinds = list(range(cstart, cstart+search_win*3+1, search_win))


    listoflines = []; 
    for n in range(0, 4):   

        rline = [min(rinds), max(rinds)]
        cline = [cinds[n], cinds[n]]
        line = [rline, cline]

        listoflines.append(line)

    for n in range(0, 4):   

        rline = [rinds[n], rinds[n]]
        cline = [min(cinds), max(cinds)]
        line = [rline, cline]

        listoflines.append(line)

    return listoflines


def plotAnnoDetectionsOnImg(img, listOfOutlines, expandedBox, filename, channelNames, textXOffset, textYOffset):

    """
    Plot outlines. 

    Parameters
    ----------

    Returns
    -------

    """

    ypt = textYOffset

    listOfSubAreas = synapseOutlinesDict['subAreas']
    listOfZinds = synapseOutlinesDict['zInds']
    deltaX = expandedBox['deltaX']
    deltaY = expandedBox['deltaY']

    plt.ioff()

    plt.imshow(img, cmap='gray')

    yAnnoOffset = 0; 
    xMid = np.round(deltaX / 2)
    yMid = np.round(deltaY / 2)


    for chname in channelNames:  
        plt.text(textXOffset, ypt, chname, color='red', horizontalalignment='right')
        ypt = ypt + deltaY 

        listOfSubAreas = synapseOutlinesDict['subAreas']
        listOfZinds = synapseOutlinesDict['zInds']
        
          
        listoflines = getGridLines(yMid, xMid)
        for line in listoflines: 
            plt.plot(line[1], line[0], color='green')
        
        for x in range(0, len(listOfZinds)): 

            subareaOutline = listOfSubAreas[x]
            xcolumn = np.array(subareaOutline[0])
            ycolumn = np.array(subareaOutline[1])

            startX = expandedBox['startX']
            startY = expandedBox['startY']

 

            xcolumn -= startX
            ycolumn -= startY

            xOffset = deltaX*(listOfZinds[x] - min(listOfZinds)) + deltaX
            xcolumn += xOffset

            ycolumn = ycolumn + yAnnoOffset; 
            
            plt.plot(xcolumn, ycolumn, color='red')
            
        yAnnoOffset = yAnnoOffset + deltaY
        yMid = yMid + deltaY

    plt.axis('off')
    #plt.show()

    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.clf()
    plt.close()



def addLabelsOnImg(img, expandedBox, filename, channelNames, textXOffset, textYOffset):

    """
    Plot outlines. 

    Parameters
    ----------

    Returns
    -------

    """
    ypt = textYOffset

    deltaY = expandedBox['deltaY']
    plt.ioff()
    plt.imshow(img, cmap='gray')

    for chname in channelNames:  
        plt.text(textXOffset, ypt, chname, color='red', horizontalalignment='right')
        ypt = ypt + deltaY 
        
    plt.axis('off')

    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.clf()
    plt.close()

def getBoundingBoxFromLabel(detection):
    """
    Get coordinates of a boundingbox containing the detection annotations
    Parameters
    ----------
    detection : dict

    Returns
    -------
    bboxCoordinates : dict 
    """
    # detection.cords = ROW COL Z / Y X Z 
    coordinateList = detection.coords

    #TODO Refactor variable names 
    maxX = 0; 
    minX = float("inf")

    maxY = 0;
    minY = float("inf")

    maxZ = 0;
    minZ = float("inf")

    for pt in coordinateList:
        
        if (pt[2] > maxZ):
            maxZ = pt[2]; 
        if (pt[2] < minZ):
            minZ = pt[2]; 

        if (pt[1] > maxX):
            maxX = pt[1]
        if (pt[1] < minX):
            minX = pt[1]

        if (pt[0] > maxY):
            maxY = pt[0]
        if (pt[0] < minY):
            minY = pt[0]

    bboxCoordinates = {'minX': minX, 'maxX': maxX, 'minY': minY, 'maxY': maxY, 'minZ': minZ, 'maxZ': maxZ}
        
    return bboxCoordinates
    
def getZListFromBoundingBox(bbox): 
    """
    Return list of z indexes that are contained in the bounding box 
    
    Parameters
    -------------
    bbox : dict 

    Returns
    --------------
    zlist : list of z indexes of the bbox
    """

    if 'startZ' in bbox: 
        startZ = bbox['startZ']
        endZ = bbox['endZ']
    
    if 'minZ' in bbox: 
        startZ = bbox['minZ']
        endZ = bbox['maxZ']

    zlist = range(int(startZ), int(endZ+1))
    return zlist

def getSynaptogramFromFile(bboxCoordinates, win_xy, win_z, stackList, showProb, filepath): 
    """
    create synaptogram for site3 data 
    
    Parameters
    -----------
    
    Returns
    -----------
    
    """
    EMfilename = "EM"
    
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
    endZ = int(round(endZ))
    
    numSlices = endZ - startZ + 1;  
    numChannels = len(stackList)
    
    # allocate synaptogram img
    img = np.zeros((numChannels * deltaY, numSlices * deltaX), dtype=np.float64)
    
    slicepos = 0; # x 
    
    # iterate over each slice 
    for sliceInd in range(startZ, endZ + 1):
        #print sliceInd; 
        
        ifpos = 0; # y 
        ifitr = 0;     
        
        # iterate over each channel 
        for stack in stackList: 
            #print stack
            
            if stack == EMfilename: 
                maxIntensity = 255;
            else: 
                maxIntensity = 5000; 
                
            cutout = getImageProbMapCutoutFromFile(stack, sliceInd, startX, startY, deltaX, deltaY, filepath)
            
            #print(startX)    
            #Convert to floating point precision 
            # cutout.astype(np.float64)
            
            # if (showProb):
            #     if stack == EMfilename: 
            #         cutout = np.divide(cutout, 255.0)
            #     elif stack == 'results':
            #         cutout = np.divide(cutout, 255.0)

            #     else: 
            #         if (np.mean(cutout) != 0):
            #             cutout = syn.getProbMap(cutout)
                        
            #     #cutout  = cutout > 0.7

            #cutout = getProbMap(cutout);
            img[ifpos:(ifpos + deltaY), slicepos:(slicepos + deltaX)] = cutout; 
            
            ifpos = ifpos + deltaY; 
            ifitr = ifitr + 1; 
            
        slicepos = slicepos + deltaX; 
            
    return img; 

def getImageProbMapCutoutFromFile(channelname, sliceInd, startX, startY, deltaX, deltaY, filepath):
    """
    Load cutout of a slice of a tiff image

    Parameters
    -----------
    channelname : str
    sliceInd : ind
    startX : ind
    startY : ind
    deltaX : ind 
    deltaY : ind 
    filepath : str

    Returns
    -----------
    cutout: 2D numpy array 
    """
    
    folderpath = os.path.join(filepath, channelname)
    img = da.imreadtiffSingleSlice(folderpath, sliceInd)
    img.astype(np.float64)

    probimg = syn.getProbMap(img)

    cutout = probimg[startY:(startY + deltaY), startX:(startX+deltaX)]
    
    return cutout

def synapseAnnotationToSynaptogram(synapse, render_args, win_xy, win_z, filepath, showProb, stackList,textXOffset, textYOffset ):
    
    bbox = getAnnotationBoundingBox2(synapse, render_args)
    bbox = transformSynapseCoordinates(bbox)
    expandedBox = expandBoundingBox(bbox, win_xy, win_z)
    
    synapseOutlinesDict = getAnnotationOutlines(synapse, render_args)
    synapseOutlinesDict = transformSynapseOutlinesDict(synapseOutlinesDict)
    
    filename = os.path.join(filepath, 'synaptograms', '{}.png'.format(synapse['oid']))
    
    img = getSynaptogramFromFile(bbox, win_xy, win_z, stackList, showProb, filepath);
    plotOutlinesOnImg(img, synapseOutlinesDict, expandedBox, filename, stackList, textXOffset, textYOffset)
    #print(filename)
    

