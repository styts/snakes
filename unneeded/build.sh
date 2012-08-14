## Remove previous builds.  Start with clean slate.
rm -rf build dist

## Force python into 32 bit mode.
export VERSIONER_PYTHON_PREFER_32_BIT=yes

## Force build with custom installed python
#/Library/Frameworks/Python.framework/Versions/2.7/bin/python setup.py py2app
python setup.py py2app
