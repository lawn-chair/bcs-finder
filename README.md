BCS Finder
==========

BCS Finder Application for Windows/Mac/Linux.  Only works with BCS firmware version 4.0 alpha preview 3 and later.

## Requirements
  * [Qt 5][qt5] - tested with 5.3.0
  * [PyQt5][pyqt5] - tested with 5.3
  * [Python 3][python] - tested with 3.3.3, 3.4.1
  * [cx_Freeze][cxFreeze] - For building Mac/Windows executables

## Setup

### Mac
  Build an .app with:
    
    python setup.py bdist_mac

### Any platform
  Run directly from command line
    
    python finder.py


[qt5]: http://qt-project.org/downloads "Qt Project"
[pyqt5]: http://www.riverbankcomputing.co.uk/software/pyqt/download5 "PyQt5"
[python]: http://www.python.org "Python"
[cxFreeze]: http://cx-freeze.readthedocs.org/en/latest/ "cx_Freeze"
