#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'sbox-your-mom',
    version = '1.0',
    packages = find_packages(
        include=['sboxyourmom','sboxyourmom.*']
    ),
    scripts = ['main.py'],
    install_requires=[
        'numpy>=1.24.2',
        'pillow>=9.4.0'
    ]
)
