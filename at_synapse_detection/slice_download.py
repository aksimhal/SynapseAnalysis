
# coding: utf-8

# In[ ]:

import os
from renderapps.module.render_module import RenderModule
import renderapi
from PIL import Image
#get_ipython().magic(u'matplotlib notebook')
import matplotlib.pyplot as plt
import sys
import numpy as np


# In[ ]:

args={
    'render':{
    'host':'localhost',
    'port':8080,
    'owner':'Anish',
    'project':'M247514_Rorb_1',
    'client_scripts':'/home/anish/Connectome/render/render-ws-java-client/src/main/scripts'
},
'log_level':'DEBUG'}
mod = RenderModule(input_data = args,args=[])
stacks = mod.render.run(renderapi.render.get_stacks_by_owner_project)


# In[ ]:

xstart = 0
xend = 231424
xwidth = xend - xstart

ystart = 0
yend = 111104
yheight = yend - ystart


# In[ ]:

for stack in stacks[29:]:
    stackname = str(stack)
    print stackname
    base_str = '/data/anish/Synaptome/M247514_Rorb_1/pngs/'
    
    for sliceind in range(0, 102):
        #img=renderapi.image.get_bb_image(stack,sliceind,207561,-10403,15315,15088,scale=0.03,render=mod.render)
        img=renderapi.image.get_bb_image(stack,sliceind,xstart,ystart,xwidth,yheight,scale=0.03,
                                         minIntensity = 0, maxIntensity = 5000, render=mod.render)
        img = img[:, :, 0]
        im = Image.fromarray(img, 'L')
        fn_str = base_str + stackname + '-' + '{:04d}'.format(sliceind) + '.png'
        print fn_str
        im.save(fn_str)


