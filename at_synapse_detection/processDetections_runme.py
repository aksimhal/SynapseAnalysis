import numpy as np
import processDetections as pd
import SynapseDetection as syn 
import os 

def main():
    
    # Example use case of processing detections
    # Load probability map 
    metadataFN = 'metadatatest.json'
    metadata = syn.loadMetadata(metadataFN)
    n = 0 
    fn = os.path.join(metadata['datalocation'], 'resultVol')
    fn = fn + str(n) + '.npy'

    resultVol = np.load(fn)

    resolution = metadata['resolution']
    thresh = metadata['thresh']
    outputFN = 'test.json'

    pd.probMapToJSON(resultVol, thresh, outputFN, resolution)

if __name__ == '__main__':
    main()



