from src.solve.solver import Solver
from src.logic.state import State
import cloud


def _process(json_data, use_cloud):
    slv = Solver(quit_on_first=False, use_cloud=use_cloud)
    st = State()

    st.load_from_json(json_data)
    slv.set_state(st)
    
    cloud.volume.sync('graphs:', 'tmp/') # sync .pickles from bucket, to prevent unnecessary computation

    sols = slv.solve()

    cloud.volume.sync('tmp/', 'graphs:') # sync .pickle to bucket (the drawing may crash, so sync before it)

    slv.draw_graph(filename='%s%s.png' % ("tmp/", st.__hash__()))
    
    cloud.volume.sync('tmp/', 'graphs:') # sync .png to bucket

def process_json(json_data, use_cloud=True, use_temp=True):
    """In the cloud or locally:
    Invoke Solver
    Populate and solve graph (or load it from tmp/ if it''s there)
    Save graph image into graphs/"""
    if not use_cloud:
        ret = _process(json_data,use_cloud)
    else:
        ret = cloud.call(_process, json_data, use_cloud=use_cloud, _env='pygame_env', _vol=['graphs'])

    return ret

def process_all_maps():
    # take the .json file in maps/ and process them in the cloud, saving the graphs(.pickle & .png) in bucket "graphs"
    import glob, os, cloud
    from src.solve.utils import process_json

    def read_json(fn):
        json_data = open(fn,'r').readlines()
        json_data = "\n".join(json_data)
        return json_data
        
    maps = glob.glob(os.path.join(os.getcwd(),'data','maps')+"/*.json")
    jsons = map(read_json, maps)
    jobs = cloud.map(process_json, jsons, use_cloud=True, _env='pygame_env', _type="c2", _vol=['graphs'])
    print "PiCloud Jobs:", jobs

    # sync home the results
    import cloud
    cloud.volume.sync("graphs:","graphs/")