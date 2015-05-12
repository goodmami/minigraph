#!/usr/bin/env python3

from setuptools import setup, Extension

long_description='''\
MiniGraph is a simple, reasonably fast module for graph structures. It
is not very featureful, but easy to use for the common cases.'''

setup(
    name='MiniGraph',
    version='0.1',
    description='A small Python module for working with small graph structures.',
    long_description=long_description,
    url='https://github.com/goodmami/minigraph',
    author='Michael Wayne Goodman',
    author_email='goodman.m.w@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='graphs',
    packages=[
        'minigraph',
    ],
    ext_modules=[
        Extension('minigraph', ['minigraph.c'])
    ],
    #extras_require={
    #    'toolbox': ['toolbox'],
    #    'itsdb': ['pydelphin']
    #}
    test_suite='tests'
)
