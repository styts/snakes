#!/usr/bin/env python
"""
Usage: main [options]

<level> is path to .json file

Options:
    -v, --version              show version
    -h, --help                 show this
    -t, --test-solvability     test level solvability
    -i, --ignore-pickle        work anyway
    -l, --level <level>        level to solve
    -p <arg>                   get rid of -psn argument on Mac.apps
"""
try:
    from docopt import docopt
except:
    pass


def solve(fn, ig, ts):
    from src.solve.utils import process_json
    j = "".join(open(fn, 'r').readlines())
    process_json(j, False, quit_on_first=ts, ignore_pickle=ig, debug_info=None)


from dvizshok.app import App
import pygame
from src.logic.utils import patternize_tile


class MyApp(App):
    def _load_levels(self):
        ## load levels/maps
        from src.utils.sort import sort_nicely
        from dvizshok.resman import resource_path
        from glob import glob
        maps = glob(resource_path("data/maps") + "/*.json")
        sort_nicely(maps)
        self.levels = maps

    def init(self):
        background = pygame.Surface(self.screen.get_size())
        patternize_tile(background, self.resman.get_surface("tile"))
        self.background = background

        self.resman.load_font("default", 20)
        self.resman.load_font("visitor1", 40)
        self.resman.load_font("visitor2", 25)

        self.font = self.resman.get_font("default_20")
        self.font_px = self.resman.get_font("visitor1_40")  # 40
        self.font_px_s = self.resman.get_font("visitor2_25")  # 25

        self._load_levels()


def main():
    from src.appstates.ingame import InGame
    from src.appstates.levelcomplete import LevelComplete
    from src.appstates.levelselect import LevelSelect
    from src.appstates.mainmenu import MainMenu

    title = 'Snakes 0.2.0'

    arguments = None
    try:
        arguments = docopt(__doc__, version=title)

        # if a level is supplied, solve it in windowless mode
        fn = arguments["--level"]
        ig = arguments["--ignore-pickle"]
        ts = arguments["--test-solvability"]

    except:
        pass

    if arguments and "--level" in arguments and fn:
        solve(fn, ig, ts)

   # Run the pygame window
    else:
        #res = (1024, 768)
        #res = (800, 480)
        app = MyApp(title, appstates=[MainMenu, InGame, LevelSelect, LevelComplete])
        app.run()


if __name__ == '__main__':
    main()
