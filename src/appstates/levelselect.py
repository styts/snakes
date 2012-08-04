import glob, os
from src.utils.sort import sort_nicely
from logic.state import State
import pygame
from appstates.mainmenu import MenuButton
from math import floor
from appstate import AppState

B_GLYPH = 'data/sprites/b_sq.png'
B_HOVER_GLYPH = 'data/sprites/b_sq_hi.png'
BUTTONS_PER_ROW = 6

class LevelButton():
    """A Selectable Level Button (20+ of these on the left)"""
    button = None
    shadow = None
    hover = None
    a = None # will be set to width of square button
    def __init__(self, name, thumb, x, y, levelnr=0):
        self.r = pygame.Rect(x, y, LevelButton.a, LevelButton.a)
        self.title = name
        self.thumb = thumb
        self.selected = False
        self.levelnr = levelnr
    
    def draw(self, surface, font=None, hover=False):
        if not self.selected:
            surface.blit(self.shadow, self.r.move(5,5))

        if not hover and not self.selected:
            surface.blit(self.button, self.r)
        else:
            surface.blit(self.hover, self.r)

        surface.blit(self.thumb, self.r.move(5,5))

    @staticmethod
    # todo: put me in Button class
    def get_button_at(buttons,(x,y)):
        for b in buttons:
            if b.r.contains(pygame.Rect(x,y,1,1)):
                return b
        return None

    @staticmethod
    def init():
        LevelButton.button = pygame.image.load(B_GLYPH)
        LevelButton.hover = pygame.image.load(B_HOVER_GLYPH)

        LevelButton.a = LevelButton.button.get_width()

        #LevelButton.w = LevelButton.button.get_width()
        #LevelButton.h = LevelButton.button.get_height()

        # create shadow surface
        LevelButton.shadow = pygame.Surface((LevelButton.a, LevelButton.a), pygame.SRCALPHA)
        # for each pixel in button glyph
        for a in xrange(LevelButton.a):
            for b in xrange(LevelButton.a):
                # set corresponding value in shadow surface to be semi-transparent
                c = LevelButton.button.get_at((a,b))
                s = c if all(c) == 0 else (0,0,0,150)
                LevelButton.shadow.set_at((a,b),s)
    


class LevelStats():
    """The Surface on the right"""
    surface = None
    def __init__(self, font, x_offset=0, width=200, height=500):
        self.surface = pygame.Surface((width,height))
        self.shadow = pygame.Surface((width,height), pygame.SRCALPHA)
        self.shadow.fill((0,0,0,150))
        #self.shadow.set_alpha(100)
        self.selected_button = None
        self.surface.fill((111,93,111))
        self.x_offset = x_offset
        self.font = font

    def _redraw(self):
        self.surface.fill((111,93,111))

        c = (255,255,255)
        s_f = self.font.render("LEVEL %s" % self.selected_button.levelnr, 0, c)
        x = self.surface.get_width() / 2 - s_f.get_width()/2
        self.surface.blit(s_f, (x,10))
        # todo: say sheet about level

    def pick(self, button):
        self.selected_button = button
        self.selected_button.selected = True
        ## todo: load level and sheeeat
        self._redraw()

    def draw(self, surface, font):
        x = self.x_offset
        y = 50
        surface.blit(self.shadow, (x+4, y+4))
        surface.blit(self.surface, (x, y))


class LevelSelect(AppState):
    """The AppState"""
    def __init__(self, app):
        self.app = app
        self.levelbuttons = []
        self.hover_button = None
        self.selected_button = None

        LevelButton.init() # make shadow, set w/h, etc.

        self.levels_width = 5*(LevelButton.a+10)
        #self.lb_surf = pygame.Surface((self.levels_width,300))

        self._refresh_levels()

        self.back_button = MenuButton(50,self.app.screen_h - 50 - MenuButton.h,"Back")
        self.select_button = MenuButton(self.app.screen_w - MenuButton.w - 50,self.app.screen_h - 50 - MenuButton.h,"Select")

        self.levelstats = LevelStats(self.app.font_px, x_offset=self.app.screen_w-430,width=380)
        self.levelstats.pick(self.levelbuttons[0]) # init with 1st level

    def _buttons(self):
        # all my buttons are belong to you
        return [self.back_button, self.select_button] + self.levelbuttons

    def resume(self):
        self.hover_button = None

    def process(self, event):
        # quit to menu - ESC
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            return "MainMenu"

        if event.type not in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN]:
            return None

        self.hover_button = LevelButton.get_button_at(self._buttons(), event.pos)

        # if self.selected_button:
        #     print self.selected_button.selected

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hover_button:
                ### back to main menu
                t = self.hover_button.title
                if t == "Back":
                    return "MainMenu"

                ### select a level button
                if self.hover_button.__class__.__name__ == "LevelButton":
                    self.selected_button = self.hover_button
                    for b in self.levelbuttons:
                        b.selected = False
                    self.selected_button.selected = True # this happens extra in pick()
                    self.levelstats.pick(self.selected_button)

    def _refresh_levels(self):
        maps = glob.glob(os.path.join(os.getcwd(),'data','maps')+"/*.json")
        sort_nicely(maps)
        i = 0
        spacing = 20
        x_o = 50
        y_o = 50
        for fn in maps:
            fn = os.path.basename(fn)
            state = State()
            state.load_from_json_file(os.path.join(os.getcwd(),'data','maps',fn))
            thumb = state.get_thumbnail()
            t_w, t_h = thumb.get_size()
            thumb = pygame.transform.scale(thumb,(t_w*4,t_h*4))
            per = BUTTONS_PER_ROW
            col = i % per
            row = floor(i / per)
            x = x_o + col*(LevelButton.a + spacing)
            y = y_o + row*(LevelButton.a + spacing)
            b = LevelButton(fn, thumb, x, y, levelnr=i+1)
            self.levelbuttons.append(b)
            i = i + 1

    def draw(self):
        self._reset_background()

        for b in self._buttons():
            hover = (b == self.hover_button)
            b.draw(self.app.screen, self.app.font_px, hover)

        self.levelstats.draw(self.app.screen, self.app.font_px)