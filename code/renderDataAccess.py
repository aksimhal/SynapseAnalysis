import json
import renderapi
import scipy
import numpy as np
from scipy.stats import norm
from render_module import RenderModule
from scipy import signal
import csv



def getCutout(stack, sliceInd, xstart, ystart, deltaX, deltaY, scale, minIntensity, maxIntensity, mod):
    """
    Returns 2D cutout of data from Render 
    Parameters
    ----------
    stack : str - name of channel in Render 
    sliceInd : ind - slice index requested
    xstart : ind - starting x coordinates 
    ystart : ind - starting y coordinates 
    deltaX : ind - width of the cutout 
    deltaY : ind - heigh of the cutout 
    scale : ind - scale to return the data. 0.03 is ~100nm/px 
    minIntensity : ind - minimum intensity value for output cutout (converting from 16bit) 
    maxIntensity : ind - maximum intensity value for output cutout (converting from 8 bit)
    mod : render module object

    Returns
    ----------
    img : numpy 2D array
    """
    
    img = renderapi.image.get_bb_image(
        stack, sliceInd, xstart, ystart, deltaX, deltaY, scale, minIntensity, maxIntensity, render=mod.render)

    img = img[:, :, 0]
    return img


def getVolumeFromRender(stack, volDimensions, scale, intensityrange, mod):
    """
    Get volume of image data from Render 

    Parameters
    ----------
    stack : str - name of channel in Render 
    volDimensions : dict - dict object with volume dimensions 
    scale : ind - scale to return the data 
    intensityrange : list - list of length 2 containing min/max intensity parameters 
    mod - render module object 

    Returns
    ----------
    vol : 3D numpy array 
    """

    xstart = volDimensions['xstart']
    ystart = volDimensions['ystart']
    deltaX = volDimensions['deltaX']
    deltaY = volDimensions['deltaY']
    startZ = volDimensions['startZ']
    endZ = volDimensions['endZ']

    vol = np.zeros(
        [int(deltaX * scale), int(deltaY * scale), int(endZ - startZ)])
    for sliceInd in xrange(startZ, endZ):

        img = getCutout(stack, sliceInd, xstart, ystart, deltaX,
                    deltaY, scale, intensityrange[0], intensityrange[1], mod)
        vol[:, :, sliceInd - startZ] = img;

    return vol


def getChannelVolumes(query, volDimensions, scale, intensityrange, mod):
    """
    Get data from Render as defined by a query

    Parameters
    ----------
    query : dict
        dict object containing filenames associated with pre/post synaptic markers
    volDimensions : dict - dict object with volume dimensions 
    scale : ind - scale to return the data 
    intensityrange : list - list of length 2 containing min/max intensity parameters 
    mod - render module object 

    Returns
    ----------
    synapticVolumes : dict
        dict with two (pre/post) lists of synaptic volumes
    """
    
    # query = {'preIF' : preIF, 'preIF_z' : preIF_z, 'postIF' : postIF, 'postIF_z' : postIF_z};

    #presynaptic volumes
    presynapticvolumes = []
    preIF = query['preIF']

    for n in xrange(0, len(preIF)):

        print preIF[n]

        volume = getVolumeFromRender(
            preIF[n], volDimensions, scale, intensityrange, mod)
        presynapticvolumes.append(volume)

    #postsynaptic volumes
    postsynapticvolumes = []
    postIF = query['postIF']

    for n in xrange(0, len(postIF)):
        print postIF[n]
        volume = getVolumeFromRender(
            postIF[n], volDimensions, scale, intensityrange, mod)
        postsynapticvolumes.append(volume)

    synapticVolumes = {'presynaptic': presynapticvolumes,
                       'postsynaptic': postsynapticvolumes};
    return synapticVolumes
