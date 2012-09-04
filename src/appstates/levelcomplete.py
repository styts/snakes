from dvizshok.appstate import AppState

import pygame
from src.utils.buttons import MenuButton


class LevelComplete(AppState):
    def __init__(self, app):
        self.app = app
        self.surface = pygame.Surface(self.app.screen.get_size(), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 150))

        panel = self.app.resman.get_surface("level_complete")
        x = self.app.screen_w / 2 - MenuButton.w / 2
        y = self.app.screen_h / 2 - panel.get_height() / 2 + panel.get_height() - 20 - MenuButton.h
        self.but_exit = MenuButton(x, y, "EXIT")
        self._buttons = []
        self._buttons.append(self.but_exit)
        self.hover_button = None

    def process(self):
        return super(LevelComplete, self).process()

    def process_input(self, event):
        # quit to menu - ESC
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            self.next_state = ("LevelSelect", None)

        ### BUTTONS
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
                if t == "EXIT":
                    self.app.audioman.sfx("select")
                    self.next_state = ("LevelSelect", None)

    def _get_button_at(self, (x, y)):
        for b in self._buttons:
            if b.r.contains(pygame.Rect(x, y, 1, 1)):
                if b.enabled:
                    return b
        return None

    def resume(self, args):
        super(LevelComplete, self).resume(args)

        self.level_name = args[0]
        self.bg = args[1]
        for b in self._buttons:
            b.selected = False
        self.hover_button = None

    def draw(self):
        r = self.app.screen.blit(self.bg, (0, 0))
        self.app.dirty(r)
        self.app.screen.blit(self.surface, (0, 0))
        panel = self.app.resman.get_surface("level_complete")
        x = self.app.screen_w / 2 - panel.get_width() / 2
        y = self.app.screen_h / 2 - panel.get_height() / 2
        self.app.screen.blit(panel, (x, y))

        # blit buttons
        for b in self._buttons:
            hover = (b == self.hover_button)
            b.draw(self.app.screen, self.app.font_px, hover)
