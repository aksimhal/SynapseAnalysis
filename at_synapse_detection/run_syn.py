import json
import renderapi
import scipy
import numpy as np
from scipy.stats import norm
from renderapps.module.render_module import RenderModule
from scipy import signal
import csv

import matplotlib.pyplot as plt

import SynapseDetection as syn
import renderDataAccess as rda


# Render settings for Galicia@Duke
args = {
    'render': {
        'host': 'http://152.3.214.113',
        'port': 8080,
        'owner': 'Anish',
        'project': 'M247514_Rorb_1',
        'client_scripts': '/home/anish/Connectome/render/render-ws-java-client/src/main/scripts'
    },
    'log_level': 'DEBUG'}

# Create Render Module Object
render_args = args['render']
mod = RenderModule(input_data=args, args=[])
# 'stacks' - list of channel names
stacks = mod.render.run(renderapi.render.get_stacks_by_owner_project)
# keep stacks with current alignment
stackList = stacks[23:]

# Dimensions 
xstart = 4000
ystart = 4000
deltaX = 10000
deltaY = 10000
startZ = 5
endZ = 15

volDimensions = {'xstart': xstart, 'ystart': ystart, 'deltaX': deltaX,
                 'deltaY': deltaY, 'startZ': startZ, 'endZ': endZ}

# Data access parameters 
scale = 0.03
minIntensity = 0
maxIntensity = 5000
intensityrange = [minIntensity, maxIntensity]

fileName = 'testqueries.csv'
listOfQueries = syn.createQueries(fileName)
query = listOfQueries[0]
synapticVolumes = rda.getChannelVolumes(query, volDimensions, scale, intensityrange, mod)

resultVol = syn.getSynapseDetections(synapticVolumes, query); 

plt.imshow(resultVol[:, :, 4], cmap='gray')
plt.colorbar()
plt.show()
