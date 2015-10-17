#!/usr/bin/env python

from pip.req import parse_requirements
from setuptools import setup, find_packages


with open('VERSION.txt', 'r') as v:
    version = v.read().strip()

# Requirements
install_reqs = parse_requirements('requirements.txt', session='dummy')
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='git-projects',
    description='Pure git commands for multi-repository projects',
    url='https://github.com/thavel/git-projects',
    author='Thibaut Havel',
    version=version,
    install_requires=reqs,
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': ['gp = git_projects.gp:main']
    },
)
