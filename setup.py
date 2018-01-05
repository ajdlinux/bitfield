#!/usr/bin/env python
#
# Utility to decode register values
# Copyright (c) 2006-2017 Jeremy Kerr <jk@ozlabs.org> and contributors
# Released under the GNU General Public License version 2 or later

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bitfield',
    version='0.3.0',
    description='Utility to decode register values',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ajdlinux/bitfield',
    author='Jeremy Kerr',
    author_email='jk@ozlabs.org',
    license='GPLv2+',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='bitfield bit register hardware',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['pyparsing'],

    entry_points={
        'console_scripts': [
            'bitfield=bitfield.bitfield:main',
        ],
    },

    package_data={
        '': ['README.md', 'bitfield.vim', 'bitfield-completions.sh'],
    },
)
