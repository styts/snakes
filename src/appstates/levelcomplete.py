from appstate import AppState
import pygame

LC_BG = 'data/sprites/level_complete_bg.png'

class LevelComplete(AppState):
    def __init__(self, app):
        self.app = app
        self.surface = pygame.Surface(self.app.screen.get_size(), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 150))
        self.panel = pygame.image.load(LC_BG)

    def process(self):
        return super(LevelComplete, self).process()

    def process_input(self, event):
        # quit to menu - ESC
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            self.next_state = ("LevelSelect", None)

        if event.type not in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN]:
            return None


    def resume(self, args):
    	super(LevelComplete, self).resume(args)

    	self.level_name = args[0]
    	self.bg = args[1]

    def draw(self):
        self.app.screen.blit(self.bg, (0, 0))
        self.app.screen.blit(self.surface, (0, 0))
        x = self.app.screen_w / 2 - self.panel.get_width()/2
        y = self.app.screen_h / 2 - self.panel.get_height()/2
        self.app.screen.blit(self.panel, (x, y))