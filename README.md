# SynapseAnalysis
Probabilistic synapse detection and evaluation for Allen Institute array tomography data

## Installation Guide 

We recommend installing anaconda and running this in a virutal environment. 


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
```

These two repositories are needed for Allen Institute data: 
```
git clone https://github.com/AllenInstitute/argschema.git
git clone https://github.com/fcollman/render-python.git
```

Clone the repository: 
```
git clone https://github.com/aksimhal/SynapseAnalysis.git
```
