#!/usr/bin/env python

from distutils.core import setup

setup(
    name='raptorpy',
    version='0.1dev',
    description='A Raptor client for python',
    author='Andrea Gilardoni',
    author_email='gilardoni@fbk.eu',
    url="https://github.com/raptorbox/raptorpy"
    packages=["raptorpy"],
    long_description=open('README.rst').read(),
    install_requires=["requests", "paho-mqtt"],
)
