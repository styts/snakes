import pprint
import pygame
import random
from utils import letter_to_color
#class Generator:
#    def __init__(self):
#        self._random_map()
#    
#    def _random_map(self):
#        pass

def make_map(n):
    coords = []
    for i in xrange(n):
        coords.append([])
        for j in xrange(n):
            v = 0
            coords[i].append(v)
    return coords

def map_to_img(coords):
    n = len(coords)
    surf = pygame.Surface((2*n,n))
    surf.lock()
    for i in xrange(n):
        for j in xrange(n):
            v = coords[i][j]
            color = letter_to_color(v)
            surf.set_at((i,j),color)
            surf.set_at((i+n,j),color)
    surf.unlock()
    pygame.image.save(surf,'temp_map.png')
    
    
def random_pos(coords):
    n = len(coords)
    a = random.randrange(0,n)
    b = random.randrange(0,n)
    return (a,b)
    
def populte_map(coords,times=1):
    tiles = ['g']
    snakes = ['G','B','R']
    for i in xrange(times):
        for t in tiles:
            a,b = random_pos(coords)
            coords[a][b] = t
        for s in snakes:
            a,b = random_pos(coords)
            coords[a][b] = s
    return coords
            

def main():
    coords = make_map(3)
    coords = populte_map(coords)
    map_to_img(coords)
    #g = Generator()

main()