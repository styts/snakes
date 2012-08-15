#!/usr/bin/env python

import os
import sys

pfm = sys.platform
cwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(cwd)

# build
path2build = {}
path2build["darwin"] = "~/bin/pyinstaller/utils/"
path2build["win32"] = "T:\\bin\\pyinstaller\\utils\\"

command = "python %sBuild.py --noconfirm %s.spec" % (path2build[pfm], pfm)

os.system(command)

# prepare
d = os.path.join("..", 'dist')
if not os.path.exists(d):
    os.makedirs(d)

# distribute
if pfm == 'darwin':
    os.system("rm -rf ../dist/Snakes.app")
    os.system("mv dist/Snakes.app ../dist/")
else:
    os.system("rm -rf ../dist/Snakes")
    os.system("mv dist/Snakes ../dist/")

# cleanup
os.system("rm -rf build dist logdict*.log ../logdict*.log")
