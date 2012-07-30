from time import time
from toolbar import Toolbar
import pygame, sys, os
from pygame.locals import FULLSCREEN
from pygame.font import SysFont
from debug_info import DebugInfo
from engine.misc import reset_state
import logic.ingame
from appstates.ingame import InGame
from engine.utils import patternize_tile

class App():
    screen_w = 1024
    screen_h = 768

    appstate = None # holds an AppState subclass instance (Menu, InGame, etc.)

    _dirty_rects = []
    #screen_w = 800
    #screen_h = 600
    #screen_w = 640
    #screen_h = 480

    def __init__(self, arguments):
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        pygame.init()
        window = pygame.display.set_mode((App.screen_w, App.screen_h))#, FULLSCREEN)
        pygame.display.set_caption('Snakes Prototype')
        self.screen = pygame.display.get_surface()
        self.is_running = True # used to trigger exit by ESC

        self.clock = pygame.time.Clock()
        #self.input = Input(self)

        background = pygame.Surface(self.screen.get_size())
        patternize_tile(background, "data/assets/tile.png")
        #patternize_tile(background, "data/assets/128-64.png")
        #background.fill((0, 0, 0))
        #background.convert()
        self.background = background

        #TODO: allow setting resolution form command line

        self.font = pygame.font.Font(os.path.join('data','fonts','WOBBLES_.ttf'),32)
        self.sysfont = SysFont("Courier",12)

        # start with ingame state
        self.appstate = InGame(self)

        ## Main Loop
        while self.is_running:
            self.process()
        pygame.quit() # cleanup finally

    def dirty(self,r):
        """AppStates call this when having drawed on app.screen somewhere"""
        if r not in self._dirty_rects:
            self._dirty_rects.append(r)

    def process(self):
        self.clock.tick(30)

        self._dirty_rects = []
        
        events = pygame.event.get()
        for event in events:
            self.appstate.process_input(event)

            # ESC quits app
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame. K_ESCAPE):
                self.is_running = False

        ## DRAW
        self.appstate.draw()

        # write fps
        fps_surf = self.sysfont.render("FPS: %s" % self.clock.get_fps(), False, (255,255,255), (0, 0, 0))
        self.dirty(self.screen.blit(fps_surf, (0, 0)))


        #print self._dirty_rects
        pygame.display.update(self._dirty_rects)
        #pygame.display.flip()
        pygame.event.pump()
