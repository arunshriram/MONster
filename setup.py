"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['MONster.py']
DATA_FILES = []
OPTIONS = {'iconfile': '/Users/arunshriram/Documents/SLAC Internship/MONster/images/appicon.icns'}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)