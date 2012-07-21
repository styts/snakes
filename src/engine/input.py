from logic.snake import Move
from utils import solve
from misc import edit_map, reset_state
from misc import save_state
import pygame #@UnresolvedImport

class Input():
    def __init__(self,app):
        self.app = app
        self.holding = False
        self.current_block = None

    def process(self,event):
        mods = pygame.key.get_mods()
        map = self.app.state.map #IGNORE:W0622

        if event.type == pygame.MOUSEMOTION:
            # event within map
            if event.pos[0] > map.x_offset and event.pos[0] < map.x_offset+map.size_px and event.pos[1] > map.y_offset and event.pos[1] < map.size_px+map.y_offset:
                # update block over which mouse is
                b = map.get_tile_at(event.pos[0], event.pos[1])
                if self.holding and b != self.current_block:
                    se = self.current_block.get_snake_el()
                    if se:
                        if se.move(Move(se.x,se.y,b.x,b.y)):
                            self.app.n_moves = self.app.n_moves + 1
                            self.app.state_complete = self.app.state.is_complete()
                self.current_block = b
            else:
                self.current_block = None
                self.holding = False

        # process motion over toolbar
        #if event.pos[0] > self.app.toolbar.x_offset and event.pos[1] > self.app.toolbar.y_offset:
        if self.app.edit_mode:
            self.app.toolbar.process(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.current_block != None:
                self.holding = True
            # ALT-clicking on a block prints debug into to stdout
            if mods & pygame.K_LCTRL and self.current_block != None:
                print self.current_block
                if self.current_block.se:
                    print self.current_block.se.get_moves()
            if self.app.edit_mode and self.app.toolbar.current_button:
                if edit_map(self.app.state,event,self.app.toolbar.current_button):
                    reset_state(self.app,"tempstate.json")

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.current_block != None:
                self.holding = False

        # toggle debug info
        if event.type == pygame.KEYUP and event.key == pygame.K_d:
            self.app.debug_info.on = not self.app.debug_info.on
        # reset map
        if event.type == pygame.KEYUP and event.key == pygame.K_r:
            reset_state(self.app)
        # solver solve
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            quit_on_first = not (mods & pygame.KMOD_LALT)
            draw_graph = (mods & pygame.KMOD_CTRL) > 0
            print "Control draw: " , draw_graph
            solve(self.app.state,debug_info=self.app.debug_info,quit_on_first=quit_on_first,draw_graph=draw_graph)
        # print map
        if event.type == pygame.KEYUP and event.key == pygame.K_m:
            self.app.map.pprint()

        # toggle edit mode
        if event.type == pygame.KEYUP and event.key == pygame.K_e:
            self.app.edit_mode = not self.app.edit_mode

        # save state/map
        if event.type == pygame.KEYUP and event.key == pygame.K_n:
            save_state(self.app.state)
            self.app.toolbar.reload_buttons()


#        # load map
#        if event.type == pygame.KEYUP and pygame.key.name(event.key) in map.mapdict:
#            level_name = map.mapdict[pygame.key.name(event.key)]
#            self.app.level_name = level_name
#            reset_state(self.app,level_name)

        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame. K_ESCAPE):
            self.app.is_running = False
