"""
Antibody Analysis 
"""
import numpy as np
from skimage import measure
from at_synapse_detection import dataAccess as da
from at_synapse_detection import SynapseDetection as syn

def getdatavolume(synaptic_volumes, resolution):
    """
    compute volume

    Parameters
    -------------
    synaptic_volumes : dict
    resolution : dict 

    Return
    --------------
    volume_um3 : double
    """

    res_xy_nm = resolution['res_xy_nm']
    res_z_nm = resolution['res_z_nm']

    # Compute Volume
    if len(synaptic_volumes['presynaptic']) > 0: 
        volume_um3 = np.prod(synaptic_volumes['presynaptic'][0].shape) \
        * (res_xy_nm/1000) * (res_z_nm/1000)
    
    elif len(synaptic_volumes['postsynaptic']) > 0: 
        volume_um3 = np.prod(synaptic_volumes['postsynaptic'][0].shape) \
        * (res_xy_nm/1000) * (res_z_nm/1000)
        
    return volume_um3
    


def run_ab_analysis(synaptic_volumes, query, thresh, resolution):
    """
    Run AB Analysis

    Parameters
    -----------
    synaptic_volumes : dict
    query : dict 
    thresh : float 
    resolution : dict 

    Returns
    -----------
    ab_measures : dict
    """

    # MEASURES
    # - Puncta Density
    # - Average punctum size 
    # - Standard deviation of the size 
    # - Synapse density
    # - Target Specificity Ratio (tsr)

    # Get data volume
    volume_um3 = getdatavolume(synaptic_volumes, resolution)

    # Data
    presynaptic_volumes = synaptic_volumes['presynaptic']
    postsynaptic_volumes = synaptic_volumes['postsynaptic']

    # Compute Probability Maps 
    for n in range(0, len(presynaptic_volumes)):
        presynaptic_volumes[n] = syn.getProbMap(presynaptic_volumes[n])

    for n in range(0, len(postsynaptic_volumes)):
        postsynaptic_volumes[n] = syn.getProbMap(postsynaptic_volumes[n])
        
    # Compute number of puncta 
    labelVol = measure.label(resultVol > 0.9)


    # %     cc = bwconncomp(volumesCell{1} > threshList(threshItr), 26);
    # %     stats = regionprops(cc, 'Area');
    # %     areaList = zeros(length(stats), 1);
    # %     for n=1:length(stats)
    # %         areaList(n) = stats(n).Area;
    # %     end
    # %
    # %     metric{punctaSize, threshItr} = cc.NumObjects;
    # %     metric{punctaStdev, threshItr} = mean(areaList);



    # numOfPunctaDetected = 0; 
    # numOfSynapsesDetected = 0; 

    # convWindow = ones(2, 1);

    # for n = 1:length(volumesCell)
    #     volumesCell{n} = convolveVolume(volumesCell{n}, convWindow);
    # end

    # for n = 1:length(volumesCell)
    #     if (minSpanList(n) == 2)
    #         factorVol = computeFactor_2(volumesCell{n});
    #         volumesCell{n} = volumesCell{n} .* factorVol;
            
    #     elseif(minSpanList(n) == 3)
    #         factorVol = computeFactor(volumesCell{n});
    #         volumesCell{n} = volumesCell{n} .* factorVol;
    #     end
    # end

    # % Get number of antibody blobs
    # for threshItr = 1:length(threshList)
    #     cc = bwconncomp(volumesCell{1} > threshList(threshItr), 26);
        
    #     metric{punctaDensityInd, threshItr} = cc.NumObjects ./ volumeUm3;
    #     numOfPunctaDetected = cc.NumObjects;

    #     stats = regionprops(cc, 'Area', 'Centroid');
    #     areaList = zeros(length(stats), 1);
    #     for n=1:length(stats)
    #         areaList(n) = stats(n).Area;
    #     end
        
    #     metric{punctaSizeInd, threshItr} = mean(areaList);
    #     metric{punctaStdevInd, threshItr} = std(areaList);
    # end



    # postsynapticVolumes = cell(sum(prepostList), 1);
    # presynapticVolumes = cell(length(prepostList) - sum(prepostList), 1);

    # preItr = 1;
    # postItr = 1;

    # for n = 1:length(volumesCell)
    #     if (prepostList(n) == 1)
    #         postsynapticVolumes{postItr} = volumesCell{n};
    #         postItr = postItr + 1;
    #     else
    #         presynapticVolumes{preItr} = volumesCell{n};
    #         preItr = preItr + 1;
    #     end
    # end

    # baseThresh = 0.5;

    # if (isempty(postsynapticVolumes))
    #     resultVol = combineVolumes_oneside(presynapticVolumes{1}, presynapticVolumes(2:end), ...
    #         baseThresh, edge_win, search_win);
        
    # elseif (isempty(presynapticVolumes))
    #     resultVol = combineVolumes_oneside(postsynapticVolumes{1}, postsynapticVolumes(2:end), ...
    #         baseThresh, edge_win, search_win);
        
    # elseif (length(postsynapticVolumes) > 1)
    #     resultVol = combineVolumes_quadch(postsynapticVolumes{1}, presynapticVolumes, ...
    #         postsynapticVolumes(2:end), baseThresh, edge_win, search_win);
    # else
    #     resultVol = combineVolumes2(postsynapticVolumes{1}, presynapticVolumes, ...
    #         baseThresh, edge_win, search_win);
    # end


    # for threshItr=1:length(threshList)
    #     resultThresholded = resultVol > threshList(threshItr);
    #     cc = bwconncomp(resultThresholded, 26);
    #     disp(cc.NumObjects); 
    #     %synapse density
    #     metric{synapseDensityInd, threshItr} = cc.NumObjects / volumeUm3;
    #     %Number of synaptic blobs
    #     metric{numDetectionInd, threshItr} = cc.NumObjects;
    #     numOfSynapsesDetected = cc.NumObjects;

    #     %     stats = regionprops(cc, 'Area', 'Centroid');
    #     %     areaList = zeros(length(stats), 1);
    #     %     for n=1:length(stats)
    #     %         areaList(n) = stats(n).Area;
    #     %     end
    #     %
    #     %     metric{punctaSizeInd, threshItr} = mean(areaList);
    #     %
    #     %     metric{punctaStdevInd, threshItr} = std(areaList);
        
    #     if (savetifs) 
    #         writeTIFFStacks(resultThresholded, tiffpath); 
    #     end
        
    # end

    # metric{precisionInd, :} = numOfSynapsesDetected ./ numOfPunctaDetected;


