# -*- mode: python -*-

#### platform-specifics ###################
import sys
platform = sys.platform
pathex = {}
pathex["darwin"] = ['/Users/kirill/Backup/projects/snakes2']
pathex["win32"] = ['T:\\Backup\\projects\\snakes2']

extention = {}
extention["darwin"] = ""
extention["win32"] = ".exe"

exe_name = {}
exe_name["darwin"] = os.path.join('..', 'build', 'Snakes.darwin', 'Snakes')
#exe_name["win32"] = os.path.join('..', 'build', 'Snakes.win32')#, 'Snakes.exe'),
exe_name["win32"] = os.path.join('..\\build\\pyi.win32\\Snakes', 'Snakes.exe')

###########################################


##### include mydir in distribution #######
def extra_datas(mydir):
    def rec_glob(p, files):
        import os
        import glob
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
            rec_glob("%s/*" % d, files)
    files = []
    rec_glob("%s/*" % mydir, files)
    extra_datas = []
    for f in files:
        extra_datas.append((f, f, 'DATA'))

    return extra_datas
###########################################

import os
os.chdir("..")
a = Analysis(['Snakes.py'],
             pathex=pathex[platform],
             hiddenimports=[],
             hookspath=None,
             excludes=["matplotlib", "scipy", "numpy", "unicodedata", "smpeg", "readline",
                 "_codecs_jp", "_codecs_hk", "_codecs_cn", "_codecs_kr", "_codecs_tw"]
             )

# append the 'data' dir
a.datas += extra_datas('data')

pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=exe_name[platform],
          debug=False,
          strip=False if platform == "win32" else True,
          upx=True,
          console=True)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=True,
               upx=True,
               name=os.path.join('..', 'dist', 'Snakes.%s' % platform))