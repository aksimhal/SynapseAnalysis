import numpy as np
import fnmatch
import os
import json
from skimage import io

def imreadtiff(fn):
    """
    Load multipage tiff image file
    Parameters
    ----------
    fn : str - location of tiff stack

    Returns
    ----------
    output : numpy 3D array
    """

    # Read tiff stack
    im = io.imread(fn)

    # Format tiff stack into a numpy array
    output = np.zeros([im.shape[1], im.shape[2], im.shape[0]])
    for n in range(0, im.shape[0]):
        output[:, :, n] = im[n, :, :]

    return output


def imreadtiffseries(folderpath):
    """
    Load a folder of tiff images
    The image filename format is hard coded - to be changed later
    Parameters
    ----------
    folderpath : str - location of tiff stack
    numImages : int - number of images in the folder

    Returns
    ----------
    output : numpy 3D array
    """
    # Read first image
    fn = os.path.join(folderpath, '00000.tiff')
    im = io.imread(fn)

    # Determine number of tiff images in directory
    numImages = len(fnmatch.filter(os.listdir(folderpath), '*.tiff'))

    # Allocate Numpy Array
    output = np.zeros([im.shape[0], im.shape[1], numImages])

    # Read tiff stack
    for n in range(0, numImages):
        fn = os.path.join(folderpath, str(n).zfill(5))
        fn = fn + '.tiff'
        im = io.imread(fn)

        output[:, :, n] = im

    return output

def imreadtiffSingleSlice(folderpath, sliceInd):
    """
    Load a single tiff image in a folder of tiff images
    Parameters
    ----------
    folderpath : str - location of tiff stack
    numImages : int - the image index to load

    Returns
    ----------
    output : numpy 2D array
    """

    # Read tiff stack
    fn = os.path.join(folderpath, str(sliceInd).zfill(5))
    fn = fn + '.tiff'
    im = io.imread(fn)

    output = im

    return output

def load_tiff_from_query(query, base_dir=None):
    """
    Load tiff stacks associated with a query. 

    Parameters
    ----------
    query : dict
        dict object containing filenames associated with pre/post synaptic markers
    base_dir : str - location of the data 

    Returns
    ----------
    synaptic_volumes : dict
        dict with two (pre/post) lists of synaptic volumes
    """

    #presynaptic volumes
    presynapticvolumes = []
    preIF = query['preIF']

    # Loop over every presynaptic channel
    for n in range(0, len(preIF)):
        print(preIF[n])
        if base_dir == None: 
            volume = imreadtiff(preIF[n])
        else: 
            fn = os.path.join(base_dir, preIF[n])
            volume = imreadtiff(fn)
        presynapticvolumes.append(volume)

    #postsynaptic volumes
    postsynapticvolumes = []
    postIF = query['postIF']

    # Loop over every postsynaptic channel
    for n in range(0, len(postIF)):
        print(postIF[n])
        if base_dir == None: 
            volume = imreadtiff(postIF[n])
        else: 
            fn = os.path.join(base_dir, postIF[n])
            volume = imreadtiff(fn)
        postsynapticvolumes.append(volume)

    synaptic_volumes = {'presynaptic': presynapticvolumes,
                       'postsynaptic': postsynapticvolumes}

    return synaptic_volumes

def loadTiffSeriesFromQuery(query, filepath):
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

    # query = {'preIF' : preIF, 'preIF_z' : preIF_z, 'postIF' : postIF, 'postIF_z' : postIF_z};

    #presynaptic volumes
    presynapticvolumes = []
    preIF = query['preIF']

    # Loop over every presynaptic channel
    for n in range(0, len(preIF)):

        #print(preIF[n])
        fn = os.path.join(filepath, preIF[n])
        volume = imreadtiffseries(fn)
        presynapticvolumes.append(volume)

    #postsynaptic volumes
    postsynapticvolumes = []
    postIF = query['postIF']

    # Loop over every postsynaptic channel
    for n in range(0, len(postIF)):
        #print(postIF[n])
        fn = os.path.join(filepath, postIF[n])
        volume = imreadtiffseries(fn)
        postsynapticvolumes.append(volume)

    synapticVolumes = {'presynaptic': presynapticvolumes,
                       'postsynaptic': postsynapticvolumes}

    return synapticVolumes



def getImageCutoutFromFile(channelname, sliceInd, startX, startY, deltaX, deltaY, filepath):
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
    img = imreadtiffSingleSlice(folderpath, sliceInd)
    cutout = img[startY:(startY + deltaY), startX:(startX+deltaX)]

    return cutout

def writeJSONFile(filename, data):
    """
    write a json file

    Parameters
    --------------
    filename : str
    data : dict

    Returns
    --------------
    """
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)