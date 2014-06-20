import sys, os
from cx_Freeze import setup, Executable

base = None

build_exe_options = {
    'include_files': ['finder.ui'],
	'compressed': True
    # I'd prefer to handle this here, but then I get errors about PyQt5.uic missing
    #'excludes': ['PyQt5.QtWebKit', 'PyQt5.QtNetwork'],
}

build_msi_options = {
	'upgrade_code': '{676a8144-0723-4e58-a7ed-21e822aa7537}'
}

if sys.platform == 'darwin':
	build_mac_options = {
		'iconfile': "ECCIcon.icns",
		'bundle_name': "BCS Finder",
		'qt_menu_nib': os.environ['HOME'] + '/Qt/5.3/clang_64/plugins/platforms/'
	}
	
elif sys.platform == 'win32':
	build_mac_options = {}
	base = "Win32GUI"
	build_exe_options['icon'] = 'ecc.ico'
	
setup(  name = "BCS Finder",
        version = "1.0",
        description = "BCS Finder",
        options = { "bdist_mac": build_mac_options,
                    "build_exe": build_exe_options,
					"build_msi": build_msi_options},
        executables = [Executable("finder.py", base=base)])


# Remove unnecessary libraries from the .app file to bring the size down
if sys.platform == 'darwin':
    for library in ['QtWebKit', '_debug', 'QtNetwork', 'QtQuick', 'QtQml']:
        os.system("find build/BCS\ Finder.app/ -iname '*{}*' -delete".format(library))
