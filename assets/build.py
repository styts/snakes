#!/usr/bin/env python

import os
import sys

pfm = sys.platform

path2build = {}
path2build["darwin"] = "~/bin/pyinstaller/utils/"
path2build["win32"] = "T:\\bin\\pyinstaller\\utils\\"

sep = {}
sep['darwin'] = '/'
sep['win32'] = '\\'

os.chdir(os.path.dirname(__file__))

buildpath = "\"%s\" \"%s\"" % (os.path.join("..", "build", "pyi.%s" % pfm),
                       "build.spec")

command = "python %sBuild.py --noconfirm --buildpath=%s" % (path2build[pfm], buildpath)

#print command

os.system(command)
