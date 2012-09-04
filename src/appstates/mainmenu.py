from dvizshok.appstate import AppState
import pygame
from ..utils.buttons import MenuButton


class MainMenu(AppState):
    _buttons = []
    hover_button = None
    y_offset = 0
    app = None

    def __init__(self, app):
        # app
        MainMenu.app = app

        MenuButton.init(app.resman)  # make shadow, set w/h, etc.

        # add button in the center
        self._add_button("PLAY", 0, 0)
        self._add_button("OPTIONS", 0, 1, disabled=True)
        self._add_button("CREDITS", 1, 1, disabled=True)
        self._add_button("EXIT", 1, 0)

    # def resume(self):
    #     self.hover_button = None

    def _add_button(self, title, position=None, column=0, disabled=False):
        n = position if position >= 0 else len(self._buttons)

        # center coords
        x = (self.app.screen_w / 2) - MenuButton.w / 2
        y = (self.app.screen_h / 2) - MenuButton.h / 2

        y_offset = MenuButton.h / 2 + MenuButton.h  # distance between buttons
        y = y + n * y_offset
        y = y + MainMenu.y_offset  # buttons begin not at center, but somewhat higher

        x = x + column * (MenuButton.w + MenuButton.h) - ((MenuButton.w + MenuButton.h) / 2)

        mb = MenuButton(x, y, title)
        mb.enabled = not disabled
        self._buttons.append(mb)

    def _get_button_at(self, (x, y)):
        for b in MainMenu._buttons:
            if b.r.contains(pygame.Rect(x, y, 1, 1)):
                if b.enabled:
                    return b
        return None

    def resume(self, arg):
        super(MainMenu, self).resume(arg)
        for b in self._buttons:
            b.selected = False

    def process(self):
        return super(MainMenu, self).process()

    def process_input(self, event):
        if event.type not in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN]:
            return None

        hover_tmp = self.hover_button
        self.hover_button = self._get_button_at(event.pos)
        if self.hover_button and self.hover_button != hover_tmp:
            # new hover: play sound
            if self.hover_button.enabled:
                self.app.audioman.sfx("mouseover")

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hover_button:
                ## CLICK
                self.hover_button.selected = True
                self.wait(self.CLICK_DELAY)
                t = self.hover_button.title
                if t == "PLAY":
                    self.app.audioman.sfx("select")
                    self.next_state = ("LevelSelect", None)
                if t == "EXIT":
                    self.next_state = ("GoodBye", None)

    def draw(self):
        self._reset_background()

        # blit buttons
        for b in MainMenu._buttons:
            hover = (b == self.hover_button)
            b.draw(self.app.screen, self.app.font_px, hover)

        # write version
        if "font" in self.app.__dict__:
            v_surf = self.app.font.render("v%s" % self.app.version,
                False, (255, 255, 255), (0, 0, 0))
            self.app.dirty(self.app.screen.blit(v_surf, (0, self.app.screen_h - v_surf.get_height())))
