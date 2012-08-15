#!/usr/bin/env python

import os
import sys

pfm = sys.platform
os.chdir(os.path.dirname(__file__))

# build
path2build = {}
path2build["darwin"] = "~/bin/pyinstaller/utils/"
path2build["win32"] = "T:\\bin\\pyinstaller\\utils\\"

command = "python %sBuild.py --noconfirm %s.spec" % (path2build[pfm], pfm)

os.system(command)

# distribute
os.system("mkdir -p %s" % os.path.join("..", 'dist'))
if pfm == 'darwin':
    os.system("rm -rf ../dist/Snakes.app")
    os.system("mv dist/Snakes.app ../dist")
else:
    os.system("rm -rf ..\\dist\\Snakes")
    os.system("mv dist\\Snakes ..\\dist")

# cleanup
os.system("rm -rf build dist logdict*.log")
