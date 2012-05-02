"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

import sys
import os
sys.path.append("src")

sys.path.insert(0, os.path.join(os.getcwd(), 'lib', 'python2.7', 'lib-dynload'))  # Added to fix dynlib bug

APP = ['Snakes.py']
DATA_FILES = []
OPTIONS = {'argv_emulation': True, 'includes': ['engine', 'pygame', 'networkx', ]}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
