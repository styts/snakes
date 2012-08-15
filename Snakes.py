#!/usr/bin/env python
"""
Usage: Snakes [options]

<level> is path to .json file

Options:
    -v, --version              show version
    -h, --help                 show this
    -t, --test-solvability     test level solvability
    -i, --ignore-pickle        work anyway
    -l, --level                level to solve
"""
from docopt import docopt

import sys


def solve(fn, ig):
    from src.solve.utils import process_json
    j = "".join(open(fn, 'r').readlines())
    process_json(j, False, quit_on_first=True, ignore_pickle=ig, debug_info=None)


def main():
    from src.engine.app import App

    for o in sys.argv:
        if o.startswith("-psn"):
            # Mac.app Hack!!! docopt will complain that a -psn_0_2740893 parameter is being passed, so avoid it
            App(None)
            sys.exit(0)

    arguments = docopt(__doc__, version='Snakes 0.2.0')

    # if a level is supplied, solve it in windowless mode
    fn = arguments["--level"]
    ig = arguments["--ignore-pickle"]

    if "--level" in arguments and fn:
        solve(fn, ig)

   # Run the pygame window
    else:
        App(arguments)

if __name__ == '__main__':
    main()
