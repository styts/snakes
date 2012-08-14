# -*- mode: python -*-
import shutil

shutil
a = Analysis(['Snakes.py'],
             pathex=['/Users/kirill/Backup/projects/snakes2'],
             hiddenimports=[],
             hookspath=None,
             )

# exclude some heavy libraries
excl_bins = ["matplotlib", "scipy", "numpy"]
for x in a.binaries:
    if any(map(x[0].startswith, excl_bins)):
          a.binaries.remove(x)
    else:
          print "binary: ", x[0]

pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.darwin/Snakes', 'Snakes'),
          debug=True,
          strip=None,
          upx=True,
          console=True )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'Snakes'))
