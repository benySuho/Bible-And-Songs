import PyInstaller.__main__
from distutils.dir_util import copy_tree
import shutil


# Create executable using PyInstaller with all required files included in the build folder.
PyInstaller.__main__.run([
    'main.py',
    '-y',
    '--windowed',
    '--distpath',
    'Program',
    '--clean',
    '--icon=icon.ico',
    '-n',
    'BibleAndSongs',
    '--add-data=icon.ico:./'
])
shutil.copy('icon.ico', 'Program/BibleAndSongs/')
copy_tree('Bible', 'Program/BibleAndSongs/Bible')

