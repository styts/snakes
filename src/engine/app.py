import pygame
import os
from pygame.font import SysFont
from src.logic.utils import patternize_tile

from src.engine.audio import AudioManager
from src.engine.resman import ResourceManager, resource_path

from src.appstates.ingame import InGame
from src.appstates.mainmenu import MainMenu
from src.appstates.levelselect import LevelSelect
from src.appstates.levelcomplete import LevelComplete


class App():
    screen_w = 1024
    screen_h = 768

    appstate = None  # holds an AppState subclass instance (Menu, InGame, etc.)

    _dirty_rects = []
    #screen_w = 800
    #screen_h = 600
    #screen_w = 640
    #screen_h = 480

    def __init__(self, arguments):
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        pygame.init()
        pygame.display.set_mode((App.screen_w, App.screen_h))  # , FULLSCREEN)
        pygame.display.set_caption('Snakes Prototype')
        self.screen = pygame.display.get_surface()
        self.is_running = True  # used to trigger exit by ESC

        self.clock = pygame.time.Clock()
        #self.input = Input(self)

        self.resman = ResourceManager(self)
        self.audioman = AudioManager(self)

        background = pygame.Surface(self.screen.get_size())
        patternize_tile(background, self.resman.get_surface("tile"))
        self.background = background

        #TODO: allow setting resolution form command line

        self.font = pygame.font.Font(resource_path(os.path.join('data', 'fonts', 'WOBBLES_.ttf')), 32)
        self.font_px = pygame.font.Font(resource_path(os.path.join('data', 'fonts', 'visitor1.ttf')), 40)
        self.font_px_s = pygame.font.Font(resource_path(os.path.join('data', 'fonts', 'visitor2.ttf')), 25)
        self.sysfont = self.font_px_s  # SysFont("Courier", 12)

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
        pygame.quit()  # cleanup finally

    def _get_appstate(self, s):
        for astate in self._appstates:
            if astate.__class__.__name__ == s:
                return astate

    def dirty(self, r):
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
            if event.type == pygame.QUIT:  # or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                self.is_running = False

        ## DRAW
        self.appstate.draw()

        # write fps
        fps_surf = self.sysfont.render("FPS: %2.2f" % self.clock.get_fps(), False, (255, 255, 255), (0, 0, 0))
        self.dirty(self.screen.blit(fps_surf, (0, 0)))

        pygame.display.update(self._dirty_rects)
        pygame.event.pump()
