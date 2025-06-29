#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Six Keys Criticality - A Framework for Neural Consciousness State Analysis
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='sixkeys',
    version='0.1.0',
    description='A Framework for Neural Consciousness State Analysis based on Critical Transition Theory',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='You Yang Hou',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/sixkeys',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    python_requires='>=3.8',
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'black>=21.0',
            'flake8>=3.8',
            'sphinx>=4.0',
            'sphinx-rtd-theme>=1.0',
            'jupyter>=1.0',
            'notebook>=6.0',
        ],
        'gpu': [
            'cupy>=9.0',
            'torch>=1.9.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'sixkeys-cli=sixkeys.cli:main',
        ],
    },
    include_package_data=True,
    package_data={
        'sixkeys': [
            'data/*.json',
            'data/*.csv',
            'examples/*.py',
        ],
    },
    keywords=[
        'neuroscience',
        'consciousness',
        'critical transitions',
        'brain networks',
        'free energy',
        'information theory',
    ],
    project_urls={
        'Documentation': 'https://sixkeys.readthedocs.io/',
        'Source': 'https://github.com/yourusername/sixkeys',
        'Tracker': 'https://github.com/yourusername/sixkeys/issues',
    },
)