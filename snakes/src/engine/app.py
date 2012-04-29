from time import time
from toolbar import Toolbar
import pygame, sys, os #@UnresolvedImport @UnusedImport

from input import Input
from debug_info import DebugInfo
from engine.misc import reset_state

class App():
    screen_w = 800
    screen_h = 600
    #screen_w = 640
    #screen_h = 480
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        pygame.init()
        window = pygame.display.set_mode((App.screen_w, App.screen_h)) #IGNORE:W0612 @UnusedVariable
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
        self.state = None
        self.debug_info = DebugInfo(self)
        self.toolbar = Toolbar(self, self.screen, self.screen_h, 200)
        
        self.n_moves = 0 
        self.time_began = time()
        self.level_name = ""
        
        reset_state(self,"tempstate.json")
        
        self.font = pygame.font.Font(os.path.join('data','fonts','WOBBLES_.ttf'),32)
        
        self.edit_mode = True
        #self.toolbar.current_button = self.toolbar.buttons[0][0]
        self.state_complete = False

    def exit(self):
        pygame.quit()
        sys.exit(0)
    
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.state.map.draw()
        for s in self.state.snakes:
            s.draw()
        self.debug_info.draw()
                
        # number of moves
        moves_str = "Moves: %s" % self.n_moves
        ren_n_moves = self.font.render(moves_str,1,(255,255,0))
        ren_n_moves_shadow = self.font.render(moves_str,1,(155,155,0))
        self.screen.blit(ren_n_moves_shadow, (12,12))
        self.screen.blit(ren_n_moves, (10,10))
        
        #time
        delta = time()-self.time_began
        min = int(delta / 60)#IGNORE:W0622
        sec = int(delta % 60)
        str_time = "%02d:%02d" % (min,sec)
        ren_time = self.font.render(str_time,1,(255,255,0))
        ren_time_shadow = self.font.render(str_time,1,(155,155,0))
        self.screen.blit(ren_time_shadow, (482,12))
        self.screen.blit(ren_time, (480,10))
        
        #completion
        if self.state_complete:
            ren_complete = self.font.render("COMPLETE",1,(155,255,0))
            self.screen.blit(ren_complete, (250,10))
        
        if self.edit_mode:
            self.toolbar.draw()
        
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
