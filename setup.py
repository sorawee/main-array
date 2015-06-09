#!/usr/bin/env python

from setuptools import setup, find_packages
setup(
    name = "Main Array Generator",
    description='printf without printf, but with main... as an array!',
    version = "0.1",
    author='Sorawee Porncharoenwase',
    author_email='sorawee_porncharoenwase@brown.edu',
    packages = find_packages(),
    install_requires = ['pexpect>=0.1'],
    scripts=['gen.py']
)