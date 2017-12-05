import numpy as np 
import synaptogram
from renderapps.module.render_module import RenderModule
import renderapi
import matplotlib.pyplot as plt
import dataAccess as da
import SynapseDetection as syn 
import os
import json 





# Render settings for Galicia@Duke
args={
    'render':{
    'host':'http://152.3.214.113',
    'port':8080,
    'owner':'Anish',
    'project':'M247514_Rorb_1',
    'client_scripts':'/home/anish/Connectome/render/render-ws-java-client/src/main/scripts'
},
'log_level':'DEBUG'}

# Create Render Module Object 
mod = RenderModule(input_data = args,args=[])

filepath = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/collman17/Site3Align2Stacks/';
stackList = ['PSD95', 'synapsin', 'VGlut1', 'GluN1', 'GABA', 'Gephyrin']

data = json.load(open('json_annotations/m247514_Site3Annotation_MN_global_v2.json'))
listOfSynapses = data['area_lists']

win_xy = 4
win_z = 1
filepath = '/Users/anish/Documents/Connectome/Synaptome-Duke/data/collman17/Site3Align2Stacks/';
stackList = ['PSD95', 'synapsin', 'VGlut1', 'GluN1', 'GABA', 'Gephyrin']
showProb = True
textXOffset = 0
textYOffset = 5

for synapse in listOfSynapses: 
    bbox = synaptogram.getAnnotationBoundingBox2(synapse, render_args)
    bbox = synaptogram.transformSynapseCoordinates(bbox)
    expandedBox = synaptogram.expandBoundingBox(bbox, win_xy, win_z)
    
    synapseOutlinesDict = synaptogram.getAnnotationOutlines(synapse, render_args)
    synapseOutlinesDict = synaptogram.transformSynapseOutlinesDict(synapseOutlinesDict)
    
    filename = os.path.join('{}.png'.format(synapse['oid']))
    
    img = synaptogram.getSynaptogramFromFile(bbox, win_xy, win_z, stackList, showProb, filepath);
    synaptogram.plotOutlinesOnImg(img, synapseOutlinesDict, expandedBox, filename, stackList, textXOffset, textYOffset)
    print filename