# -*- mode: python -*-
a = Analysis(['..\\Snakes.py'],
             pathex=['T:\\Backup\\projects\\snakes2'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('..\\build\\pyi.win32\\Snakes', 'Snakes.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('..', 'dist', 'Snakes'))
