from setuptools import setup

APP = ['Snakes.py']
DATA_FILES = ['data']

OPTIONS = {
    "argv_emulation": False,
    "compressed" : True,
    #"optimize":2,
    #"iconfile":'data/game.icns',
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
)
