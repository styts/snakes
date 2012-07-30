from engine.debug_info import DebugInfo
from engine.toolbar import Toolbar
from engine.misc import reset_state
from time import time
import pygame

from logic.snake import Move
from engine.utils import solve
from engine.misc import edit_map, reset_state
from engine.misc import save_state
from appstates.appstate import AppState
#import pygame

class InGame(AppState):
    def __init__(self,app):
        self.app = app
        self.state = None # current level
        self.debug_info = DebugInfo(self) # debug display
        self.toolbar = Toolbar(self, app.screen, app.screen_w-300, 200) # 300 px off the right edge
        
        self.n_moves = 0 
        self.time_began = time()
        self.level_name = ""
        
        #reset_state(self,"tempstate.json")

        ## input variables
        self.holding = False
        self.current_block = None
        
        self.edit_mode = True # TODO: toggle edit mode from command line

        self._reset_background() # once draw the background

    def _reset_background(self):
        """ draw the background"""
        #self.app.screen.blit(self.app.background, (0, 0))
        self.app.screen.fill((0, 0, 0))
        self.app.dirty(self.app.background.get_rect())

    def process_input(self,event):
            mods = pygame.key.get_mods()

            if self.edit_mode:
                self.toolbar.process(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.current_block != None:
                    self.holding = True
                if self.edit_mode and self.toolbar.current_button:
                    if edit_map(self.state,event,self.toolbar.current_button):
                        reset_state(self,"tempstate.json")


            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.current_block != None:
                    self.holding = False


            if not self.state: # what if we have no state/map loaded?
                return

            map = self.state.map

            if event.type == pygame.MOUSEMOTION:
                # event within map
                if event.pos[0] > map.x_offset and event.pos[0] < map.x_offset+map.size_px and event.pos[1] > map.y_offset and event.pos[1] < map.size_px+map.y_offset:
                    # update block over which mouse is
                    b = map.get_tile_at(event.pos[0], event.pos[1])
                    if self.holding and b != self.current_block:
                        se = self.current_block.get_snake_el()
                        if se:
                            if se.move(Move(se.x,se.y,b.x,b.y)):
                                self.n_moves = self.n_moves + 1
                                self._reset_background()
                                
                    self.current_block = b
                else:
                    self.current_block = None
                    self.holding = False

            # process motion over toolbar
            #if event.pos[0] > self.app.toolbar.x_offset and event.pos[1] > self.app.toolbar.y_offset:
            
            ### INTERNAL (EDITOR, DEBUG)

            # ALT-clicking on a block prints debug into to stdout
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if mods & pygame.K_LCTRL and self.current_block != None:
                    print self.current_block
                    if self.current_block.se:
                        print self.current_block.se.get_moves()

            # toggle debug info
            if event.type == pygame.KEYUP and event.key == pygame.K_d:
                self.debug_info.on = not self.debug_info.on

            # reset map
            if event.type == pygame.KEYUP and event.key == pygame.K_r:
                reset_state(self)

            # solver solve
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                quit_on_first = not (mods & pygame.KMOD_LALT)
                draw_graph = (mods & pygame.KMOD_CTRL) > 0
                print "Control draw: " , draw_graph
                solve(self.state,debug_info=self.debug_info,quit_on_first=quit_on_first,draw_graph=draw_graph)
            # print map
            #if event.type == pygame.KEYUP and event.key == pygame.K_m:
            #    self.app.map.pprint()

            # toggle edit mode
            if event.type == pygame.KEYUP and event.key == pygame.K_e:
                self.edit_mode = not self.edit_mode

            # save state/map
            if event.type == pygame.KEYUP and event.key == pygame.K_n:
                save_state(self.state)
                self.toolbar.reload_buttons()

    def draw(self):
        if self.state:
            self.state.map.draw()
            for s in self.state.snakes:
                s.draw()
        self.debug_info.draw()
                
        # number of moves
        moves_str = "Moves: %s" % self.n_moves
        ren_n_moves = self.app.font.render(moves_str,1,(255,255,0))
        ren_n_moves_shadow = self.app.font.render(moves_str,1,(155,155,0))
        self.app.screen.blit(ren_n_moves_shadow, (12,12))
        self.app.screen.blit(ren_n_moves, (10,10))
        
        #time
        delta = time()-self.time_began
        min = int(delta / 60)#IGNORE:W0622
        sec = int(delta % 60)
        str_time = "%02d:%02d" % (min,sec)
        ren_time = self.app.font.render(str_time,1,(255,255,0))
        ren_time_shadow = self.app.font.render(str_time,1,(155,155,0))
        # don't show time
        ###self.screen.blit(ren_time_shadow, (482,12))
        ###self.screen.blit(ren_time, (480,10))
        
        #completion
        if self.state and self.state.is_complete():
            ren_complete = self.app.font.render("COMPLETE",1,(155,255,0))
            self.app.screen.blit(ren_complete, (250,10))
        
        if self.edit_mode:
            self.toolbar.draw()