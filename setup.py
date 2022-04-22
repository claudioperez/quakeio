#!/usr/bin/env python

import setuptools

#import atexit
#from setuptools.command.install import install
#from setuptools.command.develop import develop
#from setuptools.command.egg_info import egg_info
#
#
#def install_styles():
#    try:
#        import matplotlib
#    except ImportError:
#        print("WARNING - Failed to install style sheets")
#        return
#    import shutil, os, glob
#
#    mpl_stylelib_dir = os.path.join(matplotlib.get_configdir(), "stylelib")
#    # Find all style files
#    stylefiles = glob.glob('styles/**/*.mplstyle', recursive=True)
#    # Find stylelib directory (where the *.mplstyle files go)
#    if not os.path.exists(mpl_stylelib_dir):
#        os.makedirs(mpl_stylelib_dir)
#    # Copy files over
#    print("Installing styles into", mpl_stylelib_dir)
#    for stylefile in stylefiles:
#        print(os.path.basename(stylefile))
#        shutil.copy(
#            stylefile,
#            os.path.join(mpl_stylelib_dir, os.path.basename(stylefile)))
#
#class InstallMoveFile(install):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        atexit.register(install_styles)
#
#class EggInfoMoveFile(egg_info):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        atexit.register(install_styles)
#
#class DevelopMoveFile(develop):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        atexit.register(install_styles)


if __name__ == "__main__":
    setuptools.setup(
#        cmdclass={
#            'install': InstallMoveFile,
#            'egg_info': EggInfoMoveFile,
#            'develop': DevelopMoveFile
#        }
    )

