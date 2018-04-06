# Synaptic Antibody Characterization Tool
This repository hosts the Synaptic Antibody Characterization Tool (SACT) - a framework to evaluate synaptic antibodies for array tomography (AT) applications.  Paper: https://www.biorxiv.org/content/early/2018/02/01/258756


## Installation Guide 
Thanks for trying out the SACT.  The tool is contained in the "SynapseAnalysis" python module; the following steps are recomended to install.  It is strongly advised to install Anaconda and run the tool in a virutal environment. 

#### Step 1
Download miniconda, which is a slimmed down version of Anaconda with Python 3.6 from https://conda.io/miniconda.html

If you're using linux, you might have to change permission of file.
`chmod u+x Miniconda3-latest-Linux-x86_64.sh`

Run installation script (different script name for different operating systems): 
`./Miniconda3-latest-Linux-x86_64.sh`

#### Step 2
Create virtual environment: 
`conda create --name synapse_analysis`

Activate virtual environment: 
`source activate synapse_analysis`

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
`python setup.py develop`

The 'user guide' section contains a link to a sample runme to see if things installed alright. 


## User Guide 
After installing the tool, navigate to https://github.com/aksimhal/SynapseAnalysis/tree/master/data/SACT_example/ and open runme.py. To run this file, download the sample data from here: .  First, open the file and change the filepath to the location of the dowloaded data.  Notes on how the tool works are included in the comments. 

To run the data presented in the paper, navigate to https://github.com/aksimhal/SynapseAnalysis/tree/master/data/antibody_analysis.  The readme file in that directory explains what each file is for and what's needed to run it. 

Please email me (Anish) at anish.simhal@duke.edu if you have any questions. 







## Data Location 
The data used for the paper is located here: https://www.dropbox.com/sh/iwawyffnynw1hod/AAB2T45x1EEWr7ZAr3BiiiIYa?dl=0
