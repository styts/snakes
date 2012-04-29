from logic.snake import Move
from logic.state import State
import pygame #@UnresolvedImport

class Input():
    def __init__(self,app):
        self.app = app
        self.holding = False
        self.current_block = None
        
    def draw(self):
        pass
        #if self.current_block:
        #    self.app.debug_info.attach_var(str(self.current_block))
        
    def process(self,event):
        mods = pygame.key.get_mods()
        map = self.app.map #IGNORE:W0622
        
        if event.type == pygame.MOUSEMOTION:
            # event within map
            if event.pos[0] > 0 and event.pos[0] < map.size_px and event.pos[1] > 0 and event.pos[1] < map.size_px:
                # update block over which mouse is
                b = map.get_tile_at(event.pos[0], event.pos[1])
                if self.holding and b != self.current_block:
                    
                    se = self.current_block.get_snake_el()
                    if se:
                        se.move(Move(se.x,se.y,b.x,b.y))
                    # can we walk the snake?
                    #if se and b.is_walkable() and se.is_neighbour_tile(b):
                    #    se.walk_to(b)
                self.current_block = b
            else:
                self.current_block = None
                self.holding = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.current_block != None:
                self.holding = True
            # ALT-clicking on a block prints debug into to stdout 
            if mods & pygame.K_LCTRL and self.current_block != None:
                print self.current_block
                if self.current_block.se:
                    print self.current_block.se.get_moves()
                
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.current_block != None:
                self.holding = False
                
        # toggle debug info
        if event.type == pygame.KEYUP and event.key == pygame.K_d:
            self.app.debug_info.on = not self.app.debug_info.on
        # reset map
        if event.type == pygame.KEYUP and event.key == pygame.K_r:
            self.app.reset_map()
        # solver solve
        if event.type == pygame.KEYUP and event.key == pygame.K_s:
            self.app.solver.set_state(State(self.app.map,self.app.snakes))
        # print map
        if event.type == pygame.KEYUP and event.key == pygame.K_m:
            self.app.map.pprint()
            
            
        # load map
        if event.type == pygame.KEYUP and pygame.key.name(event.key) in map.mapdict:
            self.app.level_name = map.mapdict[pygame.key.name(event.key)]
            self.app.reset_map()
            
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame. K_ESCAPE):
            self.app.is_running = False