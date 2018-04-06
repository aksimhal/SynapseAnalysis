# Synaptic Antibody Characterization Tool
This repository hosts the Synaptic Antibody Characterization Tool (SACT) - a framework to evaluate synaptic antibodies for array tomography (AT) applications.  Paper: https://www.biorxiv.org/content/early/2018/02/01/258756


## Installation Guide 
Thanks for trying out the SACT.  The tool is contained in the "SynapseAnalysis" python module; the following steps are recomended to install.  It is strongly advised to install anaconda and running the tool in a virutal environment. 

#### Step 1
download miniconda with python 3.6 from https://conda.io/miniconda.html

Change permission of file, if needed: 
`chmod u+x Miniconda3-latest-Linux-x86_64.sh`

Run installation script (different script name for different operating systems): 
`./Miniconda3-latest-Linux-x86_64.sh`

Create virtual environment: 
`conda create --name synapse_analysis`

Activate virtual environment: 
`source activate synapse_analysis`

Install dependencies: 
```
conda install numpy
conda install scipy
conda install scikit-image
conda install shapely
conda install --channel https://conda.anaconda.org/menpo opencv3
conda install pandas
conda install xlsxwriter
conda install pillow
conda install xlrd
```

These two repositories are needed for Allen Institute data: 
```
git clone https://github.com/AllenInstitute/argschema.git
git clone https://github.com/fcollman/render-python.git
```
Navigate to these directories and install (`python setup.py install`)


Clone the repository: 
```
git clone https://github.com/aksimhal/SynapseAnalysis.git
```

Install in developer mode since the repository is in active development. 
`python setup.py develop`


## User Guide 
The first step is to install the data

## Data Location 
[insert dropbox link]
