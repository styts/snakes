#!/usr/bin/env python
"""
Usage: Snakes [options]

<level> is path to .json file

Options:
    -v, --version              show version
    -h, --help                 show this
    -t, --test-solvability     test level solvability
    -i, --ignore-pickle        work anyway
    -l, --level <level>        level to solve
    -p <arg>                   get rid of -psn argument on Mac.apps
"""
from docopt import docopt


def solve(fn, ig, ts):
    from src.solve.utils import process_json
    j = "".join(open(fn, 'r').readlines())
    process_json(j, False, quit_on_first=ts, ignore_pickle=ig, debug_info=None)


def main():
    from src.engine.app import App

    arguments = docopt(__doc__, version='Snakes 0.2.0')

    # if a level is supplied, solve it in windowless mode
    fn = arguments["--level"]
    ig = arguments["--ignore-pickle"]
    ts = arguments["--test-solvability"]

    if "--level" in arguments and fn:
        solve(fn, ig, ts)

   # Run the pygame window
    else:
        App(arguments)

if __name__ == '__main__':
    main()
