from time import time
from toolbar import Toolbar
import pygame, sys, os

#from input import Input
from debug_info import DebugInfo
from engine.misc import reset_state
import logic.ingame
from appstates.ingame import InGame

class App():
    screen_w = 1024
    screen_h = 768

    appstate = None
    #screen_w = 800
    #screen_h = 600
    #screen_w = 640
    #screen_h = 480

    def __init__(self, arguments):
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        pygame.init()
        window = pygame.display.set_mode((App.screen_w, App.screen_h))
        pygame.display.set_caption('Snakes Prototype')
        self.screen = pygame.display.get_surface()
        self.is_running = True # used to trigger exit by ESC

        self.clock = pygame.time.Clock()
        #self.input = Input(self)

        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        self.background = background

        #TODO: allow setting resolution form command line

        self.font = pygame.font.Font(os.path.join('data','fonts','WOBBLES_.ttf'),32)

        # start with ingame state
        self.appstate = InGame(self)

    def process(self):
        self.clock.tick(60)
        
        ## PRO
        events = pygame.event.get()
        for event in events:
            self.appstate.process_input_event(event)

            # ESC quits app
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame. K_ESCAPE):
                pygame.quit()
                sys.exit(0)

        ## DRAW
        self.appstate.draw()

        pygame.display.flip()
        pygame.event.pump()
