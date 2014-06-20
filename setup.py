import sys, os
from cx_Freeze import setup, Executable

base = None
include_files = ['finder.ui']

build_mac_options = {
    'iconfile': "ECCIcon.icns",
    'bundle_name': "BCS Finder",
    'qt_menu_nib': os.environ['HOME'] + '/Qt/5.3/clang_64/plugins/platforms/'
}

build_exe_options = {
    'include_files': include_files, 
    # I'd prefer to handle this here, but then I get errors about PyQt5.uic missing
    #'excludes': ['PyQt5.QtWebKit', 'PyQt5.QtNetwork'],
}

setup(  name = "BCS Finder",
        version = "1.0",
        description = "BCS Finder",
        options = { "bdist_mac": build_mac_options,
                    "build_exe": build_exe_options },
        executables = [Executable("finder.py", base=base)])


# Remove unnecessary libraries from the .app file to bring the size down
if(sys.platform == 'darwin'):
    for library in ['QtWebKit', '_debug', 'QtNetwork', 'QtQuick', 'QtQml']:
        os.system("find build/BCS\ Finder.app/ -iname '*{}*' -delete".format(library))
