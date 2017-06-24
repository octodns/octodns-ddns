#!/usr/bin/env python

from os.path import dirname, join
import octodns_ddns

try:
    from setuptools import find_packages, setup
except ImportError:
    from distutils.core import find_packages, setup

setup(
    author='Ross McFarland',
    author_email='rwmcfa1@gmail.com',
    description=octodns_ddns.__doc__,
    install_require=[
        'octodns>=0.8.0',
        'requests>=2.13.0'
    ],
    tests_require=[
        'mock',
        'nose',
    ],
    test_suite='nose.collector',
    license='MIT',
    long_description=open('README.md').read(),
    name='octodns-ddns',
    packages=find_packages(),
    url='https://github.com/ross/octodns-ddns',
    version=octodns_ddns.__VERSION__,
)
