#!/usr/bin/env python
"""
Usage: ./Snakes.py [ --menu | --level <level_name> ]

Options:
    -v --version        show version
    -h --help           show this
"""

import sys
sys.path.append("src")

from engine.app import App
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Snakes 0.2.0')

    app = App(arguments)
    #while app.is_running:
        #app.process()
