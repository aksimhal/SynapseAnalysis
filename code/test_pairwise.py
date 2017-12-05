import json
import renderapi
import scipy
import numpy as np
from scipy.stats import norm
from render_module import RenderModule
from scipy import signal
import dataAccess as da
import pairwiseComparisons as pw

reload(pw)

def main():
    #resultVol = pw.synapsin_pairwise()
    resultVol = pw.psd95_pairwise();
    #resultVol = pw.gephyrin_pairwise(); 
    #resultVol = pw.vglut1_pairwise(); 
    #resultVol = pw.cav31_pairwise(); 


if __name__ == '__main__':
    main()