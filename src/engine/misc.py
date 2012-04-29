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
    m = hashlib.md5()
    m.update(str(state.map))
    str_md5 = m.hexdigest()[:10]
    name = "n%s-s%s-%s" % (n_n,n_s,str_md5)
    #state.save_to_image("data/maps/%s.png" % name)
    state.save_to_json("data/maps/%s.json" % name)


def edit_map(state,event,button):
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
        for j in xrange(n): #@UnusedVariable IGNORE:W0612
            v = 0
            coords['tiles'][i].append(v)
            coords['snakes'][i].append(v)
    reset_state(app,coords=coords)

def reset_state(app,level_name=None,coords=None):
    if not coords:
        if not level_name:
            level_name = app.level_name
        app.level_name = level_name

    if level_name:
        app.state = State()
        app.state.load_from_json_file(os.path.join(os.getcwd(),'data','maps',level_name))
        app.state.set_surface(app.screen)
        map = app.state.map #IGNORE:W0622
        #print app.state
    else:
        if not coords:
            coords = Map.load_coords(level_name,just_one=False) #just_one=True
        map = Map(coordinates=coords['tiles'],debug_info=app.debug_info,surface=app.screen)#IGNORE:W0622
        snakes = Snake.make_snakes(map,coords['snakes'],surface=app.screen)
        app.state = State(map,snakes)


    if "debug_info" in dir(app):
        app.debug_info.x_offset = app.screen_h

    # set the map centered
    map.y_offset = (app.screen_h - map.size_px) / 2
    map.x_offset = (app.screen_h - map.size_px) / 2

    # game-related stuff
    app.n_moves = 0
    app.time_began = time.time()
    app.state_complete = False
