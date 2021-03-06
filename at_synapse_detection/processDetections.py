import json
import scipy
import numpy as np
from scipy.stats import norm
from skimage import measure
from at_synapse_detection import synaptogram
from at_synapse_detection import SynapseDetection as syn
from scipy import io
from shapely import geometry
import os
import cv2
import scipy.ndimage as ndimage
from at_synapse_detection import evaluate_synapse_detection as esd
from at_synapse_detection.AnnotationJsonSchema import AnnotationFile, NumpyArray
import pandas


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

    pt1 = [minX, minY]  # X Y
    pt2 = [minX, maxY]  # X Y
    pt3 = [maxX, maxY]  # X Y
    pt4 = [maxX, minY]  # X Y

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
    # if len(detection.coords) == 1:
    #     bbox = synaptogram.expandBoundingBox(bbox)

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
        subarea = {'global_path': global_path, 'z': zlist[n],
                   'native_path': native_path, 'native_z': native_z[n]}
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
    ds_scale = 3 / 100

    for n in range(0, len(listofdetections)):
        detection = listofdetections[n]
        #synapse = createSynapseObject(detection, n, resolution)
        synapse = make_prop_into_contours(
            detection, ds_scale, lm_minX, lm_minY)

        area_lists.append(synapse)

    data = {'area_lists': area_lists}

    return data


def writeJSONDetectionFile(filename, output_json):
    """
    Write json file to disk
    Parameters
    -------------
    filename : str
    output_json : dict
    """

    with open(filename, 'w') as outfile:
        json.dump(output_json, outfile)


def writeJSONDetectionFile2(filename, data):
    """
    Write json file to disk using AnnotationFile() format
    Parameters
    -------------
    filename : str
    output_json : dict
    """

    schema = AnnotationFile()
    (output_json, errors) = schema.dump(data)

    with open(filename, 'w') as outfile:
        json.dump(output_json, outfile)


