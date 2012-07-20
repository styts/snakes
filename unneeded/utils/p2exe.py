# py2exe setup program
from distutils.core import setup
import py2exe
import sys
import os
import glob, shutil
import pygame
import engine, logic

sys.argv.append("py2exe")
 
VERSION = '0.0.1'
AUTHOR_NAME = 'Kirill Stytsenko'
AUTHOR_EMAIL = 'gamedev@styts.com'
AUTHOR_URL = "http://gamedev.styts.com/"
PRODUCT_NAME = "Snakes Puzzle Game"
SCRIPT_MAIN = '../main.py'
VERSIONSTRING = PRODUCT_NAME + " pre-alpha " + VERSION
ICONFILE = '../icon.ico'

# Remove the build tree on exit automatically
REMOVE_BUILD_ON_EXIT = True
PYGAMEDIR = os.path.split(pygame.base.__file__)[0]
 
SDL_DLLS = glob.glob(os.path.join(PYGAMEDIR,'*.dll'))
 
if os.path.exists('dist/'): shutil.rmtree('dist/')
 
extra_files = [ ("",[]),
                   #("data",glob.glob(os.path.join('..','data','*'))),
                   #("gfx",glob.glob(os.path.join('gfx','*.jpg'))),
                   #("gfx",glob.glob(os.path.join('gfx','*.png'))),
                   #("fonts",glob.glob(os.path.join('fonts','*.ttf'))),
                   #("music",glob.glob(os.path.join('music','*.ogg'))),
                   #("snd",glob.glob(os.path.join('snd','*.wav')))
                   ]

MODULE_EXCLUDES = []
INCLUDE_STUFF = ['encodings',"encodings.latin_1",]
 
setup(windows=[
             {'script': SCRIPT_MAIN,
               'other_resources': [(u"VERSIONTAG",1,VERSIONSTRING)],
               'icon_resources': [(1,ICONFILE)],
               }],
         options = {"py2exe": {
                             "optimize": 2,
                             "includes": INCLUDE_STUFF,
                             "compressed": 1,
                             "ascii": 1,
                             "bundle_files": 2,
                             "ignores": ['tcl','AppKit','Numeric','Foundation'],
                             "excludes": MODULE_EXCLUDES} },
          name = PRODUCT_NAME,
          version = VERSION,
          data_files = [],
          zipfile = None,
          author = AUTHOR_NAME,
          author_email = AUTHOR_EMAIL,
          url = AUTHOR_URL)

# don't need TCL
if os.path.exists('dist/tcl'): shutil.rmtree('dist/tcl') 
 
# Remove the build tree
if REMOVE_BUILD_ON_EXIT:
     shutil.rmtree('build/')
 
if os.path.exists('dist/tcl84.dll'): os.unlink('dist/tcl84.dll')
if os.path.exists('dist/tk84.dll'): os.unlink('dist/tk84.dll')
 
for f in SDL_DLLS:
    fname = os.path.basename(f)
    try:
        shutil.copyfile(f,os.path.join('dist',fname))
    except: pass
    
shutil.copytree('../data', 'dist/data',ignore=shutil.ignore_patterns('.svn'))
