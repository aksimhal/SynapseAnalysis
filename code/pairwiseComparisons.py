# pairwise comparisons 

import json
import renderapi
import scipy
import numpy as np
from scipy.stats import norm
from render_module import RenderModule
from scipy import signal
import csv

from skimage import io
from skimage import measure

#import matplotlib.pyplot as plt
import scipy.io

import SynapseDetection as syn
import renderDataAccess as rda
import dataAccess as da

# Function to look at pairwise comparisons 
def psd95_pairwise(): 
    """
    PSD95 Pairwise 
    """

    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/Antibody comparisons/KDM-RW-120419/'
    tiffpath_base = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/result_tiffs/antibody_comparisons/KDM-RW-120419/';

    foldernames = ['PSD95r_2nd.tif', 'PSD95m_1st.tif', 'synapsin_1st.tif']

    minSpanList = [2, 2]

    fn = base_dir + foldernames[2]
    synapsin_1st = da.imreadtiff(fn)
    fn = base_dir + foldernames[1]
    PSD95m_1st = da.imreadtiff(fn)

    synapticVolumes = {'presynaptic': [synapsin_1st],
                        'postsynaptic': [PSD95m_1st]}

    query = {'preIF': [], 'preIF_z': [2],
            'postIF': [], 'postIF_z': [2]}

    resultVol = syn.getSynapseDetections(synapticVolumes, query); 
    scipy.io.savemat('psdM_result.mat', {'resultVol':resultVol} )
    
    labelVol = measure.label(resultVol > 0.9)
    stats = measure.regionprops(labelVol)
    print len(stats) 

    fn = base_dir + foldernames[2]
    synapsin_1st = da.imreadtiff(fn)
    fn = base_dir + foldernames[0]
    PSD95r_2nd = da.imreadtiff(fn)

    synapticVolumes = {'presynaptic': [synapsin_1st],
                       'postsynaptic': [PSD95r_2nd]}

    fn = tiffpath_base + 'psdR_result.mat'
    resultVol = syn.getSynapseDetections(synapticVolumes, query); 
    scipy.io.savemat(fn, {'resultVol':resultVol} )

    labelVol = measure.label(resultVol > 0.9)
    stats = measure.regionprops(labelVol)
    print len(stats) 

    return resultVol; 



# Function to look at pairwise comparisons 
def synapsin_pairwise(): 
    """
    Synapsin Pairwise 
    """
    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/Antibody comparisons/KDM-SYN-090210/Synapsin/';
    tiffpath_base = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/result_tiffs/antibody_comparisons/KDM-SYN-090210/Synapsin/';

    foldernames = ['synapsinGP1stA.tif', 'synapsinR1stA.tif', 'psd1stA.tif']
    thresh = 0.9
    minSpanList = [2, 2]

    fn = base_dir + foldernames[2]
    psd1stA = da.imreadtiff(fn)
    fn = base_dir + foldernames[0]
    synapsinGP1stA = da.imreadtiff(fn)

    synapticVolumes = {'presynaptic': [synapsinGP1stA],
                        'postsynaptic': [psd1stA]}

    query = {'preIF': [], 'preIF_z': [2],
            'postIF': [], 'postIF_z': [2]}

    print "About to start synapse GP detection"

    resultVol = syn.getSynapseDetections(synapticVolumes, query); 
    scipy.io.savemat('synapsinGP1stA_result.mat', {'resultVol':resultVol} )

    labelVol = measure.label(resultVol > thresh)
    stats = measure.regionprops(labelVol)
    print len(stats) 

    fn = base_dir + foldernames[2]
    psd1stA = da.imreadtiff(fn)
    fn = base_dir + foldernames[1]
    synapsinR1stA = da.imreadtiff(fn)

    synapticVolumes = {'presynaptic': [synapsinR1stA],
                       'postsynaptic': [psd1stA]}

    fn = tiffpath_base + 'synapsinR1stA_result.mat'

    print "About to start synapse R detection"

    resultVol = syn.getSynapseDetections(synapticVolumes, query); 
    scipy.io.savemat(fn, {'resultVol':resultVol} )

    labelVol = measure.label(resultVol > thresh)
    stats = measure.regionprops(labelVol)
    print len(stats) 

    return resultVol; 