def createPolygonFromBBox(bbox):
    """
    Create a polygon object from bounding box dict

    Parameters
    -------------
    bbox : dict - start points and deltas
    Returns
    -------------
    poly : geometry.polygon object

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


def probMapToJSON(probmapvolume, metadata, query, n):
    """
    Threshold probability map and store as json annotations

    Parameters
    ------------
    probmapvolume : 3D numpy array
    metadata : dict
    n : ind - query index to match the output filename
    """

    if 'thresh' in query.keys():
        thresh = query['thresh']
    else:
        thresh = 0.9

    resolution = metadata['resolution']

    jsonFN = metadata['outputJSONlocation']
    jsonFN = os.path.join(jsonFN, 'resultVol')
    jsonFN = jsonFN + str(n) + '.json'

    # Dilate detections
    SE = np.ones((2, 2, 2))
    dilated_volume = ndimage.binary_dilation(probmapvolume > thresh, SE)
    labelVol = measure.label(dilated_volume)
    stats = measure.regionprops(labelVol, probmapvolume)

    data = detectionsToJSONFormat(stats, resolution)
    writeJSONDetectionFile(jsonFN, data)


def make_prop_into_contours(prop, ds_scale, lm_minX, lm_minY):
    """
    function copied from FC; turns prop object into contour dict

    Parameters
    -------------
    prop
    ds_scale : float downsampling scale (default = 3/100)
    lm_minX : int (default = 0)
    lm_minY : int (default = 0)

    """
    #input prob is [y, x, z]

    #the method below assumes prop.coords z, y, x

    coors = []
    for pt in prop.coords:
        newpt = [pt[2], pt[0], pt[1]]
        coors.append(newpt)

    coors = np.flip(np.copy(coors), 1)
    zvalues = np.unique(coors[:, 2])
    areas = []
    for z in zvalues:

        c2 = coors[coors[:, 2] == z]

        mins = np.min(c2, axis=0)
        maxs = np.max(c2, axis=0)
        c2 = c2 - mins
        rng = maxs - mins
        width = rng[0] + 1
        height = rng[1] + 1
        min_img = np.zeros((height, width), np.uint8)
        idx = np.ravel_multi_index((c2[:, 1], c2[:, 0]), (height, width))
        min_img_unravel = np.ravel(min_img)
        min_img_unravel[idx] = 255
        min_img = np.reshape(min_img_unravel, (height, width))
        min_img_up = cv2.resize(min_img, (2 * width, 2 * height))
        #f, ax = plt.subplots()
        #ax.imshow(min_img_up, interpolation='nearest',
        # extent=[mins[0], maxs[0]+1, maxs[1]+1, mins[1]])
        #ax.imshow(psdvol[z, :, :], interpolation='nearest', cmap=plt.cm.gray)
        a, cs, b = cv2.findContours(
            min_img_up, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        csf = []
        for c in cs:

            c = np.squeeze(c)
            #c+=.5
            c = .5 * (np.array(c, np.float64) + .5)
            c[:, 0] += mins[0]
            c[:, 1] += mins[1]
            c = np.vstack((c, c[0, :]))
            c = c / ds_scale
            c[:, 0] = c[:, 0] + lm_minX
            c[:, 1] = c[:, 1] + lm_minY
            #ax.plot(c[:,0],c[:,1],linewidth=3)

            c = np.array(c)
            c = c.tolist()

            z = np.array(z)
            z = z.tolist()

            d = {'z': z, 'global_path': c}
            areas.append(d)
    d = {'areas': areas, 'oid': str(prop.label), 'id': int(prop.label)}
    return d


def consolidateDetections(detections1, detections2):

    #detections1 == EM
    #detections2 == LM

    LM_index1 = esd.get_index('LM_index1')
    LM_index2 = esd.get_index('LM_index2')

    LM_bounds1 = esd.insert_annotations_into_index(LM_index1, detections1)
    LM_bounds2 = esd.insert_annotations_into_index(LM_index2, detections2)

    overlap_matrix = np.zeros((len(detections1), len(detections2)), np.bool)

    for i, anno2 in enumerate(detections2):

        # if i > 100:
        #     break

        res = LM_index1.intersection(LM_bounds2[i])
        for k in res:
            anno1 = detections1[k]
            try:
                overlaps, zsection = esd.do_annotations_overlap(anno2, anno1)
            except:
                print(anno1['oid'], anno2['oid'])
            if overlaps:
                overlap_matrix[k, i] = True

    #remove all annotations from LM2 which overlap with LM1

    anno2Overlaps = np.sum(overlap_matrix, axis=0)
    indsToRemove = np.nonzero(anno2Overlaps)

    uniqueDetections = np.delete(detections2, indsToRemove[0])

    detections = detections1 + uniqueDetections.tolist()

    return detections  # detections1, uniqueDetections


def getMissedAnnoIds(missed_annotations):
    """
    Extract oid from annotations
    Parameters
    ----------------
    missed_annotations: list of dict

    Returns
    ----------------
    missedAnnoIds: list of ints
    """
    missedAnnoIds = []
    for anno in missed_annotations:
        missedAnnoIds.append(anno['oid'])

    return missedAnnoIds


def evalsyndetections(args):
    """
    Evaluate glutamatergic synapse detection

    Parameters
    --------------
    args: dict of strs
        - contains information needed for evaluation
    Returns:
    output: dict
        - contains evaluation results
    """

    # Load EM Annotations
    EM_annotations = esd.load_annotation_file(args['EM_annotation_json'])
    # Load LM Annotations (detections)
    LM_annotations = esd.load_annotation_file(args['LM_annotation_json'])

    df = pandas.read_csv(args['EM_metadata_csv'])
    # Eliminate annotations which are not synapses or are not glutamatergic
    good_rows = (df[args['EM_not_synapse_column']] == False) & (
        df[args['EM_inclass_column']] == True)
    good_df = df[good_rows]

    # Find bounding cube that contains
    ann_minX = good_df.min().minX
    ann_minY = good_df.min().minY
    ann_maxX = good_df.max().maxX
    ann_maxY = good_df.max().maxY
    ann_minZ = good_df.min().minZ
    ann_maxZ = good_df.max().maxZ
    good_annotations = [
        al for al in EM_annotations if al['id'] in good_df.index]

    (ann_minX, ann_minY, ann_minZ, ann_maxX, ann_maxY, ann_maxZ) = \
        esd.get_bounding_box_of_annotations(good_annotations)

    # Determine LM Edge Annotations
    LM_edge = esd.get_edge_annotations(
        LM_annotations, ann_minX, ann_maxX, ann_minY, ann_maxY, ann_minZ, ann_maxZ)
    # Determine EM Edge Annotations
    EM_edge = esd.get_edge_annotations(
        good_annotations, ann_minX, ann_maxX, ann_minY, ann_maxY, ann_minZ, ann_maxZ)

    # Place detections in a spatial index
    LM_index = esd.get_index('LM_index')
    LM_bounds = esd.insert_annotations_into_index(LM_index, LM_annotations)
    EM_index = esd.get_index('EM_index')
    EM_bounds = esd.insert_annotations_into_index(EM_index, good_annotations)

    overlap_matrix = np.zeros(
        (len(good_annotations), len(LM_annotations)), np.bool)
    j = 0
    for i, alLM in enumerate(LM_annotations):  # Loop over each LM detection
        # check to see if LM detection overlaps with any EM anno
        res = EM_index.intersection(LM_bounds[i])
        for k in res:
            alEM = good_annotations[k]
            overlaps, zsection = esd.do_annotations_overlap(alLM, alEM)
            if overlaps:
                overlap_matrix[k, i] = True

    bins = np.arange(0, 4)  # 3 bins. 0 overlap, 1 overlap, 1+ overlaps
    LM_per_EM = np.sum(overlap_matrix, axis=1)
    EM_per_LM = np.sum(overlap_matrix, axis=0)
    LM_per_EM_counts, edges = np.histogram(
        LM_per_EM[EM_edge == False], bins=bins, normed=True)
    EM_per_LM_counts, edges = np.histogram(
        EM_per_LM[LM_edge == False], bins=bins, normed=True)
    print("EM_per_LM", EM_per_LM_counts)
    print("LM_per_EM", LM_per_EM_counts)
    print('lm edge detections:', np.sum(LM_edge))
    print('em edge annotations', np.sum(EM_edge))
    print('LM detections:', len(LM_edge))

    # Sort annotations into categories
    # True Positives (EM Detections)
    detected_annotations = []
    for counter, synapse in enumerate(good_annotations):
        if (LM_per_EM[counter] != 0 and EM_edge[counter] == False):
            detected_annotations.append(synapse)

    # False Negatives (EM Detections)
    missed_annotations = []
    for counter, synapse in enumerate(good_annotations):
        if (LM_per_EM[counter] == 0 and EM_edge[counter] == False):
            missed_annotations.append(synapse)

    # False Positives (LM Detections)
    false_positives = []
    for counter, anno in enumerate(LM_annotations):
        if (EM_per_LM[counter] == 0 and LM_edge[counter] == False):
            false_positives.append(anno)

    # True Positive (LM Detections)
    tp_detections = []
    for counter, anno in enumerate(LM_annotations):
        if (EM_per_LM[counter] != 0 and LM_edge[counter] == False):
            tp_detections.append(anno)

    # Collate results into a dict
    output = {'missed_annotations': missed_annotations, 'false_positives': false_positives,
              'tp_detections': tp_detections, 'good_annotations': good_annotations,
              'overlap_matrix': overlap_matrix, 'EM_edge': EM_edge, 'LM_edge': LM_edge,
              'EM_per_LM': EM_per_LM_counts, 'LM_per_EM': LM_per_EM_counts, 'detected_annotations': detected_annotations}

    return output


def combineResultVolumes(listOfQueryNumbers, listOfThresholds, metadata, args):
    """
    Combine multiple queries and evaluate performance

    Parameters
    ---------------
    listOfQueryNumbers : list of ints
    listOfThresholds : list of ints
    metadata : dict
    args : dict

    Returns
    ----------------
    queryresult : dict
    """

    resultVolList = []  # list of thresholded result volumes

    for n, queryNum in enumerate(listOfQueryNumbers):
        # load result volume
        fn = os.path.join(metadata['outputNPYlocation'], 'resultVol')
        fn = fn + str(queryNum) + '.npy'
        resultVol_n = np.load(fn)
        resultVol_n = resultVol_n > listOfThresholds[n]
        resultVolList.append(resultVol_n)

    resultVol = resultVolList[0]
    combinedQNum = str(listOfQueryNumbers[0])
    for volItr in range(1, len(resultVolList)):
        resultVol = resultVol + resultVolList[volItr]
        combinedQNum = combinedQNum + str(listOfQueryNumbers[volItr])

    combinedQNum = combinedQNum + str(0) + str(0)

    # output detections to json file
    query = {'thresh': 0.9}
    probMapToJSON(resultVol, metadata, query, "_combined")

    jsonFN = metadata['outputJSONlocation']
    jsonFN = os.path.join(jsonFN, 'resultVol_combined.json')

    # Evaluate results
    args['LM_annotation_json'] = jsonFN
    queryresult = evalsyndetections(args)

    return queryresult


def printEvalToText(listofevals, listOfQueries, listOfThresholds):
    """
    Outputs the evaluation results for each query to a text file

    Parameters
    --------------
    listofevals : list of dictionaries
    listOfQueries: list of dictionaries
    thresh: threshold at which detections are computed
    """
    file = open('output.txt', 'w')

    for n, evalresult in enumerate(listofevals):
        query = listOfQueries[n]
        file.write(json.dumps(query))
        file.write('\n')
        file.write('Threshold: ' + str(listOfThresholds[n]))
        file.write('\n')

        file.write("EM_per_LM: " + str(evalresult['EM_per_LM']) + '\n')
        file.write("LM_per_EM: " + str(evalresult['LM_per_EM']) + '\n')
        file.write('lm edge detections: ' +
                   str(np.sum(evalresult['LM_edge'])) + '\n')
        file.write('em edge annotations: ' +
                   str(np.sum(evalresult['EM_edge'])) + '\n')
        file.write('LM detections:' + str(len(evalresult['LM_edge'])) + '\n')

        file.write('\n')

    file.close()
