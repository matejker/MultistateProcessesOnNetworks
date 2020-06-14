#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

with open("requirements/base.txt") as f:
    required = f.read().splitlines()

setup(
    name="mk-MultistateProcessesOnNetworks",
    version="0.0.2",
    description="A generic framework for simulating and calculating multistate dynamical processes on networks.",
    author="Matej Kerekrety",
    author_email="matej.kerekrety@gmail.com",
    packages=find_packages(exclude=("tests", "notebooks")),
    install_requires=required,
)
