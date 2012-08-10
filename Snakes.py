#!/usr/bin/env python
"""
Usage: ./Snakes.py [<level>] [-t] [-i]

<level> is path to .json file

Options:
    -v, --version              show version
    -h, --help                 show this
    -t, --test-solvability     test level solvability
    -i, --ignore-pickle        work anyway
"""

#import sys
#sys.path.append("src")

from docopt import docopt

def solve(fn,ig):
    from src.solve.utils import process_json
    j = "".join(open(fn,'r').readlines())
    process_json(j, False, quit_on_first=True, ignore_pickle=ig, debug_info=None)

def main():
    arguments = docopt(__doc__, version='Snakes 0.2.0')

    # if a level is supplied, solve it in windowless mode
    fn = arguments["<level>"]
    t = arguments["--test-solvability"]
    ig = arguments["--ignore-pickle"]
    #print t

    # print arguments
    # sys.exit(0)
    if "<level>" in arguments and fn:
        solve(fn,ig)
    # Run the pygame window
    else:
        from src.engine.app import App
        app = App(arguments)

if __name__ == '__main__':
    main()
    #solve('data/maps/tempstate.json',True)
