# -*- coding: utf-8 -*-
from setuptools import setup

try:
    with open('requirements.txt') as f:
        required = f.read().splitlines()
except:
    required = ['Pillow==5.3.0', 'future==0.16.0']

setup(name="carto-print",
      author="Alberto Romeu",
      author_email="alrocar@carto.com",
      description="A module to export images from CARTO named maps",
      version="0.0.4",
      url="https://github.com/CartoDB/carto-print",
      install_requires=required,
      packages=["carto"],
      scripts=["bin/carto-print"])
