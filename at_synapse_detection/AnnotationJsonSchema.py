import argschema
import numpy as np

class NumpyArray(argschema.fields.List):
    def _deserialize(self, value, attr, obj):
        mylist = super(NumpyArray, self)._serialize(value, attr, obj)
        return np.array(mylist)

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        return argschema.fields.List._serialize(
            self, value.tolist(), attr, obj)

class Area(argschema.schemas.mm.Schema):
    tileIds = NumpyArray(argschema.fields.Str,
        description='N long list of tileIds for each local point')
    local_path = NumpyArray(argschema.fields.List(argschema.fields.Float),
        description='Nx2 numpy array of local points')
    global_path = NumpyArray(argschema.fields.List(argschema.fields.Float),
        description='Nx2 numpy array of global coordinates')
    z = argschema.fields.Float(required=False,description="z value of tileId")

class AreaList(argschema.schemas.mm.Schema):
    oid = argschema.fields.Str()
    id = argschema.fields.Int(required=True)
    areas = argschema.fields.Nested(Area, many=True)

class AnnotationFile(argschema.schemas.mm.Schema):
    area_lists = argschema.fields.Nested(AreaList, many=True)