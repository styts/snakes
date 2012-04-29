import pygame, sys, os #@UnresolvedImport @UnusedImport

from logic.map import Map
from input import Input
from logic.tile import Tile
from logic.snake import Snake
from debug_info import DebugInfo
from solver import Solver

class App():
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        pygame.init()
        window = pygame.display.set_mode((1024, 768)) #IGNORE:W0612 @UnusedVariable
        pygame.display.set_caption('Snakes Prototype')
        screen = pygame.display.get_surface()
        
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        self.background = background

        self.screen = screen
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.input = Input(self)
        self.map = None  # these are set with reset_map
        self.snakes = [] #
        self.level_name = "3x3.png"
        self.debug_info = DebugInfo(self)
        self.reset_map()
        self.solver = Solver()
        
    def reset_map(self):
        coords = Map.load_coords(self.level_name)
        self.map = Map(coords['tiles'],debug_info=self.debug_info,surface=self.screen)
        self.snakes = Snake.make_snakes(self.map,self.screen,coords['snakes'])
        if "debug_info" in dir(self):
            self.debug_info.x_offset = self.map.n*Tile.BLOCK_SIZE

    def exit(self):
        pygame.quit()
        sys.exit(0)
    
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.map.draw()
        for s in self.snakes:
            s.draw()
        self.debug_info.draw()
        self.input.draw()
        pygame.display.flip()
        pygame.event.pump()
    
    def proc_input(self,events):
        for event in events:
            if not self.is_running:
                self.exit()
            else:
                self.input.process(event)

    def process(self):
        self.clock.tick(60)
        self.proc_input(pygame.event.get())
        self.draw()
