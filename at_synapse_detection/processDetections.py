import json
import scipy
import numpy as np
from scipy.stats import norm
from skimage import measure
import synaptogram
from scipy import io
from shapely import geometry
import os


def bboxToListOfPoints(bbox): 
    """
    Converts bounding box into a list of corner points [ROW COL]
    Parameters
    -------------
    bbox : dict - start points and deltas 
    Returns
    -------------
    listofpoints - ROW COL
    """
    minX = bbox['minX']
    maxX = bbox['maxX']
    minY = bbox['minY']
    maxY = bbox['maxY']
    minZ = bbox['minZ']
    maxZ = bbox['maxZ']
    
    
    # pt1 = [minY, minX] # ROW COLUMN 
    # pt2 = [maxY, minX] # ROW COLUMN 
    # pt3 = [maxY, maxX] # ROW COLUMN 
    # pt4 = [minY, maxX] # ROW COLUMN 
    
    pt1 = [minX, minY] # X Y 
    pt2 = [minX, maxY] # X Y 
    pt3 = [maxX, maxY] # X Y
    pt4 = [maxX, minY] # X Y 

    listofpoints = [pt1, pt2, pt3, pt4]
    
    return listofpoints

def createSynapseObject(detection, detection_number, resolution): 
    """
    Create a synapse object which follows FC guidelines. 
    global_path - perimeter of the detection in pixel coordinates 
    z - list of z indexes 
    native_path - perimeter of the detection in nanometers 
    native_z - z index in nanometers

    Parameters: 
    ---------------
    detection : dict object from measure.regionprobs
    detection_number : int - number of the detection 
    resolution : dict - dict with resolutions parameters 

    Return
    ---------------
    synapse : dict object - synapse path 
    """

    bbox = synaptogram.getBoundingBoxFromLabel(detection)
    global_path = bboxToListOfPoints(bbox) 
    zlist = synaptogram.getZListFromBoundingBox(bbox)
    areas = [] 
    
    native_path = resolution['res_xy_nm'] * np.array(global_path)
    native_path = native_path.tolist() 
    
    native_z = resolution['res_z_nm'] * np.array(zlist)
    native_z = native_z.tolist()
    
    # This currently repeats the boundary along the z axis
    for n in xrange(0, len(zlist)): 
        subarea = {'global_path' : global_path, 'z' : zlist[n], 'native_path' : native_path, 'native_z' : native_z[n]}
        areas.append(subarea)

    synapse = {'id': detection_number, 'areas': areas}

    return synapse

def detectionsToJSONFormat(listofdetections, resolution): 
    """
    Take a list of detections and output into a json saveable format 

    Parameters: 
    --------------
    listOfDetections : list - stats object from skiimage.measure.label
    resolution : dict - dict containing resolution parameters 

    Returns: 
    ---------------
    data : dict - json saveable dict object 

    """
    area_lists = [] 
    for n in xrange(0, len(listofdetections)): 
        detection = listofdetections[n]
        synapse = createSynapseObject(detection, n, resolution)
        area_lists.append(synapse)

    data = {'area_lists': area_lists}
    
    return data

def writeJSONDetectionFile(filename, data): 
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)



def createPolygonFromBBox(bbox): 
    """
    
    Parameters
    -------------
    bbox : dict - start points and deltas 
    
    """
    startX = bbox['startX']
    startY = bbox['startY']
    startZ = bbox['startZ']
    deltaX = bbox['deltaX']
    deltaY = bbox['deltaY']
    endZ = bbox['endZ']
    
    
    pt1 = [startX, startY]
    pt2 = [startX, startY + deltaY]
    pt3 = [startX + deltaX, startY + deltaY]
    pt4 = [startX + deltaX, startY]
    
    poly = geometry.Polygon((pt1, pt2, pt3, pt4))
    
    return poly

def probMapToJSON(probmapvolume, metadata, n): 
    """
    Threshold probability map and store as json annotations 

    Parameters: 
    probmapvolume : 3D numpy array
    metadata : dict 
    n : ind - query index to match the output filename 
    """

    thresh = metadata['thresh'] 
    datalocation = metadata['datalocation']
    outputFN = os.path.join(datalocation, 'resultVol')
    outputFN = outputFN + str(n) + '.json'
    resolution = metadata['resolution']

    labelVol = measure.label(probmapvolume > thresh)
    stats = measure.regionprops(labelVol, probmapvolume)
    
    data = detectionsToJSONFormat(stats, resolution)

    writeJSONDetectionFile(outputFN, data)




