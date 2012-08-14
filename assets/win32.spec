# -*- mode: python -*-
a = Analysis(['Snakes.py'],
             pathex=['T:\\Backup\\projects\\snakes2'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('..', 'dist', 'win32', 'Snakes.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True )
