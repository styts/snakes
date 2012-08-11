from src.logic.map import Map
from src.logic.snake import Snake
from src.logic.state import State
from src.engine.utils import SNAKE_VALUES

def save_state(state):
    n_s = len(state.snakes)
    n_n = state.map.n
    str_md5 = state.__hash__()
    name = "n%s-s%s-%s" % (n_n,n_s,str_md5)
    #state.save_to_image("data/maps/%s.png" % name)
    state.save_to_json("data/maps/%s.json" % name)

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