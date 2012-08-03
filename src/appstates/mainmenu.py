from appstate import AppState
#from pygame import Rect
#from pygame.image import load
import pygame

B_GLYPH = 'data/sprites/button.png'
B_HOVER_GLYPH = 'data/sprites/button_hover.png'

class MenuButton:
    shadow = None
    button = None
    hover = None
    w = 0
    h = 0
    r = None
    
    def __init__(self,x,y,title):
        self.r = pygame.Rect(x, y, MenuButton.w, MenuButton.h)
        self.title = title
        self.text_color = (255,255,50)
        self.shadow_color = (135,135,0,50)

    def draw(self, surface, font, hover=False):
        surface.blit(self.shadow, self.r.move(5,5))

        if not hover:
            surface.blit(self.button, self.r)
        else:
            surface.blit(self.hover, self.r)

        s_font = font.render(self.title,False,self.text_color)
        s_sh_font = font.render(self.title,False,self.shadow_color)
        o_x = -s_font.get_width()/2
        o_y = -s_font.get_height()/2
        o = 2
        surface.blit(s_sh_font, self._get_center(o_x+o,o_y+o))
        surface.blit(s_font, self._get_center(o_x,o_y))


    def _get_center(self,ox=0,oy=0):
        x = self.r.left + self.r.width / 2
        y = self.r.top + self.r.height / 2
        x += ox + 2 # offsets (used to render font e.g.)
        y += oy + 2
        return (x,y)

    @staticmethod
    def init():
        MenuButton.button = pygame.image.load(B_GLYPH)
        MenuButton.hover = pygame.image.load(B_HOVER_GLYPH)

        MenuButton.w = MenuButton.button.get_width()
        MenuButton.h = MenuButton.button.get_height()

        # create shadow surface
        MenuButton.shadow = pygame.Surface((MenuButton.w, MenuButton.h), pygame.SRCALPHA)
        # for each pixel in button glyph
        for a in xrange(MenuButton.w):
            for b in xrange(MenuButton.h):
                # set corresponding value in shadow surface to be semi-transparent
                c = MenuButton.button.get_at((a,b))
                s = c if all(c) == 0 else (0,0,0,150)
                MenuButton.shadow.set_at((a,b),s)


class MainMenu(AppState):
    _buttons = []
    hover_button = None
    y_offset = 0

    def __init__(self, app):
        # app
        self.app = app

        MenuButton.init() # make shadow, set w/h, etc.

        # add button in the center
        self._add_button("PLAY",0)
        self._add_button("OPTIONS",1)
        self._add_button("CREDITS",2)
        self._add_button("EXIT",3)
        

    def _add_button(self, title, position=None):
        n = position if position>=0 else len(self._buttons)

        # center coords
        x = (self.app.screen_w / 2) - MenuButton.w /2
        y = (self.app.screen_h / 2) - MenuButton.h /2

        y_offset = MenuButton.h / 2 + MenuButton.h # distance between buttons
        y = y + n*y_offset 
        y = y + MainMenu.y_offset # buttons begin not at center, but somewhat higher

        mb = MenuButton(x, y, title)
        self._buttons.append(mb)

    def _get_button_at(self,(x,y)):
        for b in MainMenu._buttons:
            if b.r.contains(pygame.Rect(x,y,1,1)):
                return b
        return None

    def process(self, event):
        if event.type not in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN]:
            return None

        self.hover_button = self._get_button_at(event.pos)
        
    def draw(self):
        self._reset_background()

        # blit buttons
        for b in MainMenu._buttons:
            hover = (b == self.hover_button)
            b.draw(self.app.screen, self.app.font_px, hover)