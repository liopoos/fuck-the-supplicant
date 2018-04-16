#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16/04/2018 12:51
# @Author  : hades
# @Software: PyCharm

from setuptools import setup

APP = ['main.py']
DATA_FILES = ['icon.png']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'app.icns',
    'plist': {
        'LSUIElement': True,
        'CFBundleName': "Fuck The Supplicant",
        'CFBundleDisplayName': "Fuck The Supplicant",
        'CFBundleGetInfoString': "Fuck The Supplicant",
        'CFBundleIdentifier': "blog.mayuko.cn",
        'CFBundleVersion': "0.1.1",
        'CFBundleShortVersionString': "0.1.1"
    },
    'packages': ['rumps'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
