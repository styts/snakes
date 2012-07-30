from src.logic.map import Map
from src.logic.snake import Snake
from src.logic.state import State
from src.engine.utils import SNAKE_VALUES
import os
import hashlib
import time

def save_state(state):
    n_s = len(state.snakes)
    n_n = state.map.n
    str_md5 = state.__hash__()
    name = "n%s-s%s-%s" % (n_n,n_s,str_md5)
    #state.save_to_image("data/maps/%s.png" % name)
    state.save_to_json("data/maps/%s.json" % name)

def remove_map_file(levelname):
    """Not used"""
    # """used by RALT+mouseclick on ToolbarButton"""
    # pathname = os.path.abspath(os.path.join("data", "maps", levelname))
    # os.remove(pathname)
    # print "removed map", pathname
    pass

def edit_map(state,event,button):
    if not state:
        return False
    t = state.map.get_tile_at(event.pos[0],event.pos[1])
    if not t:
        return False
    update_snake = button.value in SNAKE_VALUES
    coords = state.map.get_coords()
    if not update_snake:
        coords[t.x][t.y] = button.value
    m = Map(coordinates=coords)
    coords_snakes = state.map.get_coords(snakes=True)
    if update_snake or button.value == '0':
        coords_snakes[t.x][t.y] = button.value
    ss = Snake.make_snakes(m,coords_snakes)
    s = State(m,ss)
    s.save_to_json("data/maps/tempstate.json")
    return True

def clean_map(app,n):
    """used in the toolbar, it sets map to a clean square of size n x n"""
    coords = {"tiles" : [], "snakes": []}
    for i in xrange(n):
        coords['tiles'].append([])
        coords['snakes'].append([])
        for j in xrange(n):
            v = 1
            coords['tiles'][i].append(v)
            coords['snakes'][i].append(v)
    reset_state(app,coords=coords)

def reset_state(ingameState,level_name=None,coords=None):
    if ingameState.app.screen != None:
        screen = ingameState.app.screen
    else:
        screen = None
    if not coords:
        if not level_name:
            level_name = ingameState.level_name
        ingameState.level_name = level_name

    if level_name:
        ingameState.state = State()
        ingameState.state.load_from_json_file(os.path.join(os.getcwd(),'data','maps',level_name))
        ingameState.state.set_surface(screen)
        map = ingameState.state.map
    else:
        if not coords:
            coords = Map.load_coords(level_name,just_one=False) #just_one=True
        map = Map(coordinates=coords['tiles'],debug_info=ingameState.debug_info,surface=screen)#IGNORE:W0622
        snakes = Snake.make_snakes(map,coords['snakes'],surface=screen)
        ingameState.state = State(map,snakes)


    if "debug_info" in dir(ingameState):
        ingameState.debug_info.x_offset = ingameState.app.screen_h

    # set the map centered
    map.y_offset = (ingameState.app.screen_h - map.size_px) / 2
    map.x_offset = (ingameState.app.screen_h - map.size_px) / 2

    # game-related stuff
    ingameState.n_moves = 0
    ingameState.time_began = time.time()
    #ingameState.state_complete = False

    ingameState._reset_background()
