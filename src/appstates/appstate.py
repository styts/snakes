
class AppState:
    """The App class takes care of the state transitions between the finite state automaton which consists of AppStates
    Those could be: Menu, InGame, LevelComplete, GameOver, HighScores, etc.
    They should all implement the following methods.
    """
    def process_input():
        """Handles the mouse and keyboard"""
        raise NotImplementedError("Should be implemented in AppState subclass")

    def draw():
        """Draws stuff on app.screen ( don't forget to call app.dirty(rect) )"""
        raise NotImplementedError("Should be implemented in AppState subclass")
        