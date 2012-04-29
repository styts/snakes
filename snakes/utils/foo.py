from logic.map import Map
from logic.snake import Snake
from logic.state import State
import pickle
import pprint
        

level_name = '3-2.png'
coords = Map.load_coords(level_name)
map = Map(coordinates=coords['tiles'])
snakes = Snake.make_snakes(map,coords['snakes'])
state = State(map,snakes)

with open('state.json', mode='w') as f:
    f.write(state.to_json())
    
s2 = State()
s2.load_from_json_file("state.json")

print s2 == state