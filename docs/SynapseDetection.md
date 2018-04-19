# Probabilistic Synapse Detection
This repository hosts the Probabilistic Synapse Detector - a framework to detect synapses for array tomography (AT) applications.  Paper: <http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005493>.

This webpage contains the following: 
    - Installation Guide 
    - User Guide 
    - Notes

This repository is maintained by Anish - email anish.simhal@duke.edu if you have any questions. 


## Installation Guide 
Thanks for trying this out!  The following steps are recomended to install.  It is strongly advised to install Anaconda and run the tool in a virutal environment. Steps 1 and 2 explain how to set up Anaconda, a python environment management system. Step 3 installs all the dependencies needed.  Steps 4 & 5 install the actual tool itself.  

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
Prior to running the program, the user has to create a runme.py file, similar to the example file linked to below.  In this file, you have to create 'queries' - python dictionary objects with specify where the data is located, which channels are presynaptic and which ones are postsynaptic, and how many slices each channel's puncta should span.  Once these have been established, the main function runs the tool and outputs an excel sheet with the desired results. 

## Notes - Sample Runme
After installing the tool, navigate to <https://github.com/aksimhal/SynapseAnalysis/tree/master/data/example/> and open `example_runme.py`. Instructions on how to use the runme are included in the readme.md file included in the folder. 


