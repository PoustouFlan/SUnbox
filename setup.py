#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'sunbox',
    version = '1.0',
    packages = find_packages(
        include=['sunbox','sunbox.*']
    ),
    scripts = ['main.py'],
    install_requires=[
        'numpy>=1.24.2',
        'pillow>=9.4.0'
    ]
)
