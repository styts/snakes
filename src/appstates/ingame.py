import time
import pygame
import os
import pickle

from src.logic.debug_info import DebugInfo
from src.logic.toolbar import Toolbar
from src.logic.snake import Snake, Move
from src.logic.state import State
from src.logic.map import Map
from src.logic.utils import get_life_values
from src.solve.utils import process_json
from src.logic.utils import edit_map
from src.logic.utils import save_state
from src.engine.appstate import AppState
from src.logic.lifemeter import LifeMeter

MAX_LIFE = 20


class InGame(AppState):
    def __init__(self, app):
        self.app = app
        self.state = None  # current level
        self.debug_info = DebugInfo(self)  # debug display
        self.toolbar = Toolbar(self, app.screen, app.screen_w - 250, 200)  # 250 px off the right edge, 200 from top

        self.n_moves = 0
        self.time_began = time.time()
        self.level_name = ""

        ## input variables
        self.holding = False
        self.current_block = None
        self.curr_se = None  # current snake element, for animation
        self.curr_se_flicker_alpha = 0

        self.edit_mode = False  # TODO: toggle edit mode from command line

        self._reset_background()  # once draw the background

        self.level_minmoves = -1  # TODO: read from state or whatever
        self.bonus_max = self.level_minmoves  # set it to same as minmoves for now
        self.max_life = MAX_LIFE  # used consistently in all levels!
        self.lifemeter = None

        #self.reset_state("tempstate.json")

    def resume(self, arg):
        super(InGame, self).resume(arg)
        self.reset_state(arg)

    def process(self):
        if self.current_block:
            self.curr_se = self.current_block.get_snake_el()
            # if self.curr_se and self.curr_se.is_head():
            #     self.curr_se.flicker()

        for s in self.state.snakes:
            for se in s.elements:
                se.process(animate=se == self.curr_se and self.curr_se.is_head())

        return super(InGame, self).process()

    def process_input(self, event):
            mods = pygame.key.get_mods()

            # quit to menu - ESC
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.next_state = ("MainMenu", None)
                #return "MainMenu"

            if self.edit_mode:
                self.toolbar.process(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.current_block != None:
                    self.holding = True
                if self.edit_mode and self.toolbar.current_button:
                    if edit_map(self.state, event, self.toolbar.current_button):
                        self.reset_state("tempstate.json")

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.current_block != None:
                    self.holding = False

            if not self.state:  # what if we have no state/map loaded?
                return

            map = self.state.map

            if event.type == pygame.MOUSEMOTION:
                # event within map
                if event.pos[0] > map.x_offset and event.pos[0] < map.x_offset + map.size_px and event.pos[1] > map.y_offset and event.pos[1] < map.size_px + map.y_offset:
                    # update block over which mouse is
                    b = map.get_tile_at(event.pos[0], event.pos[1])

                    if self.holding and b != self.current_block:
                        se = self.current_block.get_snake_el()
                        if se:
                            if se.move(Move(se.x, se.y, b.x, b.y)):
                                self.app.audioman.sfx("move")
                                self.n_moves = self.n_moves + 1
                                self._reset_background()
                                if self.state and self.state.is_complete():
                                    self.draw()
                                    self.next_state = ("LevelComplete", (self.level_name, self.app.screen.copy()))

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
                self.reset_state()

            # solver solve
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                quit_on_first = not (mods & pygame.KMOD_LALT)
                #draw_graph = True  # TRUE, cuz its quite fast with sdpf? program.... (mods & pygame.KMOD_CTRL) > 0
                ignore_pickle = (mods & pygame.KMOD_CTRL) > 0
                print "quit1: %s. ignore_pickle: %s" % (quit_on_first, ignore_pickle)
                process_json(self.state.to_json(), use_cloud=False, quit_on_first=quit_on_first, ignore_pickle=ignore_pickle, debug_info=self.debug_info)

                #solve(self.state,debug_info=self.debug_info,quit_on_first=quit_on_first,draw_graph=draw_graph)
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
        self._reset_background()

        if self.state:
            self.state.draw(resman=self.app.resman)

        self.debug_info.draw()

        # number of moves
        moves_str = "Moves: %s" % self.n_moves
        ren_n_moves = self.app.font.render(moves_str, 1, (255, 255, 0, 100))
        ren_n_moves_shadow = self.app.font.render(moves_str, 1, (155, 155, 0, 100))
        self.app.screen.blit(ren_n_moves_shadow, (12, 12))
        self.app.screen.blit(ren_n_moves, (10, 10))

        # Life Meter Bar
        life_values = get_life_values(self.n_moves, self.level_minmoves, self.max_life, self.bonus_max)
        if self.lifemeter:
            self.lifemeter.draw(self.app.screen, life_values)

        if self.edit_mode:
            self.toolbar.draw()

    def clean_map(self, n):
        """used by editor in the toolbar, it sets map to a clean square of size n x n"""
        coords = {"tiles": [], "snakes": []}
        for i in xrange(n):
            coords['tiles'].append([])
            coords['snakes'].append([])
            for j in xrange(n):
                v = 1
                coords['tiles'][i].append(v)
                coords['snakes'][i].append(v)
        self.reset_state(coords=coords)

    def reset_state(self, level_name=None, coords=None):
        if self.app.screen != None:
            screen = self.app.screen
        else:
            screen = None
        if not coords:
            if not level_name:
                level_name = self.level_name
            self.level_name = level_name

        if level_name:
            self.state = State()
            self.state.load_from_json_file(os.path.join(os.getcwd(), 'data', 'maps', level_name))
            self.state.set_surface(screen)
            map = self.state.map
        else:
            if not coords:
                coords = Map.load_coords(level_name, just_one=False)  # just_one=True
            #print "oof", self.debug_info
            map = Map(coordinates=coords['tiles'], debug_info=self.debug_info, surface=screen)
            snakes = Snake.make_snakes(map, coords['snakes'], surface=screen)
            self.state = State(map, snakes)

        if "debug_info" in dir(self):
            self.debug_info.x_offset = self.app.screen_h

        # set the map centered
        map.y_offset = (self.app.screen_h - map.size_px) / 2
        map.x_offset = (self.app.screen_h - map.size_px) / 2

        # game-related stuff
        self.n_moves = 0
        self.time_began = time.time()
        #self.state_complete = False

        self._reset_background()

        #### load the level data?

        fn = 'data/graphs/%s.pickle' % self.state.__hash__()
        if os.path.exists(fn):
            (tmp_gr, tmp_sols) = pickle.load(open(fn, 'rb'))
            self.level_minmoves = tmp_sols[0].__len__() - 1
        else:
            self.level_minmoves = -1  # yeah, default bitch
        self.bonus_max = self.level_minmoves  # same for now
        self.lifemeter = LifeMeter(self.level_minmoves, self.level_minmoves, self.max_life)  # the bar on the side
