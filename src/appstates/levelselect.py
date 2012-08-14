import os
from src.logic.state import State
import pygame
from src.appstates.mainmenu import MenuButton
from math import floor
from src.engine.appstate import AppState
from src.engine.buttons import LevelButton
# B_GLYPH = 'data/sprites/b_sq.png'
# B_HOVER_GLYPH = 'data/sprites/b_sq_hi.png'
BUTTONS_PER_ROW = 6
from src.engine.resman import resource_path


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
        self.selected_button = None

        LevelButton.init(app.resman) # make shadow, set w/h, etc.

        self.levels_width = 5*(LevelButton.w+10)
        #self.lb_surf = pygame.Surface((self.levels_width,300))

        self._refresh_levels()

        self.back_button = MenuButton(50,self.app.screen_h - 50 - MenuButton.h,"Back")
        self.select_button = MenuButton(self.app.screen_w - MenuButton.w - 50,self.app.screen_h - 50 - MenuButton.h,"Select")

        self.levelstats = LevelStats(self.app.font_px, x_offset=self.app.screen_w-430,width=380)
        #self.levelstats.pick(self.levelbuttons[0]) # init with 1st level
        self.resume(None)

    def _buttons(self):
        # all my buttons are belong to you
        return [self.back_button, self.select_button] + self.levelbuttons

    def resume(self, arg):
        super(LevelSelect, self).resume(arg)
        for b in self._buttons():
            b.selected = False
        #self.pick(self.levelbuttons[0]) # init with 1st level
        self.select_button.enabled = False

    def pick(self, button):
        for b in self._buttons():
            b.selected = False
        self.selected_button = button
        self.levelstats.pick(button)
        self.select_button.enabled = True

    def process(self):
        return super(LevelSelect, self).process()

    def process_input(self, event):
        # quit to menu - ESC
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            return "MainMenu"

        if event.type not in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN]:
            return None

        # is there a new hover button? yes: play sound
        tmp_hover = self.hover_button
        self.hover_button = LevelButton.get_button_at(self._buttons(), event.pos)
        if self.hover_button and self.hover_button != tmp_hover:
            # new hover, todo: play sound 
            self.app.audioman.sfx("mouseover")

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hover_button:
                ### select a level button
                if self.hover_button.__class__.__name__ == "LevelButton":
                    self.selected_button = self.hover_button
                    for b in self.levelbuttons:
                        b.selected = False
                    self.pick(self.selected_button)

                ### back to main menu
                t = self.hover_button.title
                self.hover_button.selected = True
                self.app.audioman.sfx("select")
                self.wait(self.CLICK_DELAY)

                if t == "Back":
                    self.next_state = ("MainMenu", None)
                if t == "Select":
                    #print self.selected_button, self.hover_button
                    self.next_state = ("InGame", self.selected_button.title)


    def _refresh_levels(self):
        maps = self.app.resman.get_levels()
        i = 0
        spacing = 20
        x_o = 50
        y_o = 50
        for fn in maps:
            fn = os.path.basename(fn)
            state = State()
            state.load_from_json_file(os.path.join(os.getcwd(),'data','maps',fn))
            thumb = state.get_thumbnail(resman=self.app.resman)
            #t_w, t_h = thumb.get_size()
            #thumb = pygame.transform.scale(thumb,(t_w*4,t_h*4))
            per = BUTTONS_PER_ROW
            col = i % per
            row = floor(i / per)
            x = x_o + col*(LevelButton.w + spacing)
            y = y_o + row*(LevelButton.w + spacing)
            b = LevelButton(fn, thumb, x, y, levelnr=i+1)
            self.levelbuttons.append(b)
            i = i + 1

    def draw(self):
        self._reset_background()

        for b in self._buttons():
            hover = (b == self.hover_button)
            b.draw(self.app.screen, self.app.font_px, hover)

        self.levelstats.draw(self.app.screen, self.app.font_px)