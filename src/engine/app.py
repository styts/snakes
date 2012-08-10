from time import time
from toolbar import Toolbar
import pygame, sys, os
from pygame.locals import FULLSCREEN
from pygame.font import SysFont
from debug_info import DebugInfo
import src.logic.ingame
from src.appstates.ingame import InGame
from src.appstates.mainmenu import MainMenu
from src.appstates.levelselect import LevelSelect
from src.appstates.levelcomplete import LevelComplete
#from appstates.appstate import GoodBye
from src.engine.utils import patternize_tile
import glob

class ResourceManager():
    LOCATION = os.path.join("data", "sprites")

    def __init__(self, app):
        self.app = app
        self._surfaces = {}
        self._load_all()

    def _load_all(self):
        ext = ".png"
        for fn in glob.glob(ResourceManager.LOCATION+"/*%s" % ext):
            bn = os.path.basename(fn).replace(ext, "")
            surf = pygame.image.load(fn)
            surf = surf.convert_alpha()
            self._surfaces[bn] = {}
            self._surfaces[bn]["default"] = surf

    def fill_me(self, surf, color, alpha):
        s = surf.copy()
        col = color + (alpha,)
        s.fill(col, None, pygame.BLEND_RGBA_MULT)
        return s

    def get_surface(self, name, color=None, alpha=255):
        color_str = str(color)
        if name not in self._surfaces.keys():
            return None

        if color:
            if color_str not in self._surfaces[name].keys():
                self._surfaces[name][color_str] = self.fill_me(self._surfaces[name]['default'], color, alpha)
            return self._surfaces[name][color_str]
        else:
            return self._surfaces[name]["default"]


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

        self.resman = ResourceManager(self)

        background = pygame.Surface(self.screen.get_size())
        patternize_tile(background, self.resman.get_surface("tile"))
        #patternize_tile(background, "data/assets/128-64.png")
        #background.fill((0, 0, 0))
        #background.convert()
        self.background = background

        #TODO: allow setting resolution form command line

        self.font = pygame.font.Font(os.path.join('data','fonts','WOBBLES_.ttf'),32)
        self.font_px = pygame.font.Font(os.path.join('data','fonts','visitor1.ttf'),40)
        self.font_px_s = pygame.font.Font(os.path.join('data','fonts','visitor2.ttf'),25)
        self.sysfont = SysFont("Courier",12)

        self._appstates = []
        self._appstates.append(MainMenu(self))
        self._appstates.append(InGame(self))
        self._appstates.append(LevelSelect(self))
        self._appstates.append(LevelComplete(self))

        self.appstate = self._get_appstate("MainMenu")
        # start with ingame state
        #self.appstate = InGame(self)

        ## Main Loop
        while self.is_running:
            self.process()
        pygame.quit() # cleanup finally

    def _get_appstate(self, s):
        for astate in self._appstates:
            if astate.__class__.__name__ == s:
                return astate

    def dirty(self,r):
        """AppStates call this when having drawed on app.screen somewhere"""
        if r not in self._dirty_rects:
            self._dirty_rects.append(r)

    def process(self):
        self.clock.tick(30)

        self._dirty_rects = []
        
        p = self.appstate.process()
        if p:
            next_state, state_arg = p
            if next_state:
                if next_state == "GoodBye":
                    self.is_running = False
                else:
                    # appstate wants to change!
                    self.appstate = self._get_appstate(next_state)
                    self.appstate.resume(state_arg)

        events = pygame.event.get()
        for event in events:
            p = self.appstate.process_input(event)
            
            # ESC quits app
            if event.type == pygame.QUIT: #or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                self.is_running = False

        ## DRAW
        self.appstate.draw()

        # write fps
        fps_surf = self.sysfont.render("FPS: %2.2f" % self.clock.get_fps(), False, (255,255,255), (0, 0, 0))
        self.dirty(self.screen.blit(fps_surf, (0, 0)))


        #print self._dirty_rects
        pygame.display.update(self._dirty_rects)
        #pygame.display.flip()
        pygame.event.pump()
