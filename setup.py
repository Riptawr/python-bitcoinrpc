#!/usr/bin/env python3.6

from distutils.core import setup

setup(
    name='python3-bitcoinrpc',
    version='1.0',
    description='Port of python-jsonrpc to Python 3.6 for use with Bitcoin',
    long_description=open('README.md').read(),
    author='Alexander Korolev',
    author_email='<lx.korolev@gmail.com>',
    maintainer='Alexander Korolev',
    maintainer_email='<lx.korolev@gmail.com>',
    url='https://github.com/Riptawr/python-bitcoinrpc/',
    packages=['bitcoinrpc'],
    classifiers=[
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)', 'Operating System :: OS Independent'
    ]
)