def gephyrin_pairwise():
    """
    Gephyrin Pairwise 
    """

    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/Antibody comparisons/KDM-SYN-161213/Gephyrin L106-83/';
    tiffpath_base = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/result_tiffs/antibody_comparisons/KDM-SYN-161213/Gephyrin L106-83/';


    foldernames = ['GephyrinL106-83.tif', 'GAD.tif']

    thresh = 0.9
    minSpanList = [2, 2]
    
    fn = base_dir + foldernames[1]
    GAD = da.imreadtiff(fn)
    fn = base_dir + foldernames[0]
    GephyrinL106 = da.imreadtiff(fn)

    synapticVolumes = {'presynaptic': [GAD],
                       'postsynaptic': [GephyrinL106]}
    
    query = {'preIF': [], 'preIF_z': [2],
            'postIF': [], 'postIF_z': [2]}

    resultVol = syn.getSynapseDetections(synapticVolumes, query); 
    scipy.io.savemat('GephyrinL106_result.mat', {'resultVol':resultVol} )
    
    labelVol = measure.label(resultVol > thresh)
    stats = measure.regionprops(labelVol)
    print len(stats) 

    # GephyrinBD 
    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/Antibody comparisons/KDM-SYN-161213/Gephyrin BD/';
    tiffpath_base2 = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/result_tiffs/antibody_comparisons/KDM-SYN-161213/Gephyrin BD/';
    
    foldernames = ['GephyrinBD.tif', 'GAD.tif']

    fn = base_dir + foldernames[1]
    GAD = da.imreadtiff(fn)
    fn = base_dir + foldernames[0]
    GephyrinBD = da.imreadtiff(fn)

    synapticVolumes = {'presynaptic': [GAD],
                       'postsynaptic': [GephyrinBD]}

    fn = tiffpath_base2 + 'GephyrinBD_result.mat'
    resultVol = syn.getSynapseDetections(synapticVolumes, query); 
    scipy.io.savemat(fn, {'resultVol':resultVol} )

    labelVol = measure.label(resultVol > thresh)
    stats = measure.regionprops(labelVol)
    print len(stats) 

    return resultVol; 

def vglut1_pairwise(): 
    """
    """

    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/Antibody comparisons/KDM-SYN-090210/VGluT1/';
    tiffpath_base = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/result_tiffs/antibody_comparisons/KDM-SYN-090210/VGluT1/';

    foldernames = ['VGlut1GP1stA.tif', 'VGlut1M1stA.tif', 'synapsin1stA.tif']

    minSpanList = [2, 2]

    fn = base_dir + foldernames[2]
    synapsin1stA = da.imreadtiff(fn)
    fn = base_dir + foldernames[0]
    VGlut1GP1stA = da.imreadtiff(fn)

    synapticVolumes = {'presynaptic': [VGlut1GP1stA, synapsin1stA],
                        'postsynaptic': []}

    query = {'preIF': [], 'preIF_z': [2, 2],
            'postIF': [], 'postIF_z': []}

    resultVol = syn.getSynapseDetections(synapticVolumes, query); 
    scipy.io.savemat('VGlut1GP1stA_result.mat', {'resultVol':resultVol} )
    
    labelVol = measure.label(resultVol > 0.9)
    stats = measure.regionprops(labelVol)
    print len(stats) 

    fn = base_dir + foldernames[2]
    synapsin1stA = da.imreadtiff(fn)
    fn = base_dir + foldernames[1]
    VGlut1M1stA = da.imreadtiff(fn)

    synapticVolumes = {'presynaptic': [VGlut1M1stA, synapsin1stA],
                       'postsynaptic': []}

    fn = tiffpath_base + 'VGlut1M1stA.mat'
    resultVol = syn.getSynapseDetections(synapticVolumes, query); 
    scipy.io.savemat(fn, {'resultVol':resultVol} )

    labelVol = measure.label(resultVol > 0.9)
    stats = measure.regionprops(labelVol)
    print len(stats) 

    return resultVol; 



def cav31_pairwise(): 
    """
    """


    base_dir = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/Antibody comparisons/KDM-MH-131023/Cav3.1/';
    tiffpath_base = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/antibodyanalysis/result_tiffs/antibody_comparisons/KDM-MH-131023/Cav3.1/';

    foldernames = ['Cav31M_1st_A.tif', 'Cav31R_1st_A.tif', 'VGluT1_1st_A.tif']

    minSpanList = [2, 2]

    fn = base_dir + foldernames[2]
    VGluT1_1st_A = da.imreadtiff(fn)
    fn = base_dir + foldernames[0]
    Cav31M_1st_A = da.imreadtiff(fn)

    synapticVolumes = {'presynaptic': [VGluT1_1st_A],
                        'postsynaptic': [Cav31M_1st_A]}

    query = {'preIF': [], 'preIF_z': [2],
            'postIF': [], 'postIF_z': [2]}

    resultVol = syn.getSynapseDetections(synapticVolumes, query); 
    scipy.io.savemat('Cav31M_1st_A_result.mat', {'resultVol':resultVol} )
    
    labelVol = measure.label(resultVol > 0.9)
    stats = measure.regionprops(labelVol)
    print len(stats) 

    fn = base_dir + foldernames[2]
    VGluT1_1st_A = da.imreadtiff(fn)
    fn = base_dir + foldernames[1]
    Cav31R_1st_A = da.imreadtiff(fn)

    synapticVolumes = {'presynaptic': [VGluT1_1st_A],
                       'postsynaptic': [Cav31R_1st_A]}

    fn = tiffpath_base + 'Cav31R_1st_A.mat'
    resultVol = syn.getSynapseDetections(synapticVolumes, query); 
    scipy.io.savemat(fn, {'resultVol':resultVol} )

    labelVol = measure.label(resultVol > 0.9)
    stats = measure.regionprops(labelVol)
    print len(stats) 

    return resultVol; 


