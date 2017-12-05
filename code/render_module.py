from json_module import JsonModule,ModuleParameters,InputDir
import marshmallow as mm
import renderapi
import os
import subprocess

class RenderClientParameters(mm.Schema):
    host = mm.fields.Str(required=True,metadata={'description':'render host'})
    port = mm.fields.Int(required=True,metadata={'description':'render post integer'})
    owner = mm.fields.Str(required=True,metadata={'description':'render default owner'})
    project = mm.fields.Str(required=True,metadata={'description':'render default project'})
    client_scripts = mm.fields.Str(required=True,metadata={'description':'path to render client scripts'})
class RenderParameters(ModuleParameters):
    render = mm.fields.Nested(RenderClientParameters)

class RenderTrakEM2Parameters(RenderParameters):
    renderHome = InputDir(required=True,metadata={'description':'root path of standard render install'})

class RenderModule(JsonModule):
    def __init__(self,schema_type=None,*args,**kwargs):
        if schema_type is None:
            schema_type = RenderParameters
        super(RenderModule,self).__init__(schema_type = schema_type,*args,**kwargs)
        self.render=renderapi.render.connect(**self.args['render'])

class TrakEM2RenderModule(RenderModule):
    def __init__(self,schema_type=None,*args,**kwargs):
        if schema_type is None:
            schema_type = RenderTrakEM2Parameters
        super(TrakEM2RenderModule,self).__init__(schema_type=schema_type,*args,**kwargs)
        jarDir = os.path.join(self.args['renderHome'],'render-app','target')
        renderjarFile = next(os.path.join(jarDir,f) for f in os.listdir(jarDir) if f.endswith('jar-with-dependencies.jar'))
        self.trakem2cmd = ['java','-cp',renderjarFile,'org.janelia.alignment.trakem2.Converter']


    def convert_trakem2_project(self,xmlFile,projectPath,json_path):
        cmd = self.trakem2cmd + ['%s'%xmlFile,'%s'%projectPath,'%s'%json_path]
        proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        while proc.poll() is None:
            line = proc.stdout.readline()
            if 'ERROR' in line:
                self.logger.error(line)
            else:    
                self.logger.debug(line)
        while proc.poll() is None:
            line = proc.stdout.readline()
            if 'ERROR' in line:
                self.logger.error(line)
            else:
                self.logger.debug(line)    



if __name__ == '__main__':
    example_input={
        "render":{
            "host":"ibs-forrestc-ux1",
            "port":8080,
            "owner":"NewOwner",
            "project":"H1706003_z150",
            "client_scripts":"/pipeline/render/render-ws-java-client/src/main/scripts"
        }
    }
    module = RenderModule(input_data=example_input)
    module.run()

    bad_input={
        "render":{
            "host":"ibs-forrestc-ux1",
            "port":'8080',
            "owner":"Forrest",
            "project":"H1706003_z150",
            "client_scripts":"/pipeline/render/render-ws-java-client/src/main/scripts"
        }
    }
    module = RenderModule(input_data=bad_input)
    module.run()