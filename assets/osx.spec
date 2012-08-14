# -*- mode: python -*-

a = Analysis(['Snakes.py'],
             pathex=['/Users/kirill/Backup/projects/snakes2'],
             hiddenimports=[],
             hookspath=None,
             )

##### exclude some heavy libraries #####
excl_bins = ["matplotlib", "scipy", "numpy"]
for x in a.binaries:
    if any(map(x[0].startswith, excl_bins)):
          a.binaries.remove(x)
    else:
          print "binary:", x[0]


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


a.datas += extra_datas('data')


pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('../build/pyi.darwin/Snakes', 'Snakes'),
          debug=False,
          strip=True,
          upx=True,
          console=True)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=True,
               upx=True,
               name=os.path.join('..', 'dist', 'Snakes.osx'))
