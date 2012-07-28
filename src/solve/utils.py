from src.solve.solver import Solver
from src.logic.state import State

def _process(json_data, use_cloud):
    slv = Solver(quit_on_first=False,use_cloud=use_cloud)
	st = State()

    state.load_from_json(json_data)
    slv.set_state(st)
    sols = slv.solve()
    slv.draw_graph(filename='graph-%s.png' % st.__hash__())


def process_json(json_data, use_cloud=True, use_temp=True):
	"""In the cloud or locally:
	Invoke Solver
	Populate and solve graph (or load it from tmp/ if it's there)
	Save graph image into graphs/
	"""


	if not use_cloud:
        _process(json_data,use_cloud)
    else:
        pid = cloud.call(process, json_data, use_cloud=use_cloud, _env='pygame_env')
        #print pid

	# TODO
	#pass


def process_all_maps():
	#TODO
	pass