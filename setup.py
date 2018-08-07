#!/usr/bin/env python

from distutils.core import setup

setup(
    name='bcli',
    version='0.7.0',
    description='EC2 Cluster Creator',
    author='Hugo Wang',
    author_email='w@mitnk.com',
    url='https://github.com/mitnk/bcli',
    packages=['bcli'],
    install_requires=[
        'boto3==1.7.65',
    ],
    entry_points={
        'console_scripts': [
            'bcli=bcli.bcli:main',
        ],
    },
)
