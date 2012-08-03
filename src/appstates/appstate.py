
class AppState:
    """The App class takes care of the state transitions between the finite state automaton which consists of AppStates
    Those could be: Menu, InGame, LevelComplete, GameOver, HighScores, etc.
    They should all implement the following methods.
    """
    def process():
        """Handles the mouse and keyboard"""
        raise NotImplementedError("Should be implemented in AppState subclass")

    def draw():
        """Draws stuff on app.screen ( don't forget to call app.dirty(rect) )"""
        raise NotImplementedError("Should be implemented in AppState subclass")
        
    def _reset_background(self):
        """ draw the background"""
        self.app.screen.blit(self.app.background, (0, 0))
        #self.app.screen.fill((0, 0, 0))
        self.app.dirty(self.app.background.get_rect())


class GoodBye(AppState):
    """A "welcome" screen that blits out saying GoodBye or waits for keypress"""
    pass
#     i = 1000 # frames
#     def process():
#         GoodBye.i = GoodBye.i - 1

#     def draw():


