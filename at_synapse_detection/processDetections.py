import json
import scipy
import numpy as np
from scipy.stats import norm
from skimage import measure
from at_synapse_detection import synaptogram
from scipy import io
from shapely import geometry
import os
import cv2
import scipy.ndimage as ndimage

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
    if len(detection.coords) == 1 : 
        bbox = synaptogram.expandBoundingBox()
    
    global_path = bboxToListOfPoints(bbox) 
    global_path = np.array(global_path)
    global_path = global_path.tolist()
    
    zlist = synaptogram.getZListFromBoundingBox(bbox)
    areas = [] 
    
    native_path = resolution['res_xy_nm'] * np.array(global_path)
    native_path = native_path.tolist() 
    
    native_z = resolution['res_z_nm'] * np.array(zlist)
    native_z = native_z.tolist()
    
    # This currently repeats the boundary along the z axis
    for n in range(0, len(zlist)): 
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
    lm_minX = 0
    lm_minY = 0 
    ds_scale = 3/100

    for n in range(0, len(listofdetections)): 
        detection = listofdetections[n]
        #synapse = createSynapseObject(detection, n, resolution)
        synapse = make_prop_into_contours(detection, ds_scale, lm_minX, lm_minY)
        
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
    jsonFN = metadata['outputJSONlocation']

    jsonFN = os.path.join(jsonFN, 'resultVol')
    jsonFN = jsonFN + str(n) + '.json'
    
    resolution = metadata['resolution']

    SE = np.ones((3, 3, 2))
    dilated_volume = ndimage.binary_dilation(probmapvolume > thresh, SE) 

    labelVol = measure.label(dilated_volume)
    stats = measure.regionprops(labelVol, probmapvolume)
    
    data = detectionsToJSONFormat(stats, resolution)

    writeJSONDetectionFile(jsonFN, data)

def make_prop_into_contours(prop, ds_scale, lm_minX, lm_minY):
    
    #input prob is [y, x, z]
    
    #the method below assumes prop.coords z, y, x
    
    coors = []
    for pt in prop.coords: 
        newpt = [pt[2], pt[0], pt[1]]
        coors.append(newpt)
    
    coors = np.flip(np.copy(coors),1)
    zvalues = np.unique(coors[:,2])
    areas =[]
    for z in zvalues:
       
        c2 = coors[coors[:,2]==z]

        mins = np.min(c2,axis=0)
        maxs = np.max(c2,axis=0)
        c2 = c2 - mins
        rng = maxs-mins
        width=rng[0]+1
        height=rng[1]+1
        min_img = np.zeros((height,width),np.uint8)
        idx=np.ravel_multi_index((c2[:,1],c2[:,0]),(height,width))
        min_img_unravel = np.ravel(min_img)
        min_img_unravel[idx]=255
        min_img = np.reshape(min_img_unravel,(height,width))
        min_img_up=cv2.resize(min_img,(2*width,2*height))  
        #f,ax = plt.subplots()
        #ax.imshow(min_img_up,interpolation='nearest',extent=[mins[0],maxs[0]+1,maxs[1]+1,mins[1]])
        #ax.imshow(psdvol[z,:,:],interpolation='nearest',cmap=plt.cm.gray)
        a,cs,b = cv2.findContours(min_img_up,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        csf = []
        for c in cs:
            
            c = np.squeeze(c)
            #c+=.5
            c = .5*(np.array(c,np.float64)+.5)
            c[:,0]+=mins[0]
            c[:,1]+=mins[1]
            c = np.vstack((c,c[0,:]))
            c=c/ds_scale
            c[:,0]=c[:,0]+lm_minX
            c[:,1]=c[:,1]+lm_minY
            #ax.plot(c[:,0],c[:,1],linewidth=3)

            c = np.array(c)
            c = c.tolist()

            z = np.array(z)
            z = z.tolist()
            
            d={'z':z,'global_path':c}
            areas.append(d)
    d={'areas':areas,'oid':str(prop.label), 'id':int(prop.label)}
    return d
        


