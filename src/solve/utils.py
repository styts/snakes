from src.solve.solver import Solver
from src.logic.state import State
import cloud, os
from multiprocessing import Process

def _process(json_data,use_cloud,quit_on_first=True, ignore_pickle=False, debug_info=None):
    slv = Solver(quit_on_first=quit_on_first, use_cloud=use_cloud, ignore_pickle=ignore_pickle, debug_info=debug_info)
    st = State()

    st.load_from_json(json_data)
    slv.set_state(st)

    filelist = []
    if use_cloud:
        # fetch remote pickle if exists
        filelist = cloud.files.list()
        pf = '%s.pickle' % st.__hash__()
        pffull = os.path.join('data','graphs', pf)
        if pf in filelist:
            cloud.files.get(pf, pffull)
    
    sols = slv.solve()

    if use_cloud: # upload solution
        cloud.files.put(pffull, pf)
    
    # the image, save it to cloud
    png = '%s.png' % st.__hash__()
    pngfull = os.path.join('data', 'graphs', png)
    if png not in filelist: # irrelevent? FIXME , pngfull does not exist, since we never synced it.
        slv.draw_graph(filename=pngfull)
        if use_cloud:
            cloud.files.put(pngfull, png)
    else:
        print "Graph Image %s already exists" % pngfull

    ret = (slv.l_shortest)
    return ret
    

def process_json(json_data, use_cloud, quit_on_first=False, ignore_pickle=False, debug_info=None):
    """In the cloud or locally:
    Invoke Solver
    Populate and solve graph (or load it from tmp/ if it''s there)
    Save graph image into graphs/"""
    ret = None
    if not use_cloud:
        # maybe start a new process here...?
        #pygame = None
        ret = _process(json_data, use_cloud, quit_on_first=quit_on_first, ignore_pickle=ignore_pickle, debug_info=debug_info)
        # does not work on my mac :/
        #p = Process(target=_process, args=(json_data, use_cloud, quit_on_first, quit_on_first))
        #p.start()
        #p.join()
        
    else:
        ret = cloud.call(_process, json_data, quit_on_first=quit_on_first, use_cloud=True, ignore_pickle=ignore_pickle, _type="f2", _env='pygame_env' )

    return ret

# def process_all_maps():
#     # take the .json file in maps/ and process them in the cloud, saving the graphs(.pickle & .png) in bucket "graphs"
#     import glob, os, cloud
#     from src.solve.utils import process_json

#     def read_json(fn):
#         json_data = open(fn,'r').readlines()
#         json_data = "\n".join(json_data)
#         return json_data
        
#     maps = glob.glob(os.path.join(os.getcwd(),'data','maps')+"/*.json")
#     jsons = map(read_json, maps)
#     jobs = cloud.map(process_json, jsons, use_cloud=True, _env='pygame_env', _type="c2", _vol=['graphs'])
#     print "PiCloud Jobs:", jobs

#     # sync home the results
#     import cloud
#     cloud.volume.sync("graphs:","graphs/")
