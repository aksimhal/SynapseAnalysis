# Synaptic Antibody Characterization Tool
This repository hosts the Synaptic Antibody Characterization Tool (SACT) - a framework to evaluate synaptic antibodies for array tomography (AT) applications.  Paper: <https://www.biorxiv.org/content/early/2018/03/14/258756>

This webpage contains the following: 
    - Installation Guide 
    - User Guide 
    - Notes
    - Data location 

This repository is maintained by Anish - email anish.simhal@duke.edu if you have any questions. 


## Installation Guide 
Thanks for trying out the SACT.  The following steps are recomended to install.  It is strongly advised to install Anaconda and run the tool in a virutal environment. Steps 1 and 2 explain how to set up Anaconda, a python environment management system. Step 3 installs all the dependencies needed.  Steps 4 & 5 install the actual tool itself.  

#### Step 1
Download miniconda, which is a slimmed down version of Anaconda with Python 3.6 from <https://conda.io/miniconda.html>.  The tool was written in Python 3.6 and is not backwards compatible with Python 2.7. 

(optional) If you're using linux, you might have to change permission of install file. 
```
chmod u+x Miniconda3-latest-Linux-x86_64.sh
```
Run installation script (different script name for different operating systems): 
```
./Miniconda3-latest-Linux-x86_64.sh
```

#### Step 2
Create virtual environment: 
```
conda create --name synapse_analysis
```

Activate virtual environment: 
```
source activate synapse_analysis
```

#### Step 3
Install dependencies: 
```
conda install numpy scipy scikit-image shapely pandas xlsxwriter pillow xlrd
conda install --channel https://conda.anaconda.org/menpo opencv3
```

#### Step 4
Clone the repository: 
```
git clone https://github.com/aksimhal/SynapseAnalysis.git
```

#### Step 5
Install in developer mode since the repository is in active development. 
```
python setup.py develop
```

The 'user guide' section contains a link to a sample runme to see if things installed alright. 

## User Guide 
Prior to running the program, the user has to create a runme.py file, similar to the example file linked to below.  In this file, you have to create 'queries' - python dictionary objects with specify where the data is located, which channels are presynaptic and which ones are postsynaptic, and how many slices each channel's puncta should span.  Then, you have to specify which channel is the 'antibody of interest' and which antibodies are the 'reference antibodies.' The antibody of interest is the one you are trying to develop (ie PSD-95) and the 'reference antibody' is another anitbody (ie synapsin) used to determined colocalization or adjacency.  Once these have been established, the main function runs the tool and outputs an excel sheet with the desired results. 

## Notes - Sample Runme
After installing the tool, navigate to <https://github.com/aksimhal/SynapseAnalysis/tree/master/data/SACT_example/> and open runme.py. Instructions on how to use the runme are included in the readme.md file included in the folder. 

To run the data presented in the paper, navigate to <https://github.com/aksimhal/SynapseAnalysis/tree/master/data/antibody_analysis.>  The readme file in that directory explains what each file is for and what's needed to run it. 



## Data Location 
The data used for the paper is located here: <https://www.dropbox.com/sh/iwawyffnynw1hod/AAB2T45x1EEWr7ZAr3BiiiIYa?dl=0>
