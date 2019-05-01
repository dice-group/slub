# -*- coding: utf-8 -*-
"""setup.py for the slub project."""
from setuptools import find_packages, setup

setup(
    name='slub',
    version="0.0.1",
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        'BeautifulSoup',
        'lxml'
    ],
)
