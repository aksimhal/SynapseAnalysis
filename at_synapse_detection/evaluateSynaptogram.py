import os
from functools import partial
from argschema import ArgSchema, ArgSchemaParser
import argschema
import marshmallow as mm
from renderapps.TrakEM2.AnnotationJsonSchema import AnnotationFile
import json
import pandas as pd
example_json={
    "EM_annotation_json":"/Users/forrestc/Site3Align2/m247514_Site3Annotation_MN_global_v2.json",
    "LM_annotation_json":"/Users/forrestc/SynapseAnalysis/data/M247514_Rorb_1/Site3Align2/results/resultVol0.json",
    "EM_metadata_csv":"/Users/forrestc/Site3Align2/MNSite3Synaptograms_v2.csv",
    "LM_metadata_file":"/Users/forrestc/SynapseAnalysis/data/M247514_Rorb_1/Site3Align2/site3_metadata.json",
    "EM_pregaba_column":"pregaba(F)",
    "EM_not_synapse_column":"ConsensusNotSynapse"
}

class EvaluateSynapseDetectionParameters(ArgSchema):
    EM_annotation_json = argschema.fields.InputFile(required=True,
        description='file path to EM annotation file')
    LM_annotation_json = argschema.fields.InputFile(required=True,
        description='file path to LM annotation results') 
    EM_metadata_csv = argschema.fields.InputFile(required=True,
        description='file path to EM metadata csv')
    EM_inclass_column = argschema.fields.Str(required=True,
        description="name of column in metadata that indicates whether synapse is gabaergic") 
    EM_not_synapse_column = argschema.fields.Str(required=True,
        description="name of column that indicates whether this annotation should be ignored")

def load_annotation_file(annotation_path):
    with open(annotation_path,'r') as fp:
            annotation_d = json.load(fp)
    schema = AnnotationFile()
    annotations,errors = schema.load(annotation_d)        
    assert(len(errors)==0)
    return annotations

class EvaluateSynapseDetection(ArgSchemaParser):
    default_schema = EvaluateSynapseDetectionParameters

    def run(self):
        print(json.dumps(self.args,indent=4))
        EM_annotations = load_annotation_file(self.args['EM_annotation_json'])
        LM_annotations = load_annotation_file(self.args['LM_annotation_json'])
        
        df = pd.read_csv(self.args['EM_metadata_csv'])


        self.logger.error('WARNING NEEDS TO BE TESTED, TALK TO FORREST IF BROKEN')


if __name__ == "__main__":
    mod = EvaluateSynapseDetection(input_data= example_json)
    mod.run()
